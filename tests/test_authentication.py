import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestAuthentication:
    """Test authentication functionality"""

    def test_user_creation(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='testpass123'
        )
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.check_password('testpass123')

    def test_jwt_token_generation(self, authenticated_user):
        """Test JWT token generation"""
        refresh = RefreshToken.for_user(authenticated_user)
        assert str(refresh.access_token) is not None
        assert str(refresh) is not None

    def test_api_authentication(self, authenticated_client, authenticated_user):
        """Test API authentication with JWT token"""
        response = authenticated_client.get('/api/v1/permissions/roles/')
        assert response.status_code == 200

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated access is denied"""
        client = APIClient()
        response = client.get('/api/v1/permissions/roles/')
        assert response.status_code == 401

    def test_invalid_token(self):
        """Test that invalid token is rejected"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = client.get('/api/v1/permissions/roles/')
        assert response.status_code == 401
