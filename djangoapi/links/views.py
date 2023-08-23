# thirdpary
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

# project
from .models import Bookmark, Collection, CustomUser
from .serializers import BookmarkSerializer, CollectionSerializer, CustomUserSerializer, UpdateCollectionSerializer
from .utils import fetch_open_graph_data


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def created_bookmark(request):
    if request.method == 'POST':
        url = request.data.get('url')
        if not url:
            return Response({"error": "please provide URL"}, status=status.HTTP_400_BAD_REQUEST)

        # extracting data from an Open Graph
        data = await fetch_open_graph_data(url)

        # creation of the new Bookmark
        bookmark = await sync_to_async(Bookmark.objects.create)(
            user=request.user,
            title=data["title"],
            description=data["description"],
            url=url,
            type=data["type"],
            image_preview=data["image"]
        )

        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
async def delete_bookmark(request, bookmark_id):
    # Синхронные операции обернуты в sync_to_async
    try:
        bookmark = await sync_to_async(Bookmark.objects.get)(id=bookmark_id, user=request.user)
    except ObjectDoesNotExist:
        return Response({"error": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND)

    await sync_to_async(bookmark.delete)()
    return Response({"message": "Bookmark deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def create_collection(request):
    if request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()
        if is_valid:
            await sync_to_async(serializer.save)(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
async def add_bookmark_to_collection(request, collection_id):
    bookmark_id = request.data.get('bookmark_id')
    if not bookmark_id:
        return JsonResponse({"error": "Please enter Bookmark ID"}, stauts = 400)

    collection = await sync_to_async(Collection.objects.get)(id=collection_id, user=request.user)
    bookmark = await sync_to_async(Bookmark.objects.get)(id=bookmark_id, user=request.user)

    # adding of the bookmark into collection
    await sync_to_async(collection.bookmarks.add)(bookmark)

    return JsonResponse({"message": "Bookmark added to collection successfully"}, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
async def update_collection(request, collection_id):
    try:
        collection = await sync_to_async(Collection.objects.get)(id=collection_id, user=request.user)
    except ObjectDoesNotExist:
        return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateCollectionSerializer(collection, data=request.data, partioal=True)
    if serializer.is_valid():
        await sync_to_async(serializer.save)()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
async def delete_collection(request, collection_id):
    collection = await sync_to_async(Collection.objects.get)(id=collection_id, user=request.user)

    await sync_to_async(collection.delete)()

    return JsonResponse({"message": "Collection deleted successfully"}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
async def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()
        if is_valid:
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
