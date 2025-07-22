from django.urls import path
from . import views

urlpatterns = [
    # User endpoints
    path('', views.user_list, name='user-list'),
    path('create/', views.user_create, name='user-create'),
    path('<int:pk>/', views.user_detail, name='user-detail'),
    path('<int:pk>/update/', views.user_update, name='user-update'),
    path('<int:pk>/delete/', views.user_delete, name='user-delete'),
    
    # Business endpoints
    path('business/', views.business_list, name='business-list'),
    path('business/create/', views.business_create, name='business-create'),
    path('business/<int:pk>/', views.business_detail, name='business-detail'),
    path('business/<int:pk>/update/', views.business_update, name='business-update'),
    path('business/<int:pk>/delete/', views.business_delete, name='business-delete'),
]
