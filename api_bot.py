import getpass
import requests


def login(host):
    """
    Авторизация

    Авторизация порисходит с помощью JWT токенов. При запросе на большую часть страниц необходимо передавать этот токен.
    """
    # данные пользователя
    data = {
        'username': input('Enter your username: ').strip(),
        'password': getpass.getpass('Enter your password: ').strip()
    }

    # получаем токены данного пользователя
    api_token_url = f'{host}/api-token/'  # обращаемся к url с токенами
    tokens = requests.post(api_token_url, data=data).json()  # запрос на страницу
    access_token = tokens['access']  # получаем токен, необходимый для авторизации
    return access_token  # возвращаем токен


def create_order(host, headers):
    """
    Создание ордера на покупку/продажу
    """
    # создаём ордер
    orders_url = f'{host}/orders/add'  # обращаемся к url для создания ордера
    # данные, необходимые для запроса
    data = {
        'stock': input('Enter name of stock: ').strip(),
        'amount': int(input('Enter amount of stocks: ').strip()),
        'type': bool(int(input('Enter "0" if you want to buy stock(s), else enter "1": ').strip())),
        'price': int(input('Enter price (or "0" if you want to trade at market price): ').strip())
    }
    requests.post(orders_url, headers=headers, json=data)  # делаем запрос, передавая токен и данные


def list_orders(host, headers):
    """
    Список всех ордеров пользователя
    """
    # смотрим список всех ордеров, убеждаясь, что ордер создан
    orders_list_url = f'{host}/api/v1/orders/'
    response = requests.get(orders_list_url, headers=headers)
    return response.json()


def list_candles(host, headers):
    """
    Список всех свечей

    В зависимости от настроек, вы можете увидеть только свечи за последние N минут.
    """
    # ввод данных, необходимых для запроса
    stock_id = int(input('Enter stock id: '))
    candles_type = int(input('Enter candle type ("0" if you want to see all candles for this stock): '))

    # список свечей
    candles_list_url = f'{host}/api/v1/candles/{stock_id}/{candles_type}'
    response = requests.get(candles_list_url, headers=headers)
    return response.json()


def list_stocks(host):
    """
    Список всех акций
    """
    orders_list_url = f'{host}/api/v1/stocks/'
    response = requests.get(orders_list_url)
    return response.json()


def readable_orders_print(orders, style):
    """
    Удобная отрисовка списка ордеров пользователя

    `table` - если вы хотите вывести ордера в виде таблицы, `default` - если вы хотите их вывести в стандартном формате.
    """
    if style == 'table':
        print('---ID----NAME----COUNT---PRICE--------TYPE--------STATE----USER_ID----DESCRIPTION')
        for order in orders:
            print(f"   {order['stock']['id']}     {order['stock']['name']}      {order['count']}     "
                  f"{format(order['price'], '.2f') if (10000 > int(order['price']) >= 1000)  else format(order['price'], '.3f') if int(order['price']) < 1000 else format(order['price'], '.1f') if int(order['price']) >= 10000 else format(order['price'], '.0f')}      "
                  f"{'buying'.ljust(7) if not order['type'] else 'selling'}     "
                  f"{'closed' if order['is_closed'] else 'open'}     {order['user']}       {order['stock']['description']}")
        print('---ID----NAME----COUNT---PRICE--------TYPE--------STATE----USER_ID----DESCRIPTION')
    elif style == 'default':
        for order in orders:
            print(f"Stock ID: {order['stock']['id']}, stock name: {order['stock']['name']}, stock description: "
                  f"{order['stock']['description']}. Order price: {order['price']}, order amount: {order['count']}, "
                  f"order type: {'buy' if not order['type'] else 'sell'}, "
                  f"order state: {'closed' if order['is_closed'] else 'open'}. User ID: {order['user']}.")


def main():
    """
    Пример клиентского API бота для создания ордеров
    """
    host = 'http://shp-exchange.tk'  # сюда надо ввести правильный адрес хоста

    # авторизация
    access_token = login(host)
    headers = {'Authorization': f'Bearer {access_token}'}
    create_order(host, headers)

    # просмотр списка ордеров
    orders = list_orders(host, headers)
    readable_orders_print(orders, 'table')


if __name__ == "__main__":
    main()
