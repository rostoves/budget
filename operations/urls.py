from django.urls import path
from operations import views

app_name = 'operations'

urlpatterns = [
    path('', views.OperationsView.as_view(), name='operations'),
]
