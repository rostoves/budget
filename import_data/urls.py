from django.urls import path
from import_data import views

app_name = 'import_data'

urlpatterns = [
    path('', views.ImportCsvView.as_view(), name='import_csv'),
]
