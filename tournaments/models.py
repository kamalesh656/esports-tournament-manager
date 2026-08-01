from django.db import models
from teams.models import User, Team


class Tournament(models.Model):
    FORMAT_CHOICES = (
        ('single_elim', 'Single Elimination'),
    )
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('registration_open', 'Registration Open'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=150)
    game_title = models.CharField(max_length=100)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='single_elim')
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    slot_limit = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_tournaments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Registration(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='registrations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tournament', 'team')

    def __str__(self):
        return f"{self.team.name} -> {self.tournament.name} ({self.status})"


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_b')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    round_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.team_a.name} vs {self.team_b.name} (Round {self.round_number})"


class MatchResult(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='result')
    winner_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_won')
    score_summary = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submitted_results')
    confirmed_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"Result: {self.match} -> Winner: {self.winner_team.name}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_ref = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.registration} - {self.payment_status}"