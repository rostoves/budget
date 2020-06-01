from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('balance_check/', views.BalanceCheck.as_view(), name='balance_check'),
    path('balance/', views.BalanceView.as_view(), name='balance'),
    path('balance_demo/', views.myFirstChart, name='balance_demo'),
]
