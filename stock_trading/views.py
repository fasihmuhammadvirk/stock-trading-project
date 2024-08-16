from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import User, StockData, Transaction
from .serializers import UserSerializer, StockDataSerializer, TransactionSerializer
from .tasks import process_transaction
from rest_framework.generics import GenericAPIView

class SayHello(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])
    def hello(self, request):
        return Response({"message": "Use /Swagger to User API Documentation."}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def retrieve_user(self, request, pk=None):
        user = cache.get(f'user_{pk}')
        if not user:
            user = get_object_or_404(User, pk=pk)
            cache.set(f'user_{pk}', user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class StockDataViewSet(viewsets.ModelViewSet):
    queryset = StockData.objects.all()
    serializer_class = StockDataSerializer

    @action(detail=True, methods=['get'])
    def retrieve_stock(self, request, pk=None):
        stock_data = cache.get(f'stock_{pk}')
        if not stock_data:
            stock_data = get_object_or_404(StockData, pk=pk)
            cache.set(f'stock_{pk}', stock_data)
        serializer = StockDataSerializer(stock_data)
        return Response(serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        process_transaction.delay(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='user-transactions')
    def retrieve_user_transactions(self, request, pk=None):
        transactions = Transaction.objects.filter(user_id=pk)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='user-transactions-range')
    def retrieve_user_transactions_range(self, request, pk=None):
        start_timestamp = request.query_params.get('start_timestamp')
        end_timestamp = request.query_params.get('end_timestamp')
        transactions = Transaction.objects.filter(user_id=pk, timestamp__range=[start_timestamp, end_timestamp])
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
