from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.username

class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.ticker

class Transaction(models.Model):
    BUY = 'buy'
    SELL = 'sell'

    TRANSACTION_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    transaction_volume = models.IntegerField()
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.ticker} - {self.transaction_type}'
