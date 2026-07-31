from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin/Organizer'),
        ('captain', 'Team Captain'),
        ('player', 'Team Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captained_teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"
