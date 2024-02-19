from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'full_name', 'profile_image', 'is_staff', 'is_active','is_superuser','premium')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'full_name', 'profile_image', 'is_staff', 'is_active','is_superuser','premium')}
        ),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
