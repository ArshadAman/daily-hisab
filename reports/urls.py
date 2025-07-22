from django.urls import path, include
from . import views

urlpatterns = [
    # ReportExport log endpoints
    path('export/', views.reportexport_list, name='reportexport-list'),
    path('export/create/', views.reportexport_create, name='reportexport-create'),
    path('export/<int:pk>/', views.reportexport_detail, name='reportexport-detail'),
    path('export/<int:pk>/delete/', views.reportexport_delete, name='reportexport-delete'),

    # Report summary/statistics endpoint
    path('summary/', views.report_summary, name='report-summary'),
]
