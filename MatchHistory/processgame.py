
import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from MatchHistory.models import Match, Team, Player_History
from Ladder.models import Player
import datetime

#   determines the change in points for:
#   new players (option  == 0)
#   1v1 (options == 1)
#   team games (options == 2)
def point_change(wpoints, lpoints, options):
    if options == 0:
        change_points = 2
    elif options == 1:   
        if wpoints >= 200 and lpoints < 80: change_points = 1
        elif wpoints >= 200 and lpoints < 90: change_points = 1
        elif wpoints >= 200 and lpoints < 111: change_points = 1
        elif wpoints >= 200 and lpoints < 165: change_points = 3
        elif wpoints >= 200 and lpoints < 200: change_points = 3
        elif wpoints >= 200 and lpoints >= 200: change_points = 6
        
        elif wpoints > 164 and lpoints < 80: change_points = 1
        elif wpoints > 164 and lpoints < 90: change_points = 1
        elif wpoints > 164 and lpoints < 111: change_points = 3
        elif wpoints > 164 and lpoints < 165: change_points = 3
        elif wpoints > 164 and lpoints < 200: change_points = 6
        elif wpoints > 164 and lpoints >= 200: change_points = 9

        elif wpoints > 110 and lpoints < 80: change_points = 1
        elif wpoints > 110 and lpoints < 90: change_points = 3
        elif wpoints > 110 and lpoints < 111: change_points = 3
        elif wpoints > 110 and lpoints < 165: change_points = 6
        elif wpoints > 110 and lpoints < 200: change_points = 9
        elif wpoints > 110 and lpoints >= 200: change_points = 12
        
        elif wpoints > 89 and lpoints < 80: change_points = 3
        elif wpoints > 89 and lpoints < 90: change_points = 3
        elif wpoints > 89 and lpoints < 111: change_points = 6
        elif wpoints > 89 and lpoints < 165: change_points = 9
        elif wpoints > 89 and lpoints < 200: change_points = 12
        elif wpoints > 89 and lpoints >= 200: change_points = 15
        
        elif wpoints > 79 and lpoints < 80: change_points = 3
        elif wpoints > 79 and lpoints < 90: change_points = 6
        elif wpoints > 79 and lpoints < 111: change_points = 9
        elif wpoints > 79 and lpoints < 165: change_points = 12
        elif wpoints > 79 and lpoints < 200: change_points = 15
        elif wpoints > 79 and lpoints >= 200: change_points = 18
        
        elif lpoints < 80: change_points = 6
        elif lpoints < 90: change_points = 9
        elif lpoints < 111: change_points = 12
        elif lpoints < 165: change_points = 15
        elif lpoints < 200: change_points = 18
        elif lpoints >= 200: change_points = 21
    else:
        tpoints = wpoints - lpoints
        if tpoints > 70: change_points = 1
        elif tpoints > 60: change_points = 2
        elif tpoints > 45: change_points = 3
        elif tpoints > 30: change_points = 4
        elif tpoints > 15: change_points = 5
        elif tpoints > -15: change_points = 6
        elif tpoints > -31: change_points = 7
        elif tpoints > -46: change_points = 8
        elif tpoints > -61: change_points = 9
        elif tpoints > -71: change_points = 10
        elif tpoints > -81: change_points = 11
        else: change_points = 12

    return change_points


# updates a players stats based on ther current point total and there new points total
def update(new_points, player):
    if new_points > player.Points:
        player.Wins+=1
        if player.Streak > 0:
            player.Streak+=1
        else:
            player.Streak = 1
    else:
        player.Losses+=1
        if player.Streak < 0:
            player.Streak-=1
        else:
            player.Streak = -1
        
    player.Points = new_points
    
    return player

# process a match or a group of matches then updates the DB
def report_match(winner, losser, map, timestamp):
    replace_champ = False # turns true if the champ needs to be replaced because of inactivity or there is no champ in the DB
    w = [] # holds a list of dicts corosponding to the winning player(s)
    l = [] # holds a list of dicts corosponding to the lossing player(s)
    loser_history_race = {}
    winner_history_race = {}
    # determines if champ needs to be updated or added
    try:
        champ = Player.objects.latest('Champ')
    except ObjectDoesNotExist:
        champ = None
        
    try:
        if champ == None:
            replace_champ = True
        elif champ.Champ < timezone.now() - datetime.timedelta(days=7):
            replace_champ = True
    except (ObjectDoesNotExist, TypeError):
        replace_champ = True

    # determines what type of point calution needs to be done
    if len(winner) == 1:
        options = 1
    else:
        options = 2
        
    # get players that won the match from the DB and add to w list.
    # if player isn't in DB, add him/her, then add to w list
    for player in winner:
        try:
            temp = Player.objects.get(Name=player['name'])
            temp.Country = player['country']
        except ObjectDoesNotExist:
            temp = Player(Name=player['name'],Race = player['race'],Country = player['country'])
            # change point calucltions to new player
            options = 0
            
        winner_history_race[temp.Name] = player['race']
        w.append(temp)
    
    # get players that lost the match from the DB and add to l list.
    # if player isn't in DB, add him/her, then add to l list            
    for player in losser:
        try:
            temp = Player.objects.get(Name=player['name'])
            temp.Country = player['country']
        except ObjectDoesNotExist:
            temp = Player(Name=player['name'],Race = player['race'],Country = player['country'])
            # change point calucltions to new player
            options = 0
            
        loser_history_race[temp.Name] = player['race']
        l.append(temp)

    winner_points = sum(i.Points for i in w) # total of points the winner(s) have
    losser_points = sum(i.Points for i in l) # total of points the losser(s) have
    update_points = point_change(winner_points, losser_points, options) # get point change

    # update champ info if the champ was defeated, a champ was kicked due to inactivity, or there was no champ
    if len(winner) == 1:
        if l[0].ChampStatus() == "champ" or replace_champ:
            w[0].Champ = timezone.now()

    # update all the stats for all players involved in the match        
    for i in range(len(w)):
        w[i] = update((w[i].Points + update_points), w[i])
    for i in range(len(l)):
        l[i] = update((l[i].Points - update_points), l[i])
        
    
    # update PastGames in the DB
    match = Match(Points=update_points, Map=map, Timestamp=timestamp)
    match.save()
    winners = Team(MatchID=match,Outcome='Win')
    winners.save()
    lossers = Team(MatchID=match,Outcome='Loss')
    lossers.save()
    
    # commit winner and losser stats to the DB
    for player in w:
        player.save()
    for player in l:
        player.save()
    
    # update PlayerHistory in the DB
    for player in w:
        tmp = Player_History(TeamID=winners,PlayerID=player,Wins=player.Wins,Losses=player.Losses,Streak=player.Streak,Points=player.Points,Race=winner_history_race[player.Name],Name=player.Name,Country=player.Country)
        tmp.save()
    for player in l:
        tmp = Player_History(TeamID=lossers,PlayerID=player,Wins=player.Wins,Losses=player.Losses,Streak=player.Streak,Points=player.Points,Race=loser_history_race[player.Name],Name=player.Name,Country=player.Country)
        tmp.save()
    