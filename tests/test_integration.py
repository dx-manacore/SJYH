import pytest
from django.contrib.auth.models import User
from apps.permissions.models import Role, Permission, UserRole


@pytest.mark.django_db
class TestIntegration:
    """Integration tests for the system"""

    def test_complete_user_role_permission_flow(self, authenticated_user):
        """Test complete workflow: create user -> assign role -> grant permissions"""
        # Create permissions
        view_perm = Permission.objects.create(
            name='view_invoices',
            resource='invoices',
            action='view',
            created_by=authenticated_user
        )
        create_perm = Permission.objects.create(
            name='create_invoices',
            resource='invoices',
            action='create',
            created_by=authenticated_user
        )
        
        # Create role
        accountant_role = Role.objects.create(
            name='Accountant',
            role_type='accountant',
            description='Accounting department role',
            created_by=authenticated_user
        )
        
        # Assign permissions to role
        accountant_role.permissions.add(view_perm, create_perm)
        
        # Create user and assign role
        test_user = User.objects.create_user(
            username='accountant1',
            email='accountant@example.com',
            password='testpass123'
        )
        user_role = UserRole.objects.create(
            user=test_user,
            role=accountant_role
        )
        
        # Verify the flow
        assert user_role.user == test_user
        assert user_role.role == accountant_role
        assert accountant_role.permissions.count() == 2
        assert view_perm in accountant_role.permissions.all()
        assert create_perm in accountant_role.permissions.all()

    def test_multiple_permissions_scenario(self, authenticated_user):
        """Test creating multiple permissions for different resources"""
        resources = ['invoices', 'inventory', 'products', 'employees']
        permissions_created = []
        
        for resource in resources:
            for action in ['view', 'create', 'edit']:
                perm = Permission.objects.create(
                    name=f'{action}_{resource}',
                    resource=resource,
                    action=action,
                    created_by=authenticated_user
                )
                permissions_created.append(perm)
        
        assert Permission.objects.count() >= len(permissions_created)
        assert all(p.is_active for p in permissions_created)

    def test_admin_role_workflow(self, authenticated_user):
        """Test admin role with all permissions"""
        # Create all permissions
        all_permissions = []
        for resource in ['invoices', 'inventory', 'products', 'employees', 'salaries', 'reports', 'settings']:
            for action in ['view', 'create', 'edit', 'delete', 'export']:
                perm = Permission.objects.create(
                    name=f'{action}_{resource}',
                    resource=resource,
                    action=action,
                    created_by=authenticated_user
                )
                all_permissions.append(perm)
        
        # Create admin role
        admin_role = Role.objects.create(
            name='System Administrator',
            role_type='admin',
            description='Full system access',
            created_by=authenticated_user
        )
        
        # Assign all permissions
        admin_role.permissions.set(all_permissions)
        
        assert admin_role.permissions.count() == len(all_permissions)
