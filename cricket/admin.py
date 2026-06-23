from django.contrib import admin
from .models import Ground, Team, Player, Tournament, Match, PlayerStats, MatchInnings, Commentary

admin.site.register(Ground)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(PlayerStats)
admin.site.register(MatchInnings)
admin.site.register(Commentary)