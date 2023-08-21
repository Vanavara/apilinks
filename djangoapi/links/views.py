from django.shortcuts import render
from rest_framework import viewsets
from .models import Bookmark, Collection
from .serializers import BookmarkSerializer, CollectionSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer