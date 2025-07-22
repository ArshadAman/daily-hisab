from django.urls import path, include
from . import views

urlpatterns = [
    path('ticket/', views.feedbackticket_list, name='feedbackticket-list'),
    path('ticket/create/', views.feedbackticket_create, name='feedbackticket-create'),
    path('ticket/<int:pk>/', views.feedbackticket_detail, name='feedbackticket-detail'),
    path('ticket/<int:pk>/update/', views.feedbackticket_update, name='feedbackticket-update'),
    path('ticket/<int:pk>/delete/', views.feedbackticket_delete, name='feedbackticket-delete'),
]
