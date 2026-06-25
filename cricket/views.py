from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from drf_spectacular.utils import extend_schema

from .models import Player
from .serializers import PlayerSerializer

@extend_schema(
    tags=["Players"],
    summary="Manage Players",
    description="CRUD operations for cricket players."
)

class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing players.

    Supports:
    - List players
    - Retrieve player details
    - Create player
    - Update player
    - Delete player
    """

    queryset = Player.objects.select_related("team").all()
    serializer_class = PlayerSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "name",
    ]
    filterset_fields = [
        "player_role",
        "team",
    ]
    ordering_fields = [
        "name",
        "age",
    ]
