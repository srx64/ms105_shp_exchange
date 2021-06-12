import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()


def main():
    """
    Пример клиентского API бота
    """
    host = 'http://127.0.0.1:8000'

    # данные пользователя
    data = {
        'username': input('Enter your username: '),
        'password': input('Enter your password: ')
    }

    # получаем токены данного пользователя
    api_token_url = f'{host}/api-token/'
    tokens = requests.post(api_token_url, data=data)
    print('Login successful.')
    access_token = tokens.json()['access']  # получаем токен, необходимый для авторизации

    # создаём ордер
    orders_url = f'{host}/orders/add'
    data = {
        'stock': input('Enter name of stock: '),
        'amount': int(input('Enter amount of stocks: ')),
        'type': bool(input('Enter "0" if you want to bue stock(s), else enter "1": ')),
        'price': int(input('Enter price (or "0" if you want to trade at market price): '))
    }
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(orders_url, headers=headers, json=data)
    print(response.status_code)

    # смотрим список всех ордеров
    url = f'{host}/api/v1/orders/'
    response = requests.get(url, headers=headers)
    print(response.json())


if __name__ == "__main__":
    main()
