from django.urls import path
from .views import (
    TournamentListCreateView, TournamentDetailView,
    RegistrationListCreateView, MatchListCreateView, MatchResultCreateView,
    GenerateBracketView, MyTournamentsView, TournamentRegistrationsView,
    RegistrationUpdateView
)

urlpatterns = [
    path('tournaments/', TournamentListCreateView.as_view(), name='tournament-list-create'),
    path('tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),
    path('registrations/', RegistrationListCreateView.as_view(), name='registration-list-create'),
    path('registrations/<int:pk>/update/', RegistrationUpdateView.as_view(), name='registration-update'),
    path('matches/', MatchListCreateView.as_view(), name='match-list-create'),
    path('match-results/', MatchResultCreateView.as_view(), name='match-result-create'),
    path('tournaments/<int:tournament_id>/generate-bracket/', GenerateBracketView.as_view(), name='generate-bracket'),
    path('tournaments/<int:tournament_id>/registrations/', TournamentRegistrationsView.as_view(), name='tournament-registrations'),
    path('my-tournaments/', MyTournamentsView.as_view(), name='my-tournaments'),
]