from celery import shared_task
from django.core.exceptions import ValidationError
from .models import Transaction, User, StockData

@shared_task
def process_transaction(transaction_data):
    try:
        user = User.objects.get(id=transaction_data['user'])
        stock_data = StockData.objects.get(ticker=transaction_data['ticker'])
        if transaction_data['transaction_type'] == 'buy':
            cost = stock_data.close_price * transaction_data['transaction_volume']
            if user.balance >= cost:
                user.balance -= cost
                user.save()
                transaction = Transaction.objects.create(
                    user=user,
                    ticker=stock_data.ticker,
                    transaction_type='buy',
                    transaction_volume=transaction_data['transaction_volume'],
                    transaction_price=stock_data.close_price,
                )
            else:
                raise ValidationError("Insufficient balance")
        else:
            transaction = Transaction.objects.create(
                user=user,
                ticker=stock_data.ticker,
                transaction_type='sell',
                transaction_volume=transaction_data['transaction_volume'],
                transaction_price=stock_data.close_price,
            )
        transaction.save()
    except Exception as e:
        raise e
