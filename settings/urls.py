from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.profilesettings_list, name='profilesettings-list'),
    path('profile/create/', views.profilesettings_create, name='profilesettings-create'),
    path('profile/<int:pk>/', views.profilesettings_detail, name='profilesettings-detail'),
    path('profile/<int:pk>/update/', views.profilesettings_update, name='profilesettings-update'),
    path('profile/<int:pk>/delete/', views.profilesettings_delete, name='profilesettings-delete'),
]
