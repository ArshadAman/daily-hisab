
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AdminActivityLog, AdminRole
from .serializers import AdminActivityLogSerializer, AdminRoleSerializer

# AdminActivityLog APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all admin activity logs",
    operation_summary="Get all admin activity logs",
    tags=['Admin Panel'],
    responses={
        200: openapi.Response(
            description="Admin activity logs retrieved successfully",
            schema=AdminActivityLogSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "admin_user": 1,
                        "action": "user_updated",
                        "target_user": 5,
                        "details": "Updated user profile information",
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0...",
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def activitylog_list(request):
    logs = AdminActivityLog.objects.all()
    serializer = AdminActivityLogSerializer(logs, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new admin activity log entry",
    operation_summary="Log admin activity",
    tags=['Admin Panel'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['admin_user', 'action'],
        properties={
            'admin_user': openapi.Schema(type=openapi.TYPE_INTEGER, description='Admin user ID'),
            'action': openapi.Schema(type=openapi.TYPE_STRING, description='Action performed'),
            'target_user': openapi.Schema(type=openapi.TYPE_INTEGER, description='Target user ID (if applicable)'),
            'details': openapi.Schema(type=openapi.TYPE_STRING, description='Activity details'),
            'ip_address': openapi.Schema(type=openapi.TYPE_STRING, description='IP address'),
            'user_agent': openapi.Schema(type=openapi.TYPE_STRING, description='User agent string'),
        },
        example={
            "admin_user": 1,
            "action": "user_suspended",
            "target_user": 15,
            "details": "User suspended for violating terms",
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    ),
    responses={
        201: openapi.Response(description="Admin activity logged successfully", schema=AdminActivityLogSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def activitylog_create(request):
    serializer = AdminActivityLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def activitylog_detail(request, pk):
    try:
        log = AdminActivityLog.objects.get(pk=pk)
    except AdminActivityLog.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AdminActivityLogSerializer(log)
    return Response(serializer.data)

@api_view(['DELETE'])
def activitylog_delete(request, pk):
    try:
        log = AdminActivityLog.objects.get(pk=pk)
    except AdminActivityLog.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    log.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# AdminRole APIs
@api_view(['GET'])
def adminrole_list(request):
    roles = AdminRole.objects.all()
    serializer = AdminRoleSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def adminrole_create(request):
    serializer = AdminRoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def adminrole_detail(request, pk):
    try:
        role = AdminRole.objects.get(pk=pk)
    except AdminRole.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AdminRoleSerializer(role)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def adminrole_update(request, pk):
    try:
        role = AdminRole.objects.get(pk=pk)
    except AdminRole.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AdminRoleSerializer(role, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def adminrole_delete(request, pk):
    try:
        role = AdminRole.objects.get(pk=pk)
    except AdminRole.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    role.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
