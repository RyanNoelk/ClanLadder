from django.db import models
from django.utils import timezone
import datetime
from django.db.models import Max

class Player(models.Model):
    Wins = models.IntegerField(default=0)
    Losses = models.IntegerField(default=0)
    Streak = models.IntegerField(default=0)
    Points = models.IntegerField(default=100)
    Race = models.CharField(max_length=100, default='Terran.png')
    Name = models.CharField(max_length=100)
    Country = models.CharField(max_length=100, default='us.png')
    Champ = models.DateTimeField(blank=True, null=True)
    LastUpdate = models.DateTimeField(auto_now=True)
        
    def __unicode__(self):
        return self.Name
    
    def Active(self):
        return self.LastUpdate >= timezone.now() - datetime.timedelta(days=28)
        
    def Ratio(self):
        return str(int((float(self.Wins) / float((self.Wins + self.Losses))) * 100)) + '%'
    
    def League(self):
        if self.Points >= 200:
            return 1
        elif self.Points >= 165:
            return 2
        elif self.Points >= 111:
            return 3
        elif self.Points >= 90:
            return 4
        elif self.Points >= 80:
            return 5
        else:
            return 6
            
    def ChampStatus(self):
        if self.Champ is None:
            return ''
            
        if self.Champ >= Player.objects.all().aggregate(Max('Champ'))['Champ__max']:
            return 'champ'
        return 'exchamp'
        
class Alias(models.Model):
    PlayerID = models.ForeignKey(Player)
    Name = models.CharField(max_length=100)
        
        
        
        