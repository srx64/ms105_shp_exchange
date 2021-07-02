from django.test import TestCase, Client
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from main.models import User, Order, Portfolio, Quotes, Stocks, LeverageData, Settings


class ProfileTest(APITestCase):
    fixtures = ['profile_test_database.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.response = self.client.get(reverse('profile'))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 401)

    def test_error_with_token(self) -> None:
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'vasya', 'password': 'promprog'}, format='json')
        # получаем токен
        token = resp.data['access']
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('access' in resp.data)
        # делаем get-запрос на профиль с помощью токена
        url = reverse('profile')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)


class LoginTest(TestCase):
    fixtures = ['profile_test_database.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)

    def test_error_with_token(self) -> None:
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'vasya', 'password': 'promprog'}, format='json')
        token = resp.data['access']
        url = reverse('login')
        resp = self.client.post(url, {'token': token}, format='json')
        self.assertEqual(resp.status_code, 200)


class OrdersListTest(APITestCase):
    fixtures = ['orders_list_test_database.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.page_name = 'orders'
        self.response = self.client.get(reverse(self.page_name))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 401)

    def test_error_with_token(self):
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'vasya', 'password': 'promprog'}, format='json')
        # получаем токен
        token = resp.data['access']
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('access' in resp.data)
        # делаем get-запрос на профиль с помощью токена
        url = reverse(self.page_name)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        resp = self.client.get(url, data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)

    def test_empty_data(self):
        self.assertEqual(len(Order.objects.all()), 0)


class PricesListTest(APITestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get(reverse('prices'))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 200)


class PortfolioTest(APITestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get(reverse('portfolio'))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 401)


class StocksListTest(APITestCase):
    fixtures = ['profile_test_database.json']

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get(reverse('stocks'))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_data_output(self) -> None:
        self.assertEqual(len(Stocks.objects.all()), 5)


class StockDetailTest(APITestCase):
    fixtures = ['profile_test_database.json']

    def setUp(self) -> None:
        self.client = Client()

    def test_error(self) -> None:
        for ind in range(1, len(Stocks.objects.all()) + 1):
            response = self.client.get(f'/api/v1/stocks/{ind}/')
            self.assertEqual(response.status_code, 200)

    def test_is_not_empty(self) -> None:
        for ind in range(1, len(Stocks.objects.all()) + 1):
            response = self.client.get(f'/api/v1/stocks/{ind}/')
            self.assertIsNotNone(response)

    def test_wrong_data(self) -> None:
        response = self.client.get('/api/v1/stock/qwe/')
        self.assertEqual(response.status_code, 404)


class BalanceAddTest(TestCase):
    fixtures = ['profile_test_database.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)
        self.verification_url = reverse('api_token')
        self.response = self.client.post(
            self.verification_url, {'username': 'vasya', 'password': 'promprog'},
            format='json'
        )
        self.token = self.response.data['access']
        self.url = reverse('balance_add')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_error(self) -> None:
        resp = self.client.get(self.url, data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)

    def test_letters(self) -> None:
        resp = self.client.post(self.url, data={'money': 'qwerty'})
        self.assertEqual(resp.status_code, 200)

    def test_numbers(self) -> None:
        resp = self.client.post(self.url, data={'money': 111})
        self.assertEqual(resp.status_code, 200)

    def test_float_numbers(self) -> None:
        resp = self.client.post(self.url, data={'money': 42.13})
        self.assertEqual(resp.status_code, 200)

    def test_negative_numbers(self) -> None:
        resp = self.client.post(self.url, data={'money': -12})
        self.assertEqual(resp.status_code, 200)


class OrderTest(APITestCase):
    fixtures = ['order_test_database.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user = User.objects.get(username='Flopper')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'Flopper', 'password': 'promprog'}, format='json')
        self.token = resp.data['access']

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 401)

    def test_add_order(self) -> None:
        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': True,
        })
        self.assertEqual(len(Order.objects.all()), 1)

    def test_portfolio_creation(self) -> None:
        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'TWTR',
            'price': 2,
            'amount': 4,
            'type': True,
        })
        self.assertEqual(len(Portfolio.objects.all()), 1)

    def test_portfolio_count(self) -> None:
        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': True,
        })
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'AAPL',
            'price': 2,
            'amount': 6,
            'type': True,
        })
        self.assertEqual(Portfolio.objects.get(pk=1).count, 0)

    def test_order_closing(self) -> None:
        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': False,
        })

        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user = User.objects.create(username='Floppers', password='promprog')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'Floppers', 'password': 'promprog'}, format='json')
        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': True,
        })
        self.assertEqual(len(Order.objects.all()), 2)

    def test_order_user_id(self) -> None:
        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user = User.objects.create(username='Flop', password='promprog')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'Flop', 'password': 'promprog'}, format='json')

        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': True,
        })

        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user = User.objects.create(username='Floppers', password='promprog')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'Floppers', 'password': 'promprog'}, format='json')
        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': True,
        })
        self.assertEqual(len(Order.objects.all()), 2)

    def test_balance_changes(self) -> None:
        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user1 = User.objects.create(username='Flopperus', balance=8, password='promprog')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'Flopperus', 'password': 'promprog'}, format='json')

        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': True,
        })

        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user2 = User.objects.create(username='Floppers', password='promprog', balance=0)
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'Floppers', 'password': 'promprog'}, format='json')
        url = reverse('add_order')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'price': 2,
            'amount': 4,
            'type': True,
        })
        self.assertEqual(self.user1.balance, 8)
        self.assertEqual(self.user2.balance, 0)


class LeverageTradingTest(APITestCase):
    fixtures = ['order_test_database.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user = User.objects.get(username='Flopper')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'Flopper', 'password': 'promprog'}, format='json')
        self.token = resp.data['access']
        self.quote = Quotes.objects.create(price=25, stock_id=1)

    def test_leverage_data_add(self) -> None:
        url = reverse('leverage_trading')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 42,
        })
        self.assertEqual(len(LeverageData.objects.all()), 1)

    def test_leverage_data_ratio(self) -> None:
        url = reverse('leverage_trading')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 42,
        })
        resp = self.client.get(url)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 13,
        })
        self.assertEqual(LeverageData.objects.get(pk=1).ratio, 13)

    def test_big_leverage_data_ratio(self) -> None:
        url = reverse('leverage_trading')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 10000000000,
        })
        resp = self.client.get(url)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 666,
        })
        self.assertEqual(LeverageData.objects.get(pk=1).ratio, 666)

    def test_negative_balance(self) -> None:
        self.client = APIClient()
        self.response = self.client.get(reverse('add_order'))
        self.user = User.objects.get(username='admin')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'admin', 'password': 'promprog'}, format='json')
        self.token = resp.data['access']
        url = reverse('leverage_trading')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 42,
        })
        self.assertEqual(len(LeverageData.objects.all()), 0)

    def test_only_one(self) -> None:
        url = reverse('leverage_trading')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 42,
        })
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 42,
        })
        self.assertEqual(len(LeverageData.objects.all()), 1)

    def test_one_per_stock(self) -> None:
        url = reverse('leverage_trading')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'OZON',
            'ratio': 42,
        })
        self.quote_two = Quotes.objects.create(price=25, stock_id=4)
        resp = self.client.post(url, data={
            'format': 'json',
            'stock': 'AAPL',
            'ratio': 42,
        })
        self.assertEqual(len(LeverageData.objects.all()), 2)
