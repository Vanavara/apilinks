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
    path('bookmarks/create/', views.created_bookmark, name='create_bookmark'),
    path('bookmarks/<int:bookmark_id>/delete/', views.delete_bookmark, name='delete_bookmark'),
    path('collection/create/', views.create_collection, name='create_collection'),
    path('collections/<int:collection_id>/add_bookmark/', views.add_bookmark_to_collection,
         name='add_bookmark_to_collection'),
    path('collections/<int:collection_id>/delete', views.delete_collection, name='delete_collection'),
    path('collections/<int:collection_id>/update/', views.update_collection, name='update_collection'),

]
