from rest_framework import serializers
from .models import Bookmark, Collection, CustomUser


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(many = True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        field = ('id', 'username', 'email', 'first_name', 'last_name', 'email')