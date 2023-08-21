from django.contrib import admin
from .models import CustomUser, Bookmark, Collection


admin.site.register(CustomUser)
admin.site.register(Bookmark)
admin.site.register(Collection)