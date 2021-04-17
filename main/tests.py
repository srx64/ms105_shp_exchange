from django.test import TestCase, Client
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from main.models import User, Stocks


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
    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get(reverse('orders'))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 200)


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
        self.assertEqual(self.response.status_code, 200)


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
            response = self.client.get(f'/api/v1/stock/{ind}/')
            self.assertEqual(response.status_code, 200)

    def test_is_not_empty(self) -> None:
        for ind in range(1, len(Stocks.objects.all()) + 1):
            response = self.client.get(f'/api/v1/stock/{ind}/')
            self.assertIsNotNone(response)

    def test_wrong_data(self) -> None:
        response = self.client.get('/api/v1/stock/qwe/')
        self.assertEqual(response.status_code, 404)
