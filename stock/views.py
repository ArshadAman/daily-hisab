
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import StockItem, StockTransaction
from .serializers import StockItemSerializer, StockTransactionSerializer

# StockItem APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all stock items",
    operation_summary="Get all stock items",
    tags=['Stock Management'],
    responses={
        200: openapi.Response(
            description="Stock items retrieved successfully",
            schema=StockItemSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "user": 1,
                        "business": 1,
                        "name": "Apple iPhone 14",
                        "sku": "IP14-128-BLK",
                        "category": "Electronics",
                        "unit": "pieces",
                        "cost_price": "50000.00",
                        "selling_price": "55000.00",
                        "current_stock": 25,
                        "min_stock": 5,
                        "max_stock": 100,
                        "description": "Latest iPhone model",
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def stockitem_list(request):
    items = StockItem.objects.all()
    serializer = StockItemSerializer(items, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new stock item",
    operation_summary="Create stock item",
    tags=['Stock Management'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['user', 'business', 'name', 'cost_price', 'selling_price'],
        properties={
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'business': openapi.Schema(type=openapi.TYPE_INTEGER, description='Business ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Item name'),
            'sku': openapi.Schema(type=openapi.TYPE_STRING, description='Stock Keeping Unit (unique identifier)'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description='Item category'),
            'unit': openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measurement (pieces, kg, liters, etc.)'),
            'cost_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cost price per unit'),
            'selling_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Selling price per unit'),
            'current_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Current stock quantity', default=0),
            'min_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum stock threshold', default=0),
            'max_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum stock capacity', default=0),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Item description'),
        },
        example={
            "user": 1,
            "business": 1,
            "name": "Samsung Galaxy S24",
            "sku": "SG24-256-WHT",
            "category": "Electronics",
            "unit": "pieces",
            "cost_price": "45000.00",
            "selling_price": "50000.00",
            "current_stock": 15,
            "min_stock": 3,
            "max_stock": 50,
            "description": "Latest Samsung flagship phone"
        }
    ),
    responses={
        201: openapi.Response(description="Stock item created successfully", schema=StockItemSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def stockitem_create(request):
    serializer = StockItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a specific stock item by ID",
    operation_summary="Get stock item details",
    tags=['Stock Management'],
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="Stock item ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Stock item retrieved successfully",
            schema=StockItemSerializer(),
            examples={
                "application/json": {
                    "id": 1,
                    "user": 1,
                    "business": 1,
                    "name": "Apple iPhone 14",
                    "sku": "IP14-128-BLK",
                    "category": "Electronics",
                    "unit": "pieces",
                    "cost_price": "50000.00",
                    "selling_price": "55000.00",
                    "current_stock": 25,
                    "min_stock": 5,
                    "max_stock": 100,
                    "description": "Latest iPhone model",
                    "created_at": "2025-01-15T10:00:00Z"
                }
            }
        ),
        404: openapi.Response(description="Stock item not found")
    }
)
@api_view(['GET'])
def stockitem_detail(request, pk):
    try:
        item = StockItem.objects.get(pk=pk)
    except StockItem.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StockItemSerializer(item)
    return Response(serializer.data)

