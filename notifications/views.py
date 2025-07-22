
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Notification
from .serializers import NotificationSerializer

# Notification APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all notifications",
    operation_summary="Get all notifications",
    tags=['Notifications'],
    responses={
        200: openapi.Response(
            description="Notifications retrieved successfully",
            schema=NotificationSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "title": "Low Stock Alert",
                        "message": "iPhone 14 stock is running low (5 units left)",
                        "type": "stock_alert",
                        "is_read": False,
                        "action_url": "/stock/items/1/",
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def notification_list(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new notification",
    operation_summary="Create notification",
    tags=['Notifications'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user', 'title', 'message', 'type'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Notification title'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Notification message'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Notification type', enum=['info', 'warning', 'error', 'success', 'stock_alert', 'payment_due']),
            'action_url': openapi.Schema(type=openapi.TYPE_STRING, description='Action URL (optional)'),
        },
        example={
            "user": 1,
            "title": "Payment Received",
            "message": "₹5,000 payment received from customer Rajesh Kumar",
            "type": "success",
            "action_url": "/udhari/customers/1/"
        }
    ),
    responses={
        201: openapi.Response(description="Notification created successfully", schema=NotificationSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def notification_create(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def notification_detail(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def notification_update(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = NotificationSerializer(notification, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def notification_delete(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    notification.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
