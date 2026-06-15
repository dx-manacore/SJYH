import pytest
from django.contrib.auth.models import User
from apps.core.models import BaseModel


@pytest.mark.django_db
class TestBaseModel:
    """Test BaseModel functionality"""

    def test_base_model_fields(self, authenticated_user):
        """Test that BaseModel has required fields"""
        # Using a concrete model that inherits from BaseModel
        from apps.permissions.models import Permission
        
        perm = Permission.objects.create(
            name='test_permission',
            resource='invoices',
            action='view',
            created_by=authenticated_user
        )
        
        assert hasattr(perm, 'created_at')
        assert hasattr(perm, 'updated_at')
        assert hasattr(perm, 'created_by')
        assert hasattr(perm, 'is_active')
        assert perm.is_active is True

    def test_base_model_timestamps(self, authenticated_user):
        """Test that timestamps are set correctly"""
        from apps.permissions.models import Permission
        
        perm = Permission.objects.create(
            name='timestamp_test',
            resource='invoices',
            action='view',
            created_by=authenticated_user
        )
        
        assert perm.created_at is not None
        assert perm.updated_at is not None
        assert perm.created_at <= perm.updated_at

    def test_base_model_active_by_default(self, authenticated_user):
        """Test that is_active defaults to True"""
        from apps.permissions.models import Permission
        
        perm = Permission.objects.create(
            name='active_test',
            resource='invoices',
            action='view',
            created_by=authenticated_user
        )
        
        assert perm.is_active is True
