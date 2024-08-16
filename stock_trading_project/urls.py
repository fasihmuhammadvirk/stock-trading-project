
from django.urls import path
from stock_trading import views
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Docs",
      default_version='v1',
      description="Stock Trading",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path ('', views.SayHello.as_view({'get': 'hello'}), name='index'),
    path('stocks/', views.StockDataViewSet.as_view({'get': 'list'}), name='StockDataViewSet'),
    path('transactions/', views.TransactionViewSet.as_view({'get': 'list'}), name='TransactionViewSet'),
    path('users/', views.UserViewSet.as_view({'get': 'list'}), name='UserViewSet'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

