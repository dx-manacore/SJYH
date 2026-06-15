from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.core.mixins import BaseViewSetMixin
from .models import Role, Permission, UserRole, AuditLog
from .serializers import RoleSerializer, PermissionSerializer, UserRoleSerializer, AuditLogSerializer

class PermissionViewSet(BaseViewSetMixin):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['resource', 'action']
    search_fields = ['name', 'description']

class RoleViewSet(BaseViewSetMixin):
    queryset = Role.objects.prefetch_related('permissions')
    serializer_class = RoleSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

class UserRoleViewSet(BaseViewSetMixin):
    queryset = UserRole.objects.select_related('user', 'role')
    serializer_class = UserRoleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'role']

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.select_related('user')
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'action', 'model_name']
    search_fields = ['model_name', 'object_id']
    ordering_fields = ['-timestamp']
    permission_classes = []
