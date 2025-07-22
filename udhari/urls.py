from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from . import views

urlpatterns = [
    # Customer endpoints
    path('customer/', views.customer_list, name='customer-list'),
    path('customer/create/', views.customer_create, name='customer-create'),
    path('customer/<int:pk>/', views.customer_detail, name='customer-detail'),
    path('customer/<int:pk>/update/', views.customer_update, name='customer-update'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer-delete'),

    # Udhari endpoints
    path('', views.udhari_list, name='udhari-list'),
    path('create/', views.udhari_create, name='udhari-create'),
    path('<int:pk>/', views.udhari_detail, name='udhari-detail'),
    path('<int:pk>/update/', views.udhari_update, name='udhari-update'),
    path('<int:pk>/delete/', views.udhari_delete, name='udhari-delete'),
]
