from django.contrib import admin
from .models import Tournament, Registration, Match, MatchResult, Payment

admin.site.register(Tournament)
admin.site.register(Registration)
admin.site.register(Match)
admin.site.register(MatchResult)
admin.site.register(Payment)
