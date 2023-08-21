from django.urls import path, include
from . import views
# from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import BookmarkViewSet, CollectionViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet)
router.register(r'collection', CollectionViewSet)
router.register(r'user', CustomUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
