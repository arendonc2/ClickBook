from django.contrib import admin
from .models import BookRecommendation, UserPreference

admin.site.register(BookRecommendation)
admin.site.register(UserPreference)
