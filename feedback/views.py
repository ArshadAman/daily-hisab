
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import FeedbackTicket
from .serializers import FeedbackTicketSerializer

# FeedbackTicket APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all feedback tickets",
    operation_summary="Get all feedback tickets",
    tags=['Feedback & Support'],
    responses={
        200: openapi.Response(
            description="Feedback tickets retrieved successfully",
            schema=FeedbackTicketSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "subject": "Feature Request: Dark Mode",
                        "message": "Please add dark mode support to the app",
                        "type": "feature_request",
                        "priority": "medium",
                        "status": "open",
                        "admin_response": "",
                        "created_at": "2025-01-15T10:00:00Z",
                        "updated_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def feedbackticket_list(request):
    tickets = FeedbackTicket.objects.all()
    serializer = FeedbackTicketSerializer(tickets, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new feedback ticket",
    operation_summary="Submit feedback",
    tags=['Feedback & Support'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user', 'subject', 'message', 'type'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'subject': openapi.Schema(type=openapi.TYPE_STRING, description='Feedback subject'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Feedback message'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Feedback type', enum=['bug_report', 'feature_request', 'support', 'complaint', 'suggestion']),
            'priority': openapi.Schema(type=openapi.TYPE_STRING, description='Priority level', enum=['low', 'medium', 'high', 'critical'], default='medium'),
        },
        example={
            "user": 1,
            "subject": "Bug: Export not working",
            "message": "When I try to export reports to PDF, the app crashes",
            "type": "bug_report",
            "priority": "high"
        }
    ),
    responses={
        201: openapi.Response(description="Feedback ticket created successfully", schema=FeedbackTicketSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def feedbackticket_create(request):
    serializer = FeedbackTicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def feedbackticket_detail(request, pk):
    try:
        ticket = FeedbackTicket.objects.get(pk=pk)
    except FeedbackTicket.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = FeedbackTicketSerializer(ticket)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def feedbackticket_update(request, pk):
    try:
        ticket = FeedbackTicket.objects.get(pk=pk)
    except FeedbackTicket.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = FeedbackTicketSerializer(ticket, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def feedbackticket_delete(request, pk):
    try:
        ticket = FeedbackTicket.objects.get(pk=pk)
    except FeedbackTicket.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    ticket.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
