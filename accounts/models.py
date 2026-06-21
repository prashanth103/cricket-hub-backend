from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("player", "Player"),
        ("captain", "Captain"),
        ("organizer", "Organizer"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="player"
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username