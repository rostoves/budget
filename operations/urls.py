from django.urls import path
from operations import views

app_name = 'operations'

urlpatterns = [
    path('', views.OperationListView.as_view(), name='operations'),
]
