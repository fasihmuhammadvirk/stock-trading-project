import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from .models import AppUser, StockData, Transaction

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    return AppUser.objects.create(username='testuser', balance=1000.00)

@pytest.fixture
def create_stock():
    return StockData.objects.create(
        ticker='AAPL',
        open_price=145.00,
        close_price=150.00,
        high=155.00,
        low=140.00,
        volume=1000000,
        timestamp="2023-08-17T14:00:00Z"
    )

@pytest.mark.django_db
def test_create_user(api_client):
    url = reverse('app-user-list')
    data = {'username': 'newuser', 'balance': 500.00}
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['username'] == 'newuser'

@pytest.mark.django_db
def test_get_user(api_client, create_user):
    url = reverse('app-user-detail', kwargs={'username': create_user.username})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == 'testuser'

@pytest.mark.django_db
def test_create_stock(api_client):
    url = reverse('stock-list')
    data = {
        'ticker': 'GOOGL',
        'open_price': 2700.00,
        'close_price': 2750.00,
        'high': 2800.00,
        'low': 2650.00,
        'volume': 1500000,
        'timestamp': "2023-08-17T14:00:00Z"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['ticker'] == 'GOOGL'

@pytest.mark.django_db
def test_get_stock(api_client, create_stock):
    url = reverse('stock-detail', kwargs={'ticker': create_stock.ticker})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['ticker'] == 'AAPL'

@pytest.mark.django_db
def test_create_transaction(api_client, create_user, create_stock):
    url = reverse('transaction-list')
    data = {
        'user_id': create_user.user_id,
        'ticker': create_stock.ticker,
        'transaction_type': 'buy',
        'transaction_volume': 2
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['transaction_price'] == 300.00

@pytest.mark.django_db
def test_get_transactions(api_client, create_user, create_stock):
    # Create a transaction first
    Transaction.objects.create(
        user=create_user,
        ticker=create_stock.ticker,
        transaction_type='buy',
        transaction_volume=2,
        transaction_price=300.00
    )
    
    url = reverse('transaction-user-list', kwargs={'user_id': create_user.user_id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['ticker'] == create_stock.ticker

@pytest.mark.django_db
def test_get_transactions_in_date_range(api_client, create_user, create_stock):
    # Create a transaction first
    Transaction.objects.create(
        user=create_user,
        ticker=create_stock.ticker,
        transaction_type='buy',
        transaction_volume=2,
        transaction_price=300.00
    )
    
    start_timestamp = "2023-08-17T00:00:00Z"
    end_timestamp = "2023-08-18T00:00:00Z"
    
    url = reverse('transaction-detail', kwargs={
        'user_id': create_user.user_id,
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp
    })
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['ticker'] == create_stock.ticker
