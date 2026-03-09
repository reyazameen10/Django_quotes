from django.contrib import admin
from .models import Profile, Post

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'join_date']
    list_filter = ['join_date']
    search_fields = ['username', 'display_name']