@swagger_auto_schema(
    method='put',
    operation_description="Update an existing stock item",
    operation_summary="Update stock item",
    tags=['Stock Management'],
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="Stock item ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Item name'),
            'sku': openapi.Schema(type=openapi.TYPE_STRING, description='Stock Keeping Unit'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description='Item category'),
            'unit': openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measurement'),
            'cost_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cost price per unit'),
            'selling_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Selling price per unit'),
            'current_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Current stock quantity'),
            'min_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum stock threshold'),
            'max_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum stock capacity'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Item description'),
        },
        example={
            "name": "Apple iPhone 14 Pro",
            "selling_price": "60000.00",
            "current_stock": 30,
            "description": "Updated iPhone Pro model"
        }
    ),
    responses={
        200: openapi.Response(description="Stock item updated successfully", schema=StockItemSerializer()),
        400: openapi.Response(description="Invalid data provided"),
        404: openapi.Response(description="Stock item not found")
    }
)
@swagger_auto_schema(
    method='patch',
    operation_description="Partially update an existing stock item",
    operation_summary="Partially update stock item",
    tags=['Stock Management'],
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="Stock item ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Item name'),
            'sku': openapi.Schema(type=openapi.TYPE_STRING, description='Stock Keeping Unit'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, description='Item category'),
            'unit': openapi.Schema(type=openapi.TYPE_STRING, description='Unit of measurement'),
            'cost_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cost price per unit'),
            'selling_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Selling price per unit'),
            'current_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Current stock quantity'),
            'min_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum stock threshold'),
            'max_stock': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum stock capacity'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Item description'),
        },
        example={
            "current_stock": 35
        }
    ),
    responses={
        200: openapi.Response(description="Stock item updated successfully", schema=StockItemSerializer()),
        400: openapi.Response(description="Invalid data provided"),
        404: openapi.Response(description="Stock item not found")
    }
)
@api_view(['PUT', 'PATCH'])
def stockitem_update(request, pk):
    try:
        item = StockItem.objects.get(pk=pk)
    except StockItem.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StockItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def stockitem_delete(request, pk):
    try:
        item = StockItem.objects.get(pk=pk)
    except StockItem.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# StockTransaction APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all stock transactions (in/out movements)",
    operation_summary="Get all stock transactions",
    tags=['Stock Transactions'],
    responses={
        200: openapi.Response(
            description="Stock transactions retrieved successfully",
            schema=StockTransactionSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "stock_item": 1,
                        "transaction_type": "in",
                        "quantity": 50,
                        "unit_price": "50000.00",
                        "total_amount": "2500000.00",
                        "date": "2025-01-15",
                        "supplier": "Tech Distributor Ltd",
                        "reference": "PO-2025-001",
                        "notes": "Initial stock purchase",
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def stocktransaction_list(request):
    txns = StockTransaction.objects.all()
    serializer = StockTransactionSerializer(txns, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new stock transaction (stock in/out movement)",
    operation_summary="Create stock transaction",
    tags=['Stock Transactions'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['stock_item', 'transaction_type', 'quantity', 'unit_price', 'date'],
        properties={
            'stock_item': openapi.Schema(type=openapi.TYPE_INTEGER, description='Stock item ID'),
            'transaction_type': openapi.Schema(type=openapi.TYPE_STRING, description='Transaction type', enum=['in', 'out']),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity moved'),
            'unit_price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Price per unit'),
            'total_amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Total transaction amount'),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Transaction date (YYYY-MM-DD)'),
            'supplier': openapi.Schema(type=openapi.TYPE_STRING, description='Supplier name (for stock in)'),
            'reference': openapi.Schema(type=openapi.TYPE_STRING, description='Reference number (PO, invoice, etc.)'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Transaction notes'),
        },
        example={
            "stock_item": 1,
            "transaction_type": "in",
            "quantity": 25,
            "unit_price": "49000.00",
            "total_amount": "1225000.00",
            "date": "2025-01-16",
            "supplier": "Mobile World Suppliers",
            "reference": "INV-2025-456",
            "notes": "Restocking inventory"
        }
    ),
    responses={
        201: openapi.Response(description="Stock transaction created successfully", schema=StockTransactionSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def stocktransaction_create(request):
    serializer = StockTransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stocktransaction_detail(request, pk):
    try:
        txn = StockTransaction.objects.get(pk=pk)
    except StockTransaction.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StockTransactionSerializer(txn)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def stocktransaction_update(request, pk):
    try:
        txn = StockTransaction.objects.get(pk=pk)
    except StockTransaction.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StockTransactionSerializer(txn, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def stocktransaction_delete(request, pk):
    try:
        txn = StockTransaction.objects.get(pk=pk)
    except StockTransaction.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    txn.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
