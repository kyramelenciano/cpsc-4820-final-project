from django.urls import path

from . import views

urlpatterns = [
    path('receipts', views.receipts, name='receipts'),
    path('', views.home, name='home')
]
