from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, StockData, Transaction

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        response = self.client.post('/users/', {'username': 'testuser', 'balance': 1000.00}, format='json')
        self.assertEqual(response.status_code, 201)

class StockDataTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_stock_data(self):
        response = self.client.post('/stocks/', {
            'ticker': 'AAPL',
            'open_price': 150.00,
            'close_price': 155.00,
            'high': 157.00,
            'low': 149.00,
            'volume': 100000,
            'timestamp': '2024-08-13T00:00:00Z'
        }, format='json')
        self.assertEqual(response.status_code, 201)

class TransactionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', balance=1000.00)
        self.stock_data = StockData.objects.create(
            ticker='AAPL',
            open_price=150.00,
            close_price=155.00,
            high=157.00,
            low=149.00,
            volume=100000,
            timestamp='2024-08-13T00:00:00Z'
        )

    def test_create_transaction(self):
        response = self.client.post('/transactions/', {
            'user': self.user.id,
            'ticker': self.stock_data.ticker,
            'transaction_type': 'buy',
            'transaction_volume': 5
        }, format='json')
        self.assertEqual(response.status_code, 201)
