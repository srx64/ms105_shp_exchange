"""
:module: candles_bot.py

Бот для группирования котировок в свечи.
"""

import argparse
import logging
import math
import os
import signal
import sys
import time
from datetime import datetime
from typing import List, Optional

import django
import pytz
from django.utils import timezone

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
    django.setup()
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc

from main.models import Stocks, Candles, Quotes, CandlesData, Settings

"""
Список всех инструментов.
Загружается только один раз. Для обновления используйте сигнал SIGHUP или просто перезапустите бота.
"""
STOCKS_LIST = None


def get_acceleration(stock_id):
    setting = None
    if Settings.objects.filter(stock_id=-1, name='chart_settings'):
        setting = Settings.objects.filter(stock_id=-1, name='chart_settings').last()
    elif Settings.objects.filter(stock_id=stock_id, name='chart_settings'):
        setting = Settings.objects.filter(stock_id=stock_id, name='chart_settings').last()
    if setting is not None:
        return setting.data['acceleration']
    else:
        return 1



def generate(prices: List[Quotes], prices_amount: int, stock: Stocks, timeframe_duration: int,
             timeframe_index: int, last_candle_data: List[int]) -> Optional[List[int]]:
    """
    Кусок кода, объединяющий котировки в свечи. Создаёт новую свечу для указанного инструмента и таймфрейма
    на основе массива котировок

    :param prices: список котировок
    :param prices_amount: количество доступных котировок
    :param stock: текущий финансовый инструмент, для которого генерируется свеча
    :param timeframe_duration: количество секунд данных, агрегируемых в текущую свечу
    :param timeframe_index: номер типа таймфрейма.
    :param last_candle_data: данные последней свечи.

    .. warning::
       Я не понимаю, как работает эта функция. Есть подозрение, что она не рассматриваем случай, когда текущий
       таймфрейм ещё не закончился. И всегда генерирует новую котировку.

    .. note::
       Как должна работать эта функция:

       Взять последнюю свечу указанного диапазона для указанного инструмента
       Проверить, не истёк ли текущий таймфрейм
       Если истёк - начать новую свечу
       Обновить данные свечи в соответствии с новыми данными
       Повторить для всех таймфреймов

    .. todo::
       Перенести этот функционал в price_bot'а. Это будет быстрее.
       А ещё лучше - перенести его на уровень моделей: во время генерации новой Quote'ы - можно сразу загружать
       все свечи по текущему инструменту и обновлять последние.

    .. todo::
       Обработать случай, в котором не генерируется новая, а изменяется последняя свеча.

    .. todo::
       Отрефакторить это. Разбить на функции, сгруппировать в класс.

    .. todo::
       После рефакторинга - добавить сюда логирование.
    """

    accelerator = get_acceleration(stock.pk)
    timeframe_duration = timeframe_duration / accelerator
    is_exist = False
    stock_prices = []
    shift = prices[0].date - prices[0].date
    i = last_candle_data[timeframe_index - 1]
    while i < prices_amount and not CandleBot.NEED_STOP:
        is_exist = False
        prices = list(Quotes.objects.filter(stock=stock))
        prices_amount = len(prices)
        for candle in Candles.objects.filter(stock=stock, type=timeframe_index):
            if (datetime.now(pytz.timezone('Europe/Moscow')) - candle.date).total_seconds() <= timeframe_duration:
                is_exist = True
        if prices_amount >= 2:
            shift += prices[i + 1].date - prices[i].date
            if shift.seconds <= timeframe_duration:
                stock_prices.append(prices[i].price)
                logging.debug(f'Добавлена новая котировка: {prices[i].price}')
                if not (Candles.objects.filter(stock=stock, type=timeframe_index) or is_exist) and len(
                    Candles.objects.filter(stock=stock, type=timeframe_index)) < 5:
                    candle = Candles(
                        high=max(stock_prices),
                        low=min(stock_prices),
                        date=timezone.now(),
                        type=timeframe_index,
                        open=stock_prices[0],
                        close=stock_prices[-1],
                        stock=stock
                    )
                    logging.debug(f'Добавлена новая свеча: {candle}')
                    stock_prices = []
                    candle.save()
                elif (datetime.now(pytz.timezone('Europe/Moscow')) -
                    Candles.objects.filter(stock=stock, type=timeframe_index).last().date).total_seconds() \
                    <= (timeframe_duration):
                    candle = Candles.objects.filter(stock=stock, type=timeframe_index).last()
                    if max(stock_prices) > candle.high:
                        candle.high = max(stock_prices)
                    if min(stock_prices) < candle.low:
                        candle.low = min(stock_prices)
                    candle.close = stock_prices[-1]
                    logging.debug(f'Обновлена свеча: {candle}')
                    stock_prices = []
                    candle.save()
                elif len(Candles.objects.filter(stock=stock)) >= 5 or len(
                    Candles.objects.filter(stock=stock)) >= 5 and not is_exist:
                    if (datetime.now(pytz.timezone('Europe/Moscow')) - Candles.objects.filter(stock=stock,
                                                                                              type=timeframe_index).last().date).total_seconds() >= timeframe_duration:
                        candle = Candles(
                            high=max(stock_prices),
                            low=min(stock_prices),
                            date=timezone.now(),
                            type=timeframe_index,
                            open=stock_prices[0],
                            close=stock_prices[-1],
                            stock=stock,
                        )
                        logging.debug(f'Добавлена новая свеча: {candle}')
                        stock_prices = []
                        candle.save()

            if i == prices_amount - 2:
                last_candle_data[timeframe_index - 1] = i
                return last_candle_data
            i += 1


