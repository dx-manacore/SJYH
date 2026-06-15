import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from apps.permissions.models import Permission, Role, UserRole


@pytest.mark.django_db
class TestModelValidation:
    """Test model validation"""

    def test_permission_name_required(self):
        """Test that permission name is required"""
        with pytest.raises(IntegrityError):
            Permission.objects.create(
                name=None,
                resource='invoices',
                action='view'
            )

    def test_role_name_required(self):
        """Test that role name is required"""
        with pytest.raises(IntegrityError):
            Role.objects.create(
                name=None,
                role_type='staff'
            )

    def test_permission_resource_choices(self):
        """Test permission resource choices"""
        valid_resources = ['invoices', 'inventory', 'products', 'employees', 'salaries', 'reports', 'settings']
        for resource in valid_resources:
            perm = Permission.objects.create(
                name=f'permission_{resource}',
                resource=resource,
                action='view'
            )
            assert perm.resource == resource

    def test_permission_action_choices(self):
        """Test permission action choices"""
        valid_actions = ['view', 'create', 'edit', 'delete', 'export']
        for i, action in enumerate(valid_actions):
            perm = Permission.objects.create(
                name=f'action_{i}',
                resource='invoices',
                action=action
            )
            assert perm.action == action

    def test_role_type_choices(self):
        """Test role type choices"""
        valid_types = ['admin', 'manager', 'accountant', 'hr_manager', 'staff']
        for role_type in valid_types:
            role = Role.objects.create(
                name=f'role_{role_type}',
                role_type=role_type
            )
            assert role.role_type == role_type
