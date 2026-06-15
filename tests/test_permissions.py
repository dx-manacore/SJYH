import pytest
from django.contrib.auth.models import User
from apps.permissions.models import Role, Permission, UserRole, AuditLog


@pytest.mark.django_db
class TestPermissionModel:
    """Test Permission model"""

    def test_create_permission(self):
        """Test creating a permission"""
        permission = Permission.objects.create(
            name='view_invoices',
            resource='invoices',
            action='view',
            description='View invoices'
        )
        assert permission.name == 'view_invoices'
        assert permission.resource == 'invoices'
        assert permission.action == 'view'
        assert permission.is_active is True

    def test_unique_resource_action(self):
        """Test unique constraint on resource and action"""
        Permission.objects.create(
            name='create_invoices',
            resource='invoices',
            action='create'
        )
        with pytest.raises(Exception):
            Permission.objects.create(
                name='add_invoices',
                resource='invoices',
                action='create'
            )

    def test_permission_display_str(self):
        """Test permission string representation"""
        permission = Permission.objects.create(
            name='delete_products',
            resource='products',
            action='delete'
        )
        assert 'حذف' in str(permission) or 'delete' in str(permission).lower()


@pytest.mark.django_db
class TestRoleModel:
    """Test Role model"""

    def test_create_role(self):
        """Test creating a role"""
        role = Role.objects.create(
            name='Admin Role',
            role_type='admin',
            description='Administrator role'
        )
        assert role.name == 'Admin Role'
        assert role.role_type == 'admin'
        assert role.is_active is True

    def test_role_with_permissions(self):
        """Test role with multiple permissions"""
        permission1 = Permission.objects.create(
            name='view_invoices',
            resource='invoices',
            action='view'
        )
        permission2 = Permission.objects.create(
            name='edit_invoices',
            resource='invoices',
            action='edit'
        )
        role = Role.objects.create(
            name='Accountant',
            role_type='accountant'
        )
        role.permissions.add(permission1, permission2)
        assert role.permissions.count() == 2

    def test_unique_role_name(self):
        """Test unique role name constraint"""
        Role.objects.create(name='Unique Role', role_type='staff')
        with pytest.raises(Exception):
            Role.objects.create(name='Unique Role', role_type='manager')


@pytest.mark.django_db
class TestUserRoleModel:
    """Test UserRole model"""

    def test_assign_role_to_user(self):
        """Test assigning a role to a user"""
        user = User.objects.create_user(username='testuser', password='pass')
        role = Role.objects.create(name='Staff', role_type='staff')
        user_role = UserRole.objects.create(user=user, role=role)
        assert user_role.user == user
        assert user_role.role == role

    def test_user_can_have_one_role(self):
        """Test that a user can only have one role (OneToOne)"""
        user = User.objects.create_user(username='testuser', password='pass')
        role1 = Role.objects.create(name='Role1', role_type='staff')
        role2 = Role.objects.create(name='Role2', role_type='manager')
        UserRole.objects.create(user=user, role=role1)
        with pytest.raises(Exception):
            UserRole.objects.create(user=user, role=role2)


@pytest.mark.django_db
class TestAuditLogModel:
    """Test AuditLog model"""

    def test_create_audit_log(self, authenticated_user):
        """Test creating an audit log entry"""
        audit_log = AuditLog.objects.create(
            user=authenticated_user,
            action='CREATE',
            resource='invoices',
            description='Created new invoice',
            created_by=authenticated_user
        )
        assert audit_log.user == authenticated_user
        assert audit_log.action == 'CREATE'
        assert audit_log.resource == 'invoices'


@pytest.mark.django_db
class TestPermissionAPI:
    """Test Permission API endpoints"""

    def test_list_permissions(self, authenticated_client):
        """Test listing permissions"""
        Permission.objects.create(
            name='view_invoices',
            resource='invoices',
            action='view'
        )
        response = authenticated_client.get('/api/v1/permissions/permissions/')
        assert response.status_code == 200
        assert len(response.data['results']) > 0

    def test_create_permission(self, authenticated_client):
        """Test creating a permission via API"""
        data = {
            'name': 'create_invoices',
            'resource': 'invoices',
            'action': 'create',
            'description': 'Create invoices'
        }
        response = authenticated_client.post('/api/v1/permissions/permissions/', data)
        assert response.status_code in [201, 200]


@pytest.mark.django_db
class TestRoleAPI:
    """Test Role API endpoints"""

    def test_list_roles(self, authenticated_client):
        """Test listing roles"""
        Role.objects.create(name='Admin', role_type='admin')
        response = authenticated_client.get('/api/v1/permissions/roles/')
        assert response.status_code == 200

    def test_create_role(self, authenticated_client):
        """Test creating a role via API"""
        data = {
            'name': 'New Role',
            'role_type': 'staff',
            'description': 'Test role'
        }
        response = authenticated_client.post('/api/v1/permissions/roles/', data)
        assert response.status_code in [201, 200]
