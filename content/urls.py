from django.urls import path, include
from . import views

urlpatterns = [
    # Banner endpoints
    path('banner/', views.banner_list, name='banner-list'),
    path('banner/create/', views.banner_create, name='banner-create'),
    path('banner/<int:pk>/', views.banner_detail, name='banner-detail'),
    path('banner/<int:pk>/update/', views.banner_update, name='banner-update'),
    path('banner/<int:pk>/delete/', views.banner_delete, name='banner-delete'),

    # Tutorial endpoints
    path('tutorial/', views.tutorial_list, name='tutorial-list'),
    path('tutorial/create/', views.tutorial_create, name='tutorial-create'),
    path('tutorial/<int:pk>/', views.tutorial_detail, name='tutorial-detail'),
    path('tutorial/<int:pk>/update/', views.tutorial_update, name='tutorial-update'),
    path('tutorial/<int:pk>/delete/', views.tutorial_delete, name='tutorial-delete'),
]
