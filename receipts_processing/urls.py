from django.urls import path, include

from . import views

urlpatterns = [
    path('receipts/new', views.new, name='new'),
    path('receipts/<int:id>/delete', views.delete, name='receipt-delete'),
    path('receipts/<int:id>/file/download',
         views.download, name='receipt-download'),
    path('receipts/<int:id>/file/view', views.view_file, name='receipt-view'),
    path('receipts/<int:id>', views.receipt_details, name='receipt-details'),
    path('signup', views.sign_up, name='signup'),
    path('', views.receipts, name='receipts'),
    path('', include('django.contrib.auth.urls'))

]
