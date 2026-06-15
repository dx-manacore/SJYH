import pytest
from django.contrib.auth.models import User
from apps.permissions.models import Role, Permission
from rest_framework import status


@pytest.mark.django_db
class TestAPIEndpoints:
    """Test API endpoints"""

    def test_api_schema_accessible(self, api_client):
        """Test that API schema is accessible"""
        response = api_client.get('/api/schema/')
        assert response.status_code == 200

    def test_swagger_docs_accessible(self, api_client):
        """Test that Swagger documentation is accessible"""
        response = api_client.get('/api/docs/')
        assert response.status_code == 200

    def test_admin_panel_accessible(self, api_client):
        """Test that admin panel is accessible"""
        # Admin requires login, so we expect redirect
        response = api_client.get('/admin/')
        assert response.status_code in [301, 302, 200]

    def test_permissions_list_endpoint(self, authenticated_client):
        """Test permissions list endpoint"""
        response = authenticated_client.get('/api/v1/permissions/permissions/')
        assert response.status_code == 200
        assert 'results' in response.data or isinstance(response.data, list)

    def test_roles_list_endpoint(self, authenticated_client):
        """Test roles list endpoint"""
        response = authenticated_client.get('/api/v1/permissions/roles/')
        assert response.status_code == 200
        assert 'results' in response.data or isinstance(response.data, list)

    def test_permissions_filtering(self, authenticated_client):
        """Test permissions filtering"""
        Permission.objects.create(
            name='view_invoices',
            resource='invoices',
            action='view'
        )
        response = authenticated_client.get('/api/v1/permissions/permissions/?resource=invoices')
        assert response.status_code == 200

    def test_pagination(self, authenticated_client):
        """Test API pagination"""
        for i in range(25):
            Role.objects.create(name=f'Role{i}', role_type='staff')
        response = authenticated_client.get('/api/v1/permissions/roles/')
        assert response.status_code == 200
        # Check pagination exists
        if 'results' in response.data:
            assert len(response.data['results']) <= 20