class CandleBot:
    """
    Основной класс бота. Постоянно в цикле мониторит котировки и обновляет свечи.

    :param NEED_STOP: критерий остановки бота. Изменяется в момент SIGINT'а
    :param CANDLE_TYPES: предопределённые таймфреймы для генерации свечей
    """
    NEED_STOP: bool = False
    CANDLE_TYPES: List[int] = [60, 300, 900, 1800, 3600]

    def __init__(self) -> None:
        """
        Подготовка массива свечей всех типов для всех инструментов
        """
        global STOCKS_LIST
        if len(CandlesData.objects.all()) < 1 or len(CandlesData.objects.all().last().data) < len(Stocks.objects.all()):
            self.data: List[List[int]] = [[0, 0, 0, 0, 0] for _ in range(len(Stocks.objects.all()))]
        else:
            self.data: List[List[int]] = [[0, 0, 0, 0, 0] for _ in range(len(Stocks.objects.all()))]
            tmp = CandlesData.objects.all().last().data
            tmp = str(tmp.replace('[', ''))
            tmp = str(tmp.replace(']', ''))
            tmp = str(tmp.split(sep=','))
            tmp = str(tmp.replace(' ', ''))
            temporary = []
            empty = ''
            tmp = str(tmp).replace("'", '')
            tmp = str(tmp).replace('[', '')
            for i in tmp:
                if i.isdigit():
                    empty += i
                elif i == ',':
                    if len(empty) > 0:
                        temporary.append(int(empty))
                    empty = ''
                elif len(empty) > 0:
                    temporary.append(int(empty))
            for i in range(len(temporary)):
                self.data[i // 5][i % 5] = temporary[i]

    def process_stock(self, stock) -> None:
        """
        Обработка одного инструмента.

        Подгружаем данные из БД и уходим в метод :meth:`generate`
        """
        if Quotes.objects.filter(stock=stock).count() == 0:
            logging.warning(
                f'Не найдены котировки для инструмента с названием {stock}, генерация свеч не производится.')
            return
        info = self.data[stock.pk - 1]
        prices = list(Quotes.objects.filter(stock=stock))
        prices_amount = len(prices)
        for i in range(len(CandleBot.CANDLE_TYPES)):
            logging.debug(f'Генерируем свечу с таймфреймом  {CandleBot.CANDLE_TYPES[i]} для инструмента {stock} ...')
            if info is not None:
                info = generate(prices, prices_amount, stock, CandleBot.CANDLE_TYPES[i], i + 1, info)
            else:
                logging.debug('Параметр "info" имеет тип None.')

    def main_loop(self) -> None:
        """
        Основной цикл бота.

        Запускает генерацию свечей для всех инструментов.
        """
        global STOCKS_LIST
        STOCKS_LIST = Stocks.objects.all()
        while not CandleBot.NEED_STOP:
            for stock in STOCKS_LIST:
                logging.debug(f'Обрабатываем инструмент с названием {stock}...')
                self.process_stock(stock)
            time.sleep(1)

    def run(self) -> None:
        """
        Entrypoint бота.

        Просто запускает бота и отчитывается об этом.
        """
        logging.info('Бот начал работу')
        self.main_loop()
        self.save_data()
        logging.info('Бот закончил работу')

    def save_data(self) -> None:
        """
        Сохранение данных в таблицу

        Сохраняем данные в таблицу перед остановкой бота, во избежание повторной генерации свечей
        """
        if CandleBot.NEED_STOP:
            CandlesData.objects.create(data=self.data)


class Application:
    """
    Универсальный класс приложения.

    Отвечает за обработку сигналов, аргументов командной строки и логи

    :param LOG_FORMAT: формат отображения логов.
    """
    LOG_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'

    def __init__(self):
        args = Application.get_args()

        Application.set_up_logging(args.loglevel)
        Application.set_up_signals()

        logging.info(f'ID процесса: {os.getpid()}')

    @staticmethod
    def set_up_signals() -> None:
        """
        Установка обработчиков сигналов при старте приложения
        """
        logging.info('Установлен обработчик SIGINT')
        signal.signal(signal.SIGINT, Application.keyboard_interrupt)
        if sys.platform != "win32":
            logging.info('Установлен обработчик SIGHUP')
            signal.signal(signal.SIGHUP, Application.update_stocks)
        else:
            logging.info('Приложение запущено на ОС Windows, обработчик SIGHUP не устанавливается')

    @staticmethod
    def keyboard_interrupt(*args) -> None:
        """
        Обработчик прерывания SIGINT.

        Прерывает основной цикл бота.
        """
        logging.info('Получен сигнал прерывания. Завершаем работу')
        CandleBot.NEED_STOP = True

    @staticmethod
    def update_stocks(*args) -> None:
        """
        Обработчик прерывания SIGHUP.

        Загружает обновлённый список инструментов в бота.
        """
        global STOCKS_LIST
        STOCKS_LIST = Stocks.objects.all()

    @staticmethod
    def get_args() -> argparse.Namespace:
        """
        Обработка входных параметров приложения.
        """
        parser = argparse.ArgumentParser(description='Бот для упаковки котировок в свечи')
        parser.add_argument('--loglevel', metavar='L', type=str, default='INFO',
                            help='Уровень детализации логов [DEBUG, INFO, WARNING, ERROR, CRITICAL]')
        return parser.parse_args()

    @staticmethod
    def set_up_logging(loglevel: str) -> None:
        """
        Установка параметров логирования

        :param loglevel: Строка, уровень детализации логов
        """
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            message = f'Invalid log level: {loglevel}'
            logging.critical(message)
            exit(-1)
        logging.basicConfig(format=Application.LOG_FORMAT, level=numeric_level)

    @staticmethod
    def run() -> None:
        """Запуск бота"""
        try:
            global STOCKS_LIST
            STOCKS_LIST = Stocks.objects.all()
            bot = CandleBot()
            bot.run()
        except django.db.utils.OperationalError:
            logging.critical('Не удалось подключиться к БД. Дальнейшая работа приложения невозможна')


if __name__ == "__main__":
    Application().run()
