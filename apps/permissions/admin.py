from django.contrib import admin
from .models import Role, Permission, UserRole, AuditLog

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'resource', 'action', 'is_active']
    list_filter = ['resource', 'action', 'is_active']
    search_fields = ['name']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'role_type', 'is_active']
    list_filter = ['role_type', 'is_active']
    search_fields = ['name']
    filter_horizontal = ['permissions']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'assigned_date']
    list_filter = ['role', 'assigned_date']
    search_fields = ['user__username']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'model_name', 'object_id']
    readonly_fields = ['timestamp']
