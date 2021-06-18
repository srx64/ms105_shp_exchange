import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()


def main():
    """
    Пример клиентского API бота для создания ордеров
    """
    host = 'http://127.0.0.1:8000'  # адрес хоста

    # данные пользователя
    data = {
        'username': input('Enter your username: ').strip(),
        'password': input('Enter your password: ').strip()
    }

    # получаем токены данного пользователя
    api_token_url = f'{host}/api-token/'  # обращаемся к url с токенами
    tokens = requests.post(api_token_url, data=data).json()  # запрос на страницу
    access_token = tokens['access']  # получаем токен, необходимый для авторизации

    # создаём ордер
    orders_url = f'{host}/orders/add'  # обращаемся к url для создания ордера
    # данные, необходимые для запроса
    data = {
        'stock': input('Enter name of stock: ').strip(),
        'amount': int(input('Enter amount of stocks: ').strip()),
        'type': bool(input('Enter "0" if you want to bue stock(s), else enter "1": ').strip()),
        'price': int(input('Enter price (or "0" if you want to trade at market price): ').strip())
    }
    headers = {'Authorization': f'Bearer {access_token}'}
    requests.post(orders_url, headers=headers, json=data)  # делаем запрос, передавая токен и данные

    # смотрим список всех ордеров, убеждаясь, что ордер создан
    orders_list_url = f'{host}/api/v1/orders/'
    response = requests.get(orders_list_url, headers=headers)
    print(response.json())


if __name__ == "__main__":
    main()
