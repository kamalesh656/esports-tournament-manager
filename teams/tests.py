import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team


@pytest.mark.django_db
class TestAuth:
    def test_register_user(self):
        client = APIClient()
        response = client.post('/api/auth/register/', {
            'username': 'testuser1',
            'email': 'testuser1@test.com',
            'password': 'testpass123',
            'role': 'captain'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='testuser1').exists()

    def test_login_success(self):
        User.objects.create_user(username='loginuser', password='testpass123', role='captain')
        client = APIClient()
        response = client.post('/api/auth/login/', {
            'username': 'loginuser',
            'password': 'testpass123'
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_wrong_password(self):
        User.objects.create_user(username='loginuser2', password='testpass123', role='captain')
        client = APIClient()
        response = client.post('/api/auth/login/', {
            'username': 'loginuser2',
            'password': 'wrongpassword'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_endpoint_requires_auth(self):
        client = APIClient()
        response = client.get('/api/auth/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTeam:
    def test_create_team(self):
        user = User.objects.create_user(username='captainX', password='testpass123', role='captain')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/api/auth/teams/', {'name': 'Test Team Alpha'})
        assert response.status_code == status.HTTP_201_CREATED
        assert Team.objects.filter(name='Test Team Alpha').exists()
        assert Team.objects.get(name='Test Team Alpha').captain == user

    def test_create_team_requires_auth(self):
        client = APIClient()
        response = client.post('/api/auth/teams/', {'name': 'Unauthorized Team'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
