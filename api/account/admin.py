from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'created_at', 'updated_at')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin)
