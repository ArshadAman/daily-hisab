
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Plan, Subscription, Coupon
from .serializers import PlanSerializer, SubscriptionSerializer, CouponSerializer

# Plan APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all subscription plans",
    operation_summary="Get all subscription plans",
    tags=['Subscription Plans'],
    responses={
        200: openapi.Response(
            description="Subscription plans retrieved successfully",
            schema=PlanSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Premium Plan",
                        "description": "Full access to all features",
                        "price": "999.00",
                        "duration_days": 30,
                        "features": {
                            "max_businesses": 5,
                            "max_transactions": 10000,
                            "advanced_reports": True,
                            "priority_support": True
                        },
                        "is_active": True,
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def plan_list(request):
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new subscription plan",
    operation_summary="Create subscription plan",
    tags=['Subscription Plans'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'price', 'duration_days'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Plan name'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Plan description'),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Plan price'),
            'duration_days': openapi.Schema(type=openapi.TYPE_INTEGER, description='Plan duration in days'),
            'features': openapi.Schema(type=openapi.TYPE_OBJECT, description='Plan features as JSON'),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is plan active', default=True),
        },
        example={
            "name": "Basic Plan",
            "description": "Essential features for small businesses",
            "price": "499.00",
            "duration_days": 30,
            "features": {
                "max_businesses": 2,
                "max_transactions": 5000,
                "advanced_reports": False,
                "priority_support": False
            },
            "is_active": True
        }
    ),
    responses={
        201: openapi.Response(description="Subscription plan created successfully", schema=PlanSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def plan_create(request):
    serializer = PlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def plan_detail(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plan)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def plan_update(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PlanSerializer(plan, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def plan_delete(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    plan.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Subscription APIs
@api_view(['GET'])
def subscription_list(request):
    subs = Subscription.objects.all()
    serializer = SubscriptionSerializer(subs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def subscription_create(request):
    serializer = SubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def subscription_detail(request, pk):
    try:
        sub = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SubscriptionSerializer(sub)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def subscription_update(request, pk):
    try:
        sub = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SubscriptionSerializer(sub, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def subscription_delete(request, pk):
    try:
        sub = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    sub.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Coupon APIs
@api_view(['GET'])
def coupon_list(request):
    coupons = Coupon.objects.all()
    serializer = CouponSerializer(coupons, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def coupon_create(request):
    serializer = CouponSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def coupon_detail(request, pk):
    try:
        coupon = Coupon.objects.get(pk=pk)
    except Coupon.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CouponSerializer(coupon)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def coupon_update(request, pk):
    try:
        coupon = Coupon.objects.get(pk=pk)
    except Coupon.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CouponSerializer(coupon, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def coupon_delete(request, pk):
    try:
        coupon = Coupon.objects.get(pk=pk)
    except Coupon.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    coupon.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
