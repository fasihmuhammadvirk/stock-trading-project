from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AppUser, StockData, Transaction
from .serializers import AppUserSerializer, StockDataSerializer, TransactionSerializer
from django.core.cache import cache

class Greet(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "use /swagger to see API documentation"})

class AppUserViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, username=None):
        cache_key = f"user_{username}"
        user_data = cache.get(cache_key)
        if not user_data:
            try:
                user = AppUser.objects.get(username=username)
                serializer = AppUserSerializer(user)
                user_data = serializer.data
                cache.set(cache_key, user_data, timeout=300)  # Cache data for 5 minutes
            except AppUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(user_data)

class StockDataViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("all_stocks")
            cache.delete(f"stock_{serializer.data['ticker']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        cache_key = "all_stocks"
        stocks_data = cache.get(cache_key)
        if not stocks_data:
            stocks = StockData.objects.all()
            serializer = StockDataSerializer(stocks, many=True)
            stocks_data = serializer.data
            cache.set(cache_key, stocks_data, timeout=300)  # Cache data for 5 minutes
        return Response(stocks_data)

    def retrieve(self, request, ticker=None):
        cache_key = f"stock_{ticker}"
        stock_data = cache.get(cache_key)
        if not stock_data:
            try:
                stock = StockData.objects.get(ticker=ticker)
                serializer = StockDataSerializer(stock)
                stock_data = serializer.data
                cache.set(cache_key, stock_data, timeout=300)  # Cache data for 5 minutes
            except StockData.DoesNotExist:
                return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(stock_data)

class TransactionViewSet(viewsets.ViewSet):

    def create(self, request):
        user_id = request.data.get('user_id')
        ticker = request.data.get('ticker')
        transaction_type = request.data.get('transaction_type')
        transaction_volume = int(request.data.get('transaction_volume'))

        try:
            user = AppUser.objects.get(user_id=user_id)
            stock = StockData.objects.get(ticker=ticker)

            transaction_price = stock.close_price * transaction_volume

            if transaction_type == 'buy' and user.balance < transaction_price:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

            if transaction_type == 'buy':
                user.balance -= transaction_price
            elif transaction_type == 'sell':
                user.balance += transaction_price

            user.save()

            transaction = Transaction.objects.create(
                user=user,
                ticker=ticker,
                transaction_type=transaction_type,
                transaction_volume=transaction_volume,
                transaction_price=transaction_price
            )

            # Invalidate relevant cache entries
            cache.delete(f"transactions_{user_id}")

            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except StockData.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, user_id=None):
        cache_key = f"transactions_{user_id}"
        transactions_data = cache.get(cache_key)
        if not transactions_data:
            transactions = Transaction.objects.filter(user_id=user_id)
            serializer = TransactionSerializer(transactions, many=True)
            transactions_data = serializer.data
            cache.set(cache_key, transactions_data, timeout=300)  # Cache data for 5 minutes
        return Response(transactions_data)

    def retrieve(self, request, user_id=None, start_timestamp=None, end_timestamp=None):
        cache_key = f"transactions_{user_id}_{start_timestamp}_{end_timestamp}"
        transactions_data = cache.get(cache_key)
        if not transactions_data:
            transactions = Transaction.objects.filter(
                user_id=user_id,
                timestamp__gte=start_timestamp,
                timestamp__lte=end_timestamp
            )
            serializer = TransactionSerializer(transactions, many=True)
            transactions_data = serializer.data
            cache.set(cache_key, transactions_data, timeout=300)  # Cache data for 5 minutes
        return Response(transactions_data)
