
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Customer, Udhari
from .serializers import CustomerSerializer, UdhariSerializer

# Customer APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all customers",
    operation_summary="Get all customers",
    tags=['Customers'],
    responses={
        200: openapi.Response(
            description="Customers retrieved successfully",
            schema=CustomerSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "business": 1,
                        "name": "Rajesh Kumar",
                        "phone": "9876543210",
                        "email": "rajesh.kumar@email.com",
                        "address": "123 Main Street, Mumbai",
                        "total_balance": "15000.00",
                        "credit_limit": "50000.00",
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def customer_list(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new customer",
    operation_summary="Create customer",
    tags=['Customers'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user', 'business', 'name', 'phone'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'business': openapi.Schema(type=openapi.TYPE_INTEGER, description='Business ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Customer name'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Customer phone number'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Customer email'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='Customer address'),
            'credit_limit': openapi.Schema(type=openapi.TYPE_NUMBER, description='Credit limit for customer', default=0),
        },
        example={
            "user": 1,
            "business": 1,
            "name": "Priya Sharma",
            "phone": "9123456789",
            "email": "priya.sharma@email.com",
            "address": "456 Park Avenue, Delhi",
            "credit_limit": "25000.00"
        }
    ),
    responses={
        201: openapi.Response(description="Customer created successfully", schema=CustomerSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def customer_create(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def customer_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def customer_delete(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    customer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Udhari APIs
@api_view(['GET'])
def udhari_list(request):
    udharis = Udhari.objects.all()
    serializer = UdhariSerializer(udharis, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def udhari_create(request):
    serializer = UdhariSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def udhari_detail(request, pk):
    try:
        udhari = Udhari.objects.get(pk=pk)
    except Udhari.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UdhariSerializer(udhari)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def udhari_update(request, pk):
    try:
        udhari = Udhari.objects.get(pk=pk)
    except Udhari.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UdhariSerializer(udhari, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def udhari_delete(request, pk):
    try:
        udhari = Udhari.objects.get(pk=pk)
    except Udhari.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    udhari.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
