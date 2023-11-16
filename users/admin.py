from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'email_verificated', 'is_active', 'phone_number')
    search_fields = ('email', 'first_name', 'last_name')
