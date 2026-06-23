from django.db import models
from django.conf import settings
from core.models import BaseModel


class Ground(BaseModel):
    name = models.CharField(max_length=150)

    location = models.CharField(max_length=255)

    capacity = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    image = models.URLField(
        blank=True,
        null=True
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Team(BaseModel):
    name = models.CharField(max_length=150)
    short_name = models.CharField(max_length=10)
    logo = models.URLField(
        blank=True,
        null=True
    )
    home_ground = models.ForeignKey(
        Ground,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    founded_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Player(BaseModel):
    ROLE_CHOICES = (
        ("batsman", "Batsman"),
        ("bowler", "Bowler"),
        ("all_rounder", "All Rounder"),
        ("wicket_keeper", "Wicket Keeper"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=150)
    image = models.URLField(
        blank=True,
        null=True
    )
    age = models.PositiveIntegerField()
    player_role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )
    batting_style = models.CharField(
        max_length=50,
        blank=True
    )
    bowling_style = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.name

class Tournament(BaseModel):
    STATUS_CHOICES = (
        ("upcoming", "Upcoming"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    )

    name = models.CharField(max_length=150)
    logo = models.URLField(
        blank=True,
        null=True
    )
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    prize = models.CharField(
        max_length=100,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming"
    )
    teams = models.ManyToManyField(
        Team,
        blank=True
    )
    format = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return self.name

class Match(BaseModel):
    STATUS_CHOICES = (
        ("upcoming", "Upcoming"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    )

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches"
    )
    team1 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='team1_matches'
    )
    team2 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='team2_matches'
    )
    ground = models.ForeignKey(
        Ground,
        on_delete=models.SET_NULL,
        null=True,
    )
    match_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming"
    )
    toss_winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="toss_wins"
    )
    toss_decision = models.CharField(
        max_length=10,
        choices=(
            ("bat","Bat"),
            ("field","Field"),
        ),
    )
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="match_wins"
    )
    result = models.CharField(
        blank=True
    )
    man_of_the_match = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="man_of_the_match"
    )

    def __str__(self):
        if self.tournament:
            return f"{self.team1} vs {self.team2} ({self.tournament})"
        return f"{self.team1} vs {self.team2}"
    
class PlayerStats(BaseModel):
    player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        related_name='stats'
    )
    matches = models.PositiveIntegerField(default=0)
    runs = models.PositiveIntegerField(default=0)
    wickets = models.PositiveIntegerField(default=0)
    best_bowling = models.CharField(
        max_length=20,
        blank=True
    )
    batting_average = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    strike_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    economy = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )
    ducks = models.PositiveIntegerField(default=0)
    highest_score = models.PositiveIntegerField(default=0)
    fifties = models.PositiveIntegerField(default=0)
    hundreds = models.PositiveIntegerField(default=0)
    two_hundreds = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return f"{self.player.name} Stats"

class MatchInnings(BaseModel):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='innings'
    )
    batting_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )
    innings_number = models.PositiveIntegerField()
    runs = models.PositiveIntegerField(default=0)
    wickets = models.PositiveIntegerField(default=0)
    overs = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0
    )

    def __str__(self):
        return f"{self.match} Innings {self.innings_number}"
    
class Commentary(BaseModel):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='commentary'
    )
    over = models.DecimalField(
        max_digits=4,
        decimal_places=1,
    )
    event_type = models.CharField(
        max_length=50,
        choices=(
            ("run", "Run"),
            ("wicket", "Wicket"),
            ("boundary", "Boundary"),
            ("wide", "Wide"),
            ("no_ball", "No Ball"),
            ("bye", "Bye"),
            ("legbye", "Legbye"),
        ),
        default="run"
    )
    runs = models.PositiveIntegerField(default=0)
    text = models.CharField()


    def __str__(self):
        return f"{self.match} - {self.over} - {self.text}"
    



