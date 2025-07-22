
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Banner, Tutorial
from .serializers import BannerSerializer, TutorialSerializer

# Banner APIs
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of all banners",
    operation_summary="Get all banners",
    tags=['Content Management'],
    responses={
        200: openapi.Response(
            description="Banners retrieved successfully",
            schema=BannerSerializer(many=True),
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "title": "Welcome to Daily Hisab",
                        "description": "Manage your business finances easily",
                        "image_url": "https://example.com/banners/welcome.jpg",
                        "action_url": "/dashboard/",
                        "is_active": True,
                        "display_order": 1,
                        "start_date": "2025-01-01",
                        "end_date": "2025-12-31",
                        "created_at": "2025-01-15T10:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def banner_list(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new banner",
    operation_summary="Create banner",
    tags=['Content Management'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'image_url'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Banner title'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Banner description'),
            'image_url': openapi.Schema(type=openapi.TYPE_STRING, description='Banner image URL'),
            'action_url': openapi.Schema(type=openapi.TYPE_STRING, description='Action URL when banner is clicked'),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is banner active', default=True),
            'display_order': openapi.Schema(type=openapi.TYPE_INTEGER, description='Display order', default=1),
            'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Start date'),
            'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='End date'),
        },
        example={
            "title": "Premium Features Available",
            "description": "Upgrade to premium for advanced features",
            "image_url": "https://example.com/banners/premium.jpg",
            "action_url": "/subscription/plans/",
            "is_active": True,
            "display_order": 2,
            "start_date": "2025-01-15",
            "end_date": "2025-02-15"
        }
    ),
    responses={
        201: openapi.Response(description="Banner created successfully", schema=BannerSerializer()),
        400: openapi.Response(description="Invalid data provided")
    }
)
@api_view(['POST'])
def banner_create(request):
    serializer = BannerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def banner_detail(request, pk):
    try:
        banner = Banner.objects.get(pk=pk)
    except Banner.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BannerSerializer(banner)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def banner_update(request, pk):
    try:
        banner = Banner.objects.get(pk=pk)
    except Banner.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BannerSerializer(banner, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def banner_delete(request, pk):
    try:
        banner = Banner.objects.get(pk=pk)
    except Banner.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    banner.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Tutorial APIs
@api_view(['GET'])
def tutorial_list(request):
    tutorials = Tutorial.objects.all()
    serializer = TutorialSerializer(tutorials, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def tutorial_create(request):
    serializer = TutorialSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def tutorial_detail(request, pk):
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TutorialSerializer(tutorial)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def tutorial_update(request, pk):
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TutorialSerializer(tutorial, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def tutorial_delete(request, pk):
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    tutorial.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
