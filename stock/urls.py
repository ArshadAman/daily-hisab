from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from . import views

urlpatterns = [
    # StockItem endpoints
    path('item/', views.stockitem_list, name='stockitem-list'),
    path('item/create/', views.stockitem_create, name='stockitem-create'),
    path('item/<int:pk>/', views.stockitem_detail, name='stockitem-detail'),
    path('item/<int:pk>/update/', views.stockitem_update, name='stockitem-update'),
    path('item/<int:pk>/delete/', views.stockitem_delete, name='stockitem-delete'),

    # StockTransaction endpoints
    path('transaction/', views.stocktransaction_list, name='stocktransaction-list'),
    path('transaction/create/', views.stocktransaction_create, name='stocktransaction-create'),
    path('transaction/<int:pk>/', views.stocktransaction_detail, name='stocktransaction-detail'),
    path('transaction/<int:pk>/update/', views.stocktransaction_update, name='stocktransaction-update'),
    path('transaction/<int:pk>/delete/', views.stocktransaction_delete, name='stocktransaction-delete'),
]
