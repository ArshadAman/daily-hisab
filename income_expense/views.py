
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Category, IncomeExpense
from .serializers import CategorySerializer, IncomeExpenseSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Category APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all income/expense categories",
    operation_summary="Get all categories",
    tags=['Categories'],
    responses={
        200: openapi.Response(
            description="Categories retrieved successfully",
            schema=CategorySerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Food & Beverages",
                        "type": "expense",
                        "business": 1,
                        "default": True
                    },
                    {
                        "id": 2,
                        "name": "Sales Revenue",
                        "type": "income",
                        "business": 1,
                        "default": False
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new category for income or expense tracking",
    operation_summary="Create new category",
    tags=['Categories'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'type', 'business'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category name'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Category type', enum=['income', 'expense']),
            'business': openapi.Schema(type=openapi.TYPE_INTEGER, description='Business ID'),
            'default': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is default category'),
        },
        example={
            "name": "Transportation",
            "type": "expense", 
            "business": 1,
            "default": False
        }
    ),
    responses={
        201: openapi.Response(description="Category created successfully", schema=CategorySerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# IncomeExpense APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all income and expense entries",
    operation_summary="Get all income/expense entries",
    tags=['Income & Expense'],
    responses={
        200: openapi.Response(
            description="Income/expense entries retrieved successfully",
            schema=IncomeExpenseSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "business": 1,
                        "amount": "500.00",
                        "type": "expense",
                        "category": {
                            "id": 1,
                            "name": "Food & Beverages",
                            "type": "expense"
                        },
                        "date": "2025-01-15",
                        "time": "14:30:00",
                        "payment_mode": "cash",
                        "notes": "Lunch expenses",
                        "voice_entry": False,
                        "created_at": "2025-01-15T14:30:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def income_expense_list(request):
    entries = IncomeExpense.objects.all()
    serializer = IncomeExpenseSerializer(entries, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new income or expense entry",
    operation_summary="Create income/expense entry",
    tags=['Income & Expense'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user', 'business', 'amount', 'type', 'date'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'business': openapi.Schema(type=openapi.TYPE_INTEGER, description='Business ID'),
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount (decimal)'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Entry type', enum=['income', 'expense']),
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Entry date (YYYY-MM-DD)'),
            'time': openapi.Schema(type=openapi.TYPE_STRING,  description='Entry time (HH:MM:SS)'),
            'payment_mode': openapi.Schema(type=openapi.TYPE_STRING, description='Payment method (cash, card, upi, etc.)'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Additional notes'),
            'voice_entry': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Was this entered via voice?'),
        },
        example={
            "user": 1,
            "business": 1,
            "amount": "1500.00",
            "type": "income",
            "category_id": 2,
            "date": "2025-01-15",
            "time": "10:30:00",
            "payment_mode": "upi",
            "notes": "Product sale",
            "voice_entry": False
        }
    ),
    responses={
        201: openapi.Response(description="Entry created successfully", schema=IncomeExpenseSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def income_expense_create(request):
    serializer = IncomeExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a specific income/expense entry by ID",
    operation_summary="Get income/expense entry details",
    tags=['Income & Expense'],
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="Income/expense entry ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Entry retrieved successfully",
            schema=IncomeExpenseSerializer(),
            examples={
                "application/json": {
                    "id": 1,
                    "user": 1,
                    "business": 1,
                    "amount": "500.00",
                    "type": "expense",
                    "category": {
                        "id": 1,
                        "name": "Food & Beverages",
                        "type": "expense"
                    },
                    "date": "2025-01-15",
                    "time": "14:30:00",
                    "payment_mode": "cash",
                    "notes": "Lunch expenses",
                    "voice_entry": False,
                    "created_at": "2025-01-15T14:30:00Z"
                }
            }
        ),
        404: openapi.Response(description="Entry not found")
    }
)
@api_view(['GET'])
def income_expense_detail(request, pk):
    try:
        entry = IncomeExpense.objects.get(pk=pk)
    except IncomeExpense.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = IncomeExpenseSerializer(entry)
    return Response(serializer.data)

@swagger_auto_schema(
    method='put',
    operation_description="Update an existing income/expense entry",
    operation_summary="Update income/expense entry",
    tags=['Income & Expense'],
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="Income/expense entry ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount (decimal)'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Entry type', enum=['income', 'expense']),
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Entry date (YYYY-MM-DD)'),
            'time': openapi.Schema(type=openapi.TYPE_STRING,  description='Entry time (HH:MM:SS)'),
            'payment_mode': openapi.Schema(type=openapi.TYPE_STRING, description='Payment method'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Additional notes'),
            'voice_entry': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Was this entered via voice?'),
        },
        example={
            "amount": "750.00",
            "type": "expense",
            "category_id": 1,
            "date": "2025-01-15",
            "time": "15:30:00",
            "payment_mode": "card",
            "notes": "Updated lunch expense",
            "voice_entry": False
        }
    ),
    responses={
        200: openapi.Response(description="Entry updated successfully", schema=IncomeExpenseSerializer()),
        400: openapi.Response(description="Invalid data provided"),
        404: openapi.Response(description="Entry not found")
    }
)
@swagger_auto_schema(
    method='patch',
    operation_description="Partially update an existing income/expense entry",
    operation_summary="Partially update income/expense entry",
    tags=['Income & Expense'],
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="Income/expense entry ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount (decimal)'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Entry type', enum=['income', 'expense']),
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Entry date (YYYY-MM-DD)'),
            'time': openapi.Schema(type=openapi.TYPE_STRING,  description='Entry time (HH:MM:SS)'),
            'payment_mode': openapi.Schema(type=openapi.TYPE_STRING, description='Payment method'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Additional notes'),
            'voice_entry': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Was this entered via voice?'),
        },
        example={
            "amount": "750.00",
            "notes": "Updated lunch expense"
        }
    ),
    responses={
        200: openapi.Response(description="Entry updated successfully", schema=IncomeExpenseSerializer()),
        400: openapi.Response(description="Invalid data provided"),
        404: openapi.Response(description="Entry not found")
    }
)
@api_view(['PUT', 'PATCH'])
def income_expense_update(request, pk):
    try:
        entry = IncomeExpense.objects.get(pk=pk)
    except IncomeExpense.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = IncomeExpenseSerializer(entry, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='delete',
    operation_description="Delete an income/expense entry",
    operation_summary="Delete income/expense entry",
    tags=['Income & Expense'],
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="Income/expense entry ID to delete",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        204: openapi.Response(description="Entry deleted successfully"),
        404: openapi.Response(description="Entry not found")
    }
)
@api_view(['DELETE'])
def income_expense_delete(request, pk):
    try:
        entry = IncomeExpense.objects.get(pk=pk)
    except IncomeExpense.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    entry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
