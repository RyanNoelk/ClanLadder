from django.db import models
from Ladder.models import Player

class Season(models.Model):
    Name = models.CharField(max_length=100)
    StartDate = models.DateTimeField(auto_now_add=True)
    EndDate = models.DateTimeField(blank=True, null=True)
    LastUpdate = models.DateTimeField(auto_now=True)

class Match(models.Model):
    SeasonID = models.ForeignKey(Season)
    Points = models.IntegerField(default=0)
    Map = models.CharField(max_length=100)
    Timestamp = models.CharField(max_length=50)
    LastUpdate = models.DateTimeField(auto_now=True)
    
class Team(models.Model):
    MatchID = models.ForeignKey(Match)
    Outcome = models.CharField(max_length=100)
    LastUpdate = models.DateTimeField(auto_now=True)

class Player_History(models.Model):
    PlayerID = models.ForeignKey(Player)
    TeamID = models.ForeignKey(Team)
    Wins = models.IntegerField(default=0)
    Losses = models.IntegerField(default=0)
    Streak = models.IntegerField(default=0)
    Points = models.IntegerField(default=0)
    Race = models.CharField(max_length=200)
    Name = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    LastUpdate = models.DateTimeField(auto_now=True)
    

