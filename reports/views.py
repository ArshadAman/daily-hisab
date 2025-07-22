
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ReportExport
from .serializers import ReportExportSerializer

# ReportExport log APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all report export logs",
    operation_summary="Get all report export logs",
    tags=['Reports & Analytics'],
    responses={
        200: openapi.Response(
            description="Report export logs retrieved successfully",
            schema=ReportExportSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "report_type": "income_expense",
                        "export_format": "pdf",
                        "date_from": "2025-01-01",
                        "date_to": "2025-01-31",
                        "file_path": "/exports/income_expense_2025_01.pdf",
                        "status": "completed",
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def reportexport_list(request):
    exports = ReportExport.objects.all()
    serializer = ReportExportSerializer(exports, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new report export request",
    operation_summary="Request report export",
    tags=['Reports & Analytics'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user', 'report_type', 'export_format'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'report_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of report', enum=['income_expense', 'stock', 'udhari', 'summary']),
            'export_format': openapi.Schema(type=openapi.TYPE_STRING, description='Export format', enum=['pdf', 'excel', 'csv']),
            'date_from': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Start date for report'),
            'date_to': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='End date for report'),
        },
        example={
            "user": 1,
            "report_type": "income_expense",
            "export_format": "pdf",
            "date_from": "2025-01-01",
            "date_to": "2025-01-31"
        }
    ),
    responses={
        201: openapi.Response(description="Report export request created successfully", schema=ReportExportSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def reportexport_create(request):
    serializer = ReportExportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def reportexport_detail(request, pk):
    try:
        export = ReportExport.objects.get(pk=pk)
    except ReportExport.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ReportExportSerializer(export)
    return Response(serializer.data)

@api_view(['DELETE'])
def reportexport_delete(request, pk):
    try:
        export = ReportExport.objects.get(pk=pk)
    except ReportExport.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    export.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Placeholder for summary/statistics API (to be expanded as needed)
@api_view(['GET'])
def report_summary(request):
    # Example: return static summary, replace with real logic
    return Response({"summary": "Report summary endpoint. Implement logic as needed."})
