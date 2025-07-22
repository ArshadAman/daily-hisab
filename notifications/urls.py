from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification-list'),
    path('create/', views.notification_create, name='notification-create'),
    path('<int:pk>/', views.notification_detail, name='notification-detail'),
    path('<int:pk>/update/', views.notification_update, name='notification-update'),
    path('<int:pk>/delete/', views.notification_delete, name='notification-delete'),
]
