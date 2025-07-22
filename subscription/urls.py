from django.urls import path, include
from . import views

urlpatterns = [
    # Plan endpoints
    path('plan/', views.plan_list, name='plan-list'),
    path('plan/create/', views.plan_create, name='plan-create'),
    path('plan/<int:pk>/', views.plan_detail, name='plan-detail'),
    path('plan/<int:pk>/update/', views.plan_update, name='plan-update'),
    path('plan/<int:pk>/delete/', views.plan_delete, name='plan-delete'),

    # Subscription endpoints
    path('subscription/', views.subscription_list, name='subscription-list'),
    path('subscription/create/', views.subscription_create, name='subscription-create'),
    path('subscription/<int:pk>/', views.subscription_detail, name='subscription-detail'),
    path('subscription/<int:pk>/update/', views.subscription_update, name='subscription-update'),
    path('subscription/<int:pk>/delete/', views.subscription_delete, name='subscription-delete'),

    # Coupon endpoints
    path('coupon/', views.coupon_list, name='coupon-list'),
    path('coupon/create/', views.coupon_create, name='coupon-create'),
    path('coupon/<int:pk>/', views.coupon_detail, name='coupon-detail'),
    path('coupon/<int:pk>/update/', views.coupon_update, name='coupon-update'),
    path('coupon/<int:pk>/delete/', views.coupon_delete, name='coupon-delete'),
]
