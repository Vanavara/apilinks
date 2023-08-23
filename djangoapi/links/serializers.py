# thirdparty
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

# project
from .models import Bookmark, Collection, CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2')
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


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
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'email')


class UpdateCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['name', 'description']
