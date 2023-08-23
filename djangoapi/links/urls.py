# thirdparty
from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from rest_framework.routers import DefaultRouter

# project
from .views import BookmarkViewSet, CollectionViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet)
router.register(r'collection', CollectionViewSet)
router.register(r'user', CustomUserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="LinksAPI",
        default_version='v1',
        description="Bookmarks creation API"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
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
    path('register/', views.register, name='register'),
]
