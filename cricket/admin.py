from django.contrib import admin
from .models import Ground, Team, Player, Tournament, Match

admin.site.register(Ground)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Match)