from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'dob', 'phone_number', 'address', 'status']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['user__username', 'first_name', 'last_name']

admin.site.register(UserProfile, UserProfileAdmin)
