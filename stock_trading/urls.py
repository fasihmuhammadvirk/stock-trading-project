from django.urls import path
from .views import AppUserViewSet, StockDataViewSet, TransactionViewSet, Greet

app_user_list = AppUserViewSet.as_view({
    'post': 'create'
})

app_user_detail = AppUserViewSet.as_view({
    'get': 'retrieve'
})

stock_list = StockDataViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

stock_detail = StockDataViewSet.as_view({
    'get': 'retrieve'
})

transaction_list = TransactionViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

transaction_detail = TransactionViewSet.as_view({
    'get': 'retrieve'
})

greet = Greet.as_view({'get': 'list'})

urlpatterns = [
    path('',greet, name='greet'),
    path('users/', app_user_list, name='app-user-list'),
    path('users/<str:username>/', app_user_detail, name='app-user-detail'),
    path('stocks/', stock_list, name='stock-list'),
    path('stocks/<str:ticker>/', stock_detail, name='stock-detail'),
    path('transactions/', transaction_list, name='transaction-list'),
    path('transactions/<int:user_id>/', transaction_list, name='transaction-user-list'),
    path('transactions/<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/', transaction_detail, name='transaction-detail'),
]
