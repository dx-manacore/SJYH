from rest_framework import serializers
from apps.core.serializers import BaseSerializer
from .models import Role, Permission, UserRole, AuditLog

class PermissionSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Permission
        fields = BaseSerializer.Meta.fields + ['id', 'name', 'resource', 'action', 'description']

class RoleSerializer(BaseSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Role
        fields = BaseSerializer.Meta.fields + ['id', 'name', 'role_type', 'description', 'permissions']

class UserRoleSerializer(BaseSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = UserRole
        fields = BaseSerializer.Meta.fields + ['id', 'user', 'user_username', 'role', 'role_name', 'assigned_date']

class AuditLogSerializer(BaseSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = AuditLog
        fields = BaseSerializer.Meta.fields + [
            'id', 'user', 'user_username', 'action', 'model_name',
            'object_id', 'changes', 'ip_address', 'timestamp'
        ]
        read_only_fields = ['timestamp', 'created_at', 'updated_at']
