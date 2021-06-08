# SHP.EXchange
Кратко: эмулятор биржи

Развёрнуто: 
- Акции
- Покупка / Продажа
- Торговля в лонг
- Торговля в шорт
- Торговля с плечом
- Margin call
- История - загружается в виде массива котировок. Позже - эмулируется ботами.

## Технологический стек
- Python 3.8 (не меньше)
- Django 3
- Django REST Framework


## Подготовка рабочего места разработчика.

### Установка необходимых библиотек
```bash
sudo apt install make gcc g++
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs
````

### Backend
1. В главной папке проекта необходимо создать папку `data` и поместить туда .csv файлы из [необходимых файлов](https://gitlab.informatics.ru/2020-2021/mytischi/s105/exchange_engine/-/wikis/%D0%9D%D0%B5%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B8%D0%BC%D1%8B%D0%B5-%D1%84%D0%B0%D0%B9%D0%BB%D1%8B) в Wiki проекта. 
   Они нужны будут для запуска ботов
2. Создать venv, установить библиотеки

   ```bash
   python3.8 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Подготовить БД
   * Установить postgresql
     ```bash
     sudo apt install postgresql
     sudo systemctl start postgresql.service
     sudo systemctl enable postgresql.service
     ```
   * Создать юзера и базу
     ```bash
     sudo -u postgres psql
     ```
     Далее в консоли postgresql
     ```sql
     create database exchange;
     create user shp with encrypted password 'promprog';
     grant all privileges on database exchange to shp;
     \q
     ```
   * Скачать из [необходимых файлов](https://gitlab.informatics.ru/2020-2021/mytischi/s105/exchange_engine/-/wikis/%D0%9D%D0%B5%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B8%D0%BC%D1%8B%D0%B5-%D1%84%D0%B0%D0%B9%D0%BB%D1%8B) 
     файл `exchange.sql`, поместить его в корень проекта и загрузить его в БД командой
     ```bash
     sudo -u postgres psql exchange < exchange.sql
     ```
   * Актуализировать схему
     ```bash
     ./manage.py migrate
     ```
   * создать юзера (выполняется только для разработки, в продакшене не делать)
     ```bash
     ./manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
     ```

### Frontend
Здесь всё просто
```bash
cd exchange_engine_frontend
npm install
```

### Запуск проекта
```bash
python price_bot.py    # открыть в отдельной вкладке, команда будет работать на протяжении всего времени
python candles_bot.py    # открыть в отдельной вкладке, команда будет работать на протяжении всего времени
./manage.py runserver  # открыть в отдельной вкладке, команда будет работать на протяжении всего времени
cd exchange_engine_frontend
npm run serve  # открыть в отдельной вкладке, команда будет работать на протяжении всего времени
```

## Тесты
Для тестирования чистоты кода введите в терминал команду:
```bash
DJANGO_SETTINGS_MODULE=exchange_engine.settings pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations *
```

Для тестирования самого кода введите в терминал:
```bash
./manage.py test
```


## Дополнительно

Все необходимые файлы вы можете найти здесь: https://gitlab.informatics.ru/2020-2021/mytischi/s105/exchange_engine/-/wikis/%D0%9D%D0%B5%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B8%D0%BC%D1%8B%D0%B5+%D1%84%D0%B0%D0%B9%D0%BB%D1%8B

Более подробная информация и проекте и его запуске доступна по ссылке: https://gitlab.informatics.ru/2020-2021/mytischi/s105/exchange_engine/-/wikis/home
