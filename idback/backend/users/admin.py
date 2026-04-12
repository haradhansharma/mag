from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ["username", "email", "role", "is_staff", "is_active"]
    list_filter = ["role", "is_staff", "is_active"]
    search_fields = ["username", "email"]
    ordering = ["username"]
    
    # This controls the edit page
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Permissions & Roles", {"fields": ("role", )}),
    )

    # This controls the "Add User" page
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),
    )
 
