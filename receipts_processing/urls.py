from django.urls import path

from . import views

urlpatterns = [
    path('receipts/new', views.index, name='index'),
    path('receipts/<int:id>/delete', views.delete, name='receipt-delete'),
    path('receipts/<int:id>/file/download', views.download, name='receipt-download'),
    path('receipts/<int:id>/file/view', views.view_file, name='receipt-view'),
    path('receipts/<int:id>', views.receipt_details, name='receipt-details'),
    path('receipts', views.receipts, name='receipts'),
    path('', views.home, name='home')
]
