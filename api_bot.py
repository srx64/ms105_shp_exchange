import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_engine.settings')
django.setup()


def main():
    data = {
        'username': 'vasya',
        'password': 'promprog'
    }
    api_token_url = 'http://127.0.0.1:8000/api-token/'
    tokens = requests.post(api_token_url, data=data).json()
    access_token = tokens['access']
    orders_url = 'http://127.0.0.1:8000/orders/add/'
    data = {
        'stock': 'OZON',
        'amount': 1,
        'type': False,
        'price': 0
    }
    response = requests.post(orders_url, headers={'Authorization': f'Bearer {access_token}'}, data=data)
    print(response)
    url = 'http://127.0.0.1:8000/api/v1/orders/'
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})
    print(response.json())


if __name__ == "__main__":
    main()
