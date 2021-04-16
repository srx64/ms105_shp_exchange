from django.test import TestCase, Client
from rest_framework.test import APITestCase
from django.urls import reverse


class ProfileTest(TestCase):
    fixtures = ['profile_test_database.json']

    def setUp(self) -> None:
        self.client = Client()
        self.response = self.client.get(reverse('profile'))

    def test_error(self) -> None:
        self.assertEqual(self.response.status_code, 401)


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
