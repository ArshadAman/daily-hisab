from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from . import views

urlpatterns = [
    # Category endpoints
    path('category/', views.category_list, name='category-list'),
    path('category/create/', views.category_create, name='category-create'),
    path('category/<int:pk>/', views.category_detail, name='category-detail'),
    path('category/<int:pk>/update/', views.category_update, name='category-update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category-delete'),

    # IncomeExpense endpoints
    path('', views.income_expense_list, name='income-expense-list'),
    path('create/', views.income_expense_create, name='income-expense-create'),
    path('<int:pk>/', views.income_expense_detail, name='income-expense-detail'),
    path('<int:pk>/update/', views.income_expense_update, name='income-expense-update'),
    path('<int:pk>/delete/', views.income_expense_delete, name='income-expense-delete'),
]
