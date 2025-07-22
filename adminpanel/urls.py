from django.urls import path, include
from . import views

urlpatterns = [
    # AdminActivityLog endpoints
    path('activitylog/', views.activitylog_list, name='activitylog-list'),
    path('activitylog/create/', views.activitylog_create, name='activitylog-create'),
    path('activitylog/<int:pk>/', views.activitylog_detail, name='activitylog-detail'),
    path('activitylog/<int:pk>/delete/', views.activitylog_delete, name='activitylog-delete'),

    # AdminRole endpoints
    path('role/', views.adminrole_list, name='adminrole-list'),
    path('role/create/', views.adminrole_create, name='adminrole-create'),
    path('role/<int:pk>/', views.adminrole_detail, name='adminrole-detail'),
    path('role/<int:pk>/update/', views.adminrole_update, name='adminrole-update'),
    path('role/<int:pk>/delete/', views.adminrole_delete, name='adminrole-delete'),
]
