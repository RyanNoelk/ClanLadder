from django.shortcuts       import get_object_or_404, render
from Ladder.models          import Player
from Ladder.models          import Player
from django.core.exceptions import ObjectDoesNotExist
from MatchHistory.models    import Match, Team, Player_History

def HowITWorks(request):
    return render(request, 'Ladder/HowITWorks.html')
    
def Contact(request):
    return render(request, 'Ladder/Contact.html')
    
def index(request):  
    League    = []  
    champ     = {}
    pastgames = []
    
    try:
        Players = Player.objects.order_by('-Points').all()
    except ObjectDoesNotExist:
        context = {'League': League, 'Champ': champ, 'Pastgames': pastgames}
        return render(request, 'Ladder/index.html', context)
        
    league1 = []
    league2 = []
    league3 = []
    league4 = []
    league5 = []
    league6 = []

    for P in Players:
        if P.Active():
            if P.League() == 1:
                league1.append(P)
            elif P.League() == 2:
                league2.append(P)
            elif P.League() == 3:
                league3.append(P)
            elif P.League() == 4:
                league4.append(P)
            elif P.League() == 5:
                league5.append(P)
            else:
                league6.append(P)
        
        if P.ChampStatus() == 'champ':
            champ = {'Name':P.Name,'Time':P.Champ}
            
    League.append({'Players':league1, 'LeagueName':'Challenger Class (200+)',   'LeagueNumber':1})
    League.append({'Players':league2, 'LeagueName':'Veteran Class (165-199)',   'LeagueNumber':2})
    League.append({'Players':league3, 'LeagueName':'Academy Class (111-164)',   'LeagueNumber':3})
    League.append({'Players':league4, 'LeagueName':'Recruit Class (90-110)',    'LeagueNumber':4})
    League.append({'Players':league5, 'LeagueName':'Newbie Class (80-89)',      'LeagueNumber':5})
    League.append({'Players':league6, 'LeagueName':'Casual Class (79 & Under)', 'LeagueNumber':6})
        
    try:
        matchs = Match.objects.order_by('-id').all()[:3]
    except ObjectDoesNotExist:
        context = {'League': League, 'Champ': champ, 'Pastgames': pastgames}
        return render(request, 'Ladder/index.html', context)
    
    for match in matchs:
        try:
            teams = Team.objects.filter(MatchID=match)
        except ObjectDoesNotExist:
            continue
            
        lossers = []
        winners = []
        for team in teams:
            if team.Outcome == 'Win':
                try:
                    players = Player_History.objects.order_by('-Points').filter(TeamID=team)
                except ObjectDoesNotExist:
                    continue
                for player in players:
                    winners.append({'Name':player.Name, 'Points':player.Points, 'Race':player.Race, 'Country':player.Country,})
            elif team.Outcome == 'Loss':
                try:
                    players = Player_History.objects.order_by('-Points').filter(TeamID=team)
                except ObjectDoesNotExist:
                    continue                
                for player in players:
                    lossers.append({'Name':player.Name, 'Points':player.Points, 'Race':player.Race, 'Country':player.Country,})
    
        pastgames.append({'PointDiff':match.Points, 'Map':match.Map, 'Winners':winners, 'Date':match.LastUpdate, 'Lossers':lossers})
        
    context = {'League': League, 'Champ': champ, 'Pastgames': pastgames}
    return render(request, 'Ladder/index.html', context)