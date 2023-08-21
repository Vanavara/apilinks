from django.urls import path, include
from . import views
# from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import BookmarkViewSet, CollectionViewSet

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet)
router.register(r'collection', CollectionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
