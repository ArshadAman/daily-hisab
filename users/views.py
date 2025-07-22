
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Business
from .serializers import UserSerializer, BusinessSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all users in the system",
    operation_summary="Get all users",
    tags=['Users'],
    responses={
        200: openapi.Response(
            description="List of users retrieved successfully",
            schema=UserSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "phone": "+1234567890",
                        "language": "en",
                        "business": {
                            "id": 1,
                            "name": "John's Shop",
                            "type": "retail"
                        },
                        "is_premium": False,
                        "referral_code": "JOHN123",
                        "referred_by": None,
                        "app_locked": False,
                        "health_score": 95,
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_active": True
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve details of a specific user by their ID",
    operation_summary="Get user by ID",
    tags=['Users'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="User ID",
            type=openapi.TYPE_INTEGER,
            required=True,
            example=1
        )
    ],
    responses={
        200: openapi.Response(
            description="User details retrieved successfully",
            schema=UserSerializer(),
            examples={
                "application/json": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "language": "en",
                    "business": {
                        "id": 1,
                        "name": "John's Shop",
                        "type": "retail"
                    },
                    "is_premium": False,
                    "referral_code": "JOHN123",
                    "referred_by": None,
                    "app_locked": False,
                    "health_score": 95,
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True
                }
            }
        ),
        404: openapi.Response(
            description="User not found",
            examples={
                "application/json": {
                    "detail": "Not found."
                }
            }
        )
    }
)
@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new user account with all required information",
    operation_summary="Create new user",
    tags=['Users'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Unique username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
            'language': openapi.Schema(type=openapi.TYPE_STRING, description='Language preference', enum=['en', 'hi', 'mr']),
            'business_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Business ID to associate with'),
            'referral_code': openapi.Schema(type=openapi.TYPE_STRING, description='User referral code'),
            'referred_by': openapi.Schema(type=openapi.TYPE_STRING, description='Referrer code'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
        },
        example={
            "username": "john_doe",
            "password": "securepassword123",
            "email": "john@example.com",
            "phone": "+1234567890",
            "language": "en",
            "business_id": 1,
            "referral_code": "JOHN123",
            "first_name": "John",
            "last_name": "Doe"
        }
    ),
    responses={
        201: openapi.Response(
            description="User created successfully",
            schema=UserSerializer(),
            examples={
                "application/json": {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "language": "en",
                    "business": {
                        "id": 1,
                        "name": "John's Shop",
                        "type": "retail"
                    },
                    "is_premium": False,
                    "referral_code": "JOHN123",
                    "referred_by": None,
                    "app_locked": False,
                    "health_score": 100,
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True
                }
            }
        ),
        400: openapi.Response(
            description="Invalid data provided",
            examples={
                "application/json": {
                    "username": ["This field is required."],
                    "password": ["This field is required."]
                }
            }
        )
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email'),
            password=request.data.get('password'),
            phone=serializer.validated_data.get('phone'),
            language=serializer.validated_data.get('language', 'en'),
            is_premium=serializer.validated_data.get('is_premium', False),
            referral_code=serializer.validated_data.get('referral_code'),
            referred_by=serializer.validated_data.get('referred_by'),
            app_locked=serializer.validated_data.get('app_locked', False),
            health_score=serializer.validated_data.get('health_score', 100),
            notes=serializer.validated_data.get('notes'),
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='put',
    operation_description="Update user details completely (all fields required)",
    operation_summary="Update user (PUT)",
    tags=['Users'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="User ID",
            type=openapi.TYPE_INTEGER,
            required=True,
            example=1
        )
    ],
    request_body=UserSerializer,
    responses={
        200: openapi.Response(description="User updated successfully", schema=UserSerializer()),
        400: openapi.Response(description="Invalid data provided"),
        404: openapi.Response(description="User not found")
    }
)
@swagger_auto_schema(
    method='patch',
    operation_description="Partially update user details (only specified fields)",
    operation_summary="Update user (PATCH)",
    tags=['Users'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="User ID",
            type=openapi.TYPE_INTEGER,
            required=True,
            example=1
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
            'language': openapi.Schema(type=openapi.TYPE_STRING, description='Language preference', enum=['en', 'hi', 'mr']),
            'is_premium': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Premium status'),
            'app_locked': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='App lock status'),
            'health_score': openapi.Schema(type=openapi.TYPE_INTEGER, description='Health score (0-100)'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Admin notes'),
        },
        example={
            "email": "newemail@example.com",
            "language": "hi",
            "is_premium": True
        }
    ),
    responses={
        200: openapi.Response(description="User updated successfully", schema=UserSerializer()),
        400: openapi.Response(description="Invalid data provided"),
        404: openapi.Response(description="User not found")
    }
)
@api_view(['PUT', 'PATCH'])
def user_update(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='delete',
    operation_description="Delete a user permanently from the system",
    operation_summary="Delete user",
    tags=['Users'],
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="User ID",
            type=openapi.TYPE_INTEGER,
            required=True,
            example=1
        )
    ],
    responses={
        204: openapi.Response(description="User deleted successfully"),
        404: openapi.Response(description="User not found")
    }
)
@api_view(['DELETE'])
def user_delete(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Business APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all businesses",
    operation_summary="Get all businesses",
    tags=['Business'],
    responses={
        200: openapi.Response(
            description="List of businesses retrieved successfully",
            schema=BusinessSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "John's Shop",
                        "type": "retail",
                        "owner": 1,
                        "created_at": "2025-01-15T10:30:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def business_list(request):
    businesses = Business.objects.all()
    serializer = BusinessSerializer(businesses, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new business entity",
    operation_summary="Create new business",
    tags=['Business'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'owner'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Business name'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Business type (e.g., retail, service)'),
            'owner': openapi.Schema(type=openapi.TYPE_INTEGER, description='Owner user ID'),
        },
        example={
            "name": "John's Electronics Store",
            "type": "retail",
            "owner": 1
        }
    ),
    responses={
        201: openapi.Response(description="Business created successfully", schema=BusinessSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def business_create(request):
    serializer = BusinessSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def business_detail(request, pk):
    try:
        business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BusinessSerializer(business)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def business_update(request, pk):
    try:
        business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BusinessSerializer(business, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def business_delete(request, pk):
    try:
        business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    business.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
