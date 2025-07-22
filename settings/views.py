
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ProfileSettings
from .serializers import ProfileSettingsSerializer

# ProfileSettings APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all profile settings",
    operation_summary="Get all profile settings",
    tags=['Settings & Preferences'],
    responses={
        200: openapi.Response(
            description="Profile settings retrieved successfully",
            schema=ProfileSettingsSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "language": "en",
                        "currency": "INR",
                        "date_format": "DD/MM/YYYY",
                        "time_format": "12h",
                        "notifications_enabled": True,
                        "email_notifications": True,
                        "sms_notifications": False,
                        "dark_mode": False,
                        "auto_backup": True,
                        "created_at": "2025-01-15T10:00:00Z",
                        "updated_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def profilesettings_list(request):
    settings = ProfileSettings.objects.all()
    serializer = ProfileSettingsSerializer(settings, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create new profile settings for a user",
    operation_summary="Create profile settings",
    tags=['Settings & Preferences'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'language': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred language', enum=['en', 'hi', 'mr'], default='en'),
            'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Preferred currency', default='INR'),
            'date_format': openapi.Schema(type=openapi.TYPE_STRING, description='Date format preference', enum=['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY-MM-DD'], default='DD/MM/YYYY'),
            'time_format': openapi.Schema(type=openapi.TYPE_STRING, description='Time format preference', enum=['12h', '24h'], default='12h'),
            'notifications_enabled': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Enable notifications', default=True),
            'email_notifications': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Enable email notifications', default=True),
            'sms_notifications': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Enable SMS notifications', default=False),
            'dark_mode': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Enable dark mode', default=False),
            'auto_backup': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Enable automatic backup', default=True),
        },
        example={
            "user": 1,
            "language": "hi",
            "currency": "INR",
            "date_format": "DD/MM/YYYY",
            "time_format": "24h",
            "notifications_enabled": True,
            "email_notifications": True,
            "sms_notifications": True,
            "dark_mode": True,
            "auto_backup": True
        }
    ),
    responses={
        201: openapi.Response(description="Profile settings created successfully", schema=ProfileSettingsSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def profilesettings_create(request):
    serializer = ProfileSettingsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profilesettings_detail(request, pk):
    try:
        setting = ProfileSettings.objects.get(pk=pk)
    except ProfileSettings.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSettingsSerializer(setting)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def profilesettings_update(request, pk):
    try:
        setting = ProfileSettings.objects.get(pk=pk)
    except ProfileSettings.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSettingsSerializer(setting, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def profilesettings_delete(request, pk):
    try:
        setting = ProfileSettings.objects.get(pk=pk)
    except ProfileSettings.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    setting.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
