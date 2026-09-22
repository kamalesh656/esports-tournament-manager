import pytest
from rest_framework.test import APIClient
from rest_framework import status
from teams.models import User, Team
from .models import Tournament, Registration, Match


@pytest.mark.django_db
class TestTournament:
    def test_create_tournament(self):
        organizer = User.objects.create_user(username='org1', password='testpass123', role='admin')
        client = APIClient()
        client.force_authenticate(user=organizer)
        response = client.post('/api/tournaments/', {
            'name': 'Test Cup',
            'game_title': 'Valorant',
            'format': 'single_elim',
            'entry_fee': '0.00',
            'slot_limit': 8,
            'status': 'registration_open'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert Tournament.objects.filter(name='Test Cup').exists()
        assert Tournament.objects.get(name='Test Cup').organizer == organizer


@pytest.mark.django_db
class TestBracketGeneration:
    def setup_method(self):
        self.organizer = User.objects.create_user(username='bracket_org', password='pass123', role='admin')
        self.tournament = Tournament.objects.create(
            name='Bracket Test Cup',
            game_title='BGMI',
            format='single_elim',
            entry_fee=0,
            slot_limit=8,
            status='registration_open',
            organizer=self.organizer
        )

    def _create_approved_team(self, name, username):
        captain = User.objects.create_user(username=username, password='pass123', role='captain')
        team = Team.objects.create(name=name, captain=captain)
        Registration.objects.create(tournament=self.tournament, team=team, status='approved')
        return team

    def test_bracket_generation_with_4_teams(self):
        self._create_approved_team('Team A', 'capA')
        self._create_approved_team('Team B', 'capB')
        self._create_approved_team('Team C', 'capC')
        self._create_approved_team('Team D', 'capD')

        client = APIClient()
        client.force_authenticate(user=self.organizer)
        response = client.post(f'/api/tournaments/{self.tournament.id}/generate-bracket/')

        assert response.status_code == status.HTTP_201_CREATED
        assert Match.objects.filter(tournament=self.tournament).count() == 2

    def test_bracket_generation_fails_with_less_than_2_teams(self):
        self._create_approved_team('Team Solo', 'capSolo')

        client = APIClient()
        client.force_authenticate(user=self.organizer)
        response = client.post(f'/api/tournaments/{self.tournament.id}/generate-bracket/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Match.objects.filter(tournament=self.tournament).count() == 0

    def test_bracket_generation_ignores_pending_registrations(self):
        self._create_approved_team('Approved Team', 'capApproved')
        pending_captain = User.objects.create_user(username='capPending', password='pass123', role='captain')
        pending_team = Team.objects.create(name='Pending Team', captain=pending_captain)
        Registration.objects.create(tournament=self.tournament, team=pending_team, status='pending')

        client = APIClient()
        client.force_authenticate(user=self.organizer)
        response = client.post(f'/api/tournaments/{self.tournament.id}/generate-bracket/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_only_organizer_can_generate_bracket(self):
        self._create_approved_team('Team A', 'capA2')
        self._create_approved_team('Team B', 'capB2')

        other_user = User.objects.create_user(username='not_organizer', password='pass123', role='captain')
        client = APIClient()
        client.force_authenticate(user=other_user)
        response = client.post(f'/api/tournaments/{self.tournament.id}/generate-bracket/')

        assert response.status_code == status.HTTP_403_FORBIDDEN
