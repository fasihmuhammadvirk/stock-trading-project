from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import AppUser, StockData, Transaction
from .serializers import AppUserSerializer, StockDataSerializer, TransactionSerializer

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
        try:
            user = AppUser.objects.get(username=username)
            serializer = AppUserSerializer(user)
            return Response(serializer.data)
        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class StockDataViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        stocks = StockData.objects.all()
        serializer = StockDataSerializer(stocks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, ticker=None):
        try:
            stock = StockData.objects.get(ticker=ticker)
            serializer = StockDataSerializer(stock)
            return Response(serializer.data)
        except StockData.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

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

            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except AppUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except StockData.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, user_id=None):
        transactions = Transaction.objects.filter(user_id=user_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, user_id=None, start_timestamp=None, end_timestamp=None):
        transactions = Transaction.objects.filter(
            user_id=user_id,
            timestamp__gte=start_timestamp,
            timestamp__lte=end_timestamp
        )
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
