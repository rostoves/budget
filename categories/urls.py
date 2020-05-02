from django.urls import path
from categories import views

app_name = 'categories'

urlpatterns = [
    path('types/', views.TypeListView.as_view(), name='types'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('mcc/', views.MerchantCodeListView.as_view(), name='mcc'),
    path('descriptions/', views.DescriptionListView.as_view(), name='descriptions'),
]
