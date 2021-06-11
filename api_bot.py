import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()


def main():
    host = 'http://127.0.0.1:8000'
    data = {
        'username': 'vasya',
        'password': 'promprog'
    }
    api_token_url = f'{host}/api-token/'
    tokens = requests.post(api_token_url, data=data).json()
    access_token = tokens['access']
    orders_url = f'{host}/orders/add'
    data = {
        'stock': 'OZON',
        'amount': 1,
        'type': False,
        'price': 0
    }
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(orders_url, headers=headers, data=data)
    print(response)
    url = f'{host}/api/v1/orders/'
    response = requests.get(url, headers=headers)
    print(response.json())


if __name__ == "__main__":
    main()
