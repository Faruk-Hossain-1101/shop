from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets =(
        (None, {'fields':('first_name','last_name', 'email', 'password')}),
        ('Permissions', {'fields':('is_staff', 'is_active')}),

    )
    ordering = ('email',)
admin.site.register(User, CustomUserAdmin)
