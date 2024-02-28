from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import CustomUser, InvitationCode
from members.models import PaymentImage, Wallet

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

admin.site.register(InvitationCode)
admin.site.register(CustomUser, CustomUserAdmin)


class PaymentImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'created_at')  # Customize the columns displayed
    list_filter = ('created_at',)  # Enable filtering by created_at
    date_hierarchy = 'created_at'  # Add a date drill-down functionality

admin.site.register(PaymentImage, PaymentImageAdmin)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')  # Customize the columns displayed
    search_fields = ('user__username',)  # Enable search by username

admin.site.register(Wallet, WalletAdmin)
