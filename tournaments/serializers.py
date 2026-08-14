from rest_framework import serializers
from .models import Tournament, Registration, Match, MatchResult, Payment


class TournamentSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'game_title', 'format', 'entry_fee', 'slot_limit', 'status', 'organizer', 'created_at')


class RegistrationSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source='team.name')
    tournament_name = serializers.ReadOnlyField(source='tournament.name')

    class Meta:
        model = Registration
        fields = ('id', 'tournament', 'tournament_name', 'team', 'team_name', 'status', 'registered_at')
        read_only_fields = ('status',)


class MatchSerializer(serializers.ModelSerializer):
    team_a_name = serializers.ReadOnlyField(source='team_a.name')
    team_b_name = serializers.ReadOnlyField(source='team_b.name')

    class Meta:
        model = Match
        fields = ('id', 'tournament', 'team_a', 'team_a_name', 'team_b', 'team_b_name', 'scheduled_time', 'round_number')


class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchResult
        fields = ('id', 'match', 'winner_team', 'score_summary', 'submitted_by', 'confirmed_by_admin')
        read_only_fields = ('submitted_by', 'confirmed_by_admin')