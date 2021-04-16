from django.test import TestCase, Client
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from main.models import User


class ProfileTest(APITestCase):
    fixtures = ['profile_test_database.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.response = self.client.get(reverse('profile'))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 401)

    def test_error_with_token(self):
        self.user = User.objects.get(username='vasya')
        self.client.force_login(user=self.user)
        verification_url = reverse('api_token')
        resp = self.client.post(verification_url, {'username': 'vasya', 'password': 'promprog'}, format='json')
        token = resp.data['access']
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('access' in resp.data)

        url = reverse('profile')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        resp = self.client.get(url, data={'format': 'json'})
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
