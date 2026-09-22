from rest_framework import generics, permissions
from .models import Tournament, Registration, Match, MatchResult
from .serializers import (
    TournamentSerializer, RegistrationSerializer,
    MatchSerializer, MatchResultSerializer
)


class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MatchListCreateView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MatchResultCreateView(generics.CreateAPIView):
    queryset = MatchResult.objects.all()
    serializer_class = MatchResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from .models import Tournament, Registration, Match


class GenerateBracketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({"error": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND)

        # Only the organizer can generate the bracket
        if tournament.organizer != request.user:
            return Response({"error": "Only the organizer can generate the bracket"}, status=status.HTTP_403_FORBIDDEN)

        # Get all approved teams for this tournament
        approved_registrations = Registration.objects.filter(tournament=tournament, status='approved')
        teams = [reg.team for reg in approved_registrations]

        if len(teams) < 2:
            return Response({"error": "Need at least 2 approved teams to generate a bracket"}, status=status.HTTP_400_BAD_REQUEST)

        # Shuffle teams randomly for fair seeding
        random.shuffle(teams)

        # If odd number of teams, one team gets a "bye" (skips round 1) - for simplicity, we drop the last team for now
        if len(teams) % 2 != 0:
            teams = teams[:-1]

        matches_created = []
        for i in range(0, len(teams), 2):
            match = Match.objects.create(
                tournament=tournament,
                team_a=teams[i],
                team_b=teams[i + 1],
                round_number=1
            )
            matches_created.append({
                "match_id": match.id,
                "team_a": match.team_a.name,
                "team_b": match.team_b.name
            })

        return Response({
            "message": f"Bracket generated with {len(matches_created)} matches",
            "matches": matches_created
        }, status=status.HTTP_201_CREATED)
from rest_framework.permissions import IsAuthenticated


class MyTournamentsView(generics.ListAPIView):
    """Tournaments organized by the logged-in user"""
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tournament.objects.filter(organizer=self.request.user)


class TournamentRegistrationsView(generics.ListAPIView):
    """All registrations for a specific tournament (organizer only)"""
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tournament_id = self.kwargs['tournament_id']
        return Registration.objects.filter(tournament_id=tournament_id)


class RegistrationUpdateView(generics.UpdateAPIView):
    """Approve/reject a registration - organizer only"""
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        registration = self.get_object()
        if registration.tournament.organizer != request.user:
            return Response({"error": "Only the tournament organizer can update this"}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in ['approved', 'rejected', 'pending']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        registration.status = new_status
        registration.save()
        return Response(RegistrationSerializer(registration).data)