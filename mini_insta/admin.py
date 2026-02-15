from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'display_name', 'join_date']
    list_filter = ['join_date']
    search_fields = ['username', 'display_name']
