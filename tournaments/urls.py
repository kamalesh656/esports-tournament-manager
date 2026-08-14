from django.urls import path
from .views import (
    TournamentListCreateView, TournamentDetailView,
    RegistrationListCreateView, MatchListCreateView, MatchResultCreateView
)

urlpatterns = [
    path('tournaments/', TournamentListCreateView.as_view(), name='tournament-list-create'),
    path('tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),
    path('registrations/', RegistrationListCreateView.as_view(), name='registration-list-create'),
    path('matches/', MatchListCreateView.as_view(), name='match-list-create'),
    path('match-results/', MatchResultCreateView.as_view(), name='match-result-create'),
]