from django.shortcuts         import get_object_or_404, render
from django.http              import HttpResponseRedirect
from django.core.urlresolvers import reverse
from replayhandler            import HandleUploadedFile, BuildContentFromReplay
from processgame              import report_match
from django.core.exceptions   import ObjectDoesNotExist
from MatchHistory.models      import Match, Team, Player_History
from Ladder.models      import Player
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
import random
from django_ajax.decorators import ajax

@ajax
def GetPlayerList(request):
    items = []
    try:
        players = Player.objects.order_by('Name')
    except ObjectDoesNotExist:
        return {'result': ''}
        
    for player in players:
        items.append(player.Name)
        
    return {'result': items}
    
@ajax
def GetPlayerRaceAndCountry(request, player_name):
    try:
        player = Player.objects.get(Name=player_name)
        items = []
        items.append(player.Race)
        items.append(player.Country)
        return {'result': items}
    except ObjectDoesNotExist:
        return {'result': ''}
            
    return {'result': ''}
    
def index(request):  
    games = [] 
    try:
        matchs = Match.objects.order_by('-LastUpdate').all()
    except ObjectDoesNotExist:
        context = {'Games': games}    
        return render(request, 'MatchHistory/index.html', context)
    
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
    
        games.append({'PointDiff':match.Points, 'Map':match.Map, 'Winners':winners, 'Date':match.LastUpdate, 'Lossers':lossers, 'ID':match.id})
        
    context = {'Games': games}    
    return render(request, 'MatchHistory/index.html', context)

@login_required(login_url='/Accounts/login/')
def SubmitReplay(request):   
    return render(request, 'MatchHistory/SubmitReplay.html')
    
    
'''   
def Upload(request):
    if request.method == 'POST':
        #HandleUploadedFile(request.FILES['file'], request.FILES['file'].name)
        return HttpResponseRedirect(reverse('MatchHistory:Confirm'))
    return HttpResponseRedirect(reverse('MatchHistory:Submit'))
'''
    
@login_required(login_url='/Accounts/login/')
def SubmitText(request): 
    game = []    
    duplicate = ''
    empty = ''
    if request.method == 'POST':
        try:
            for file in request.FILES.getlist('file'):
                if file.name[-10:] == '.SC2Replay':
                    HandleUploadedFile(file, '/tmp/' + file.name)
                    cur_game = BuildContentFromReplay('/tmp/' + file.name)
                    game.append(cur_game)
                    if Match.objects.filter(Timestamp=cur_game['datetimestamp']).exists():
                        duplicate = 'duplicate'
                    empty = '1'
        except (KeyError, UnboundLocalError):
            game = []    
    else:
        empty = '1'
        
    if empty is None or empty == '':
        return render(request, 'MatchHistory/SubmitReplay.html', {'not_valid': 'NoReplay'})
    else:
        return render(request, 'MatchHistory/SubmitText.html', {'games': game, 'Duplicate': duplicate})

def Update(request):    
    if request.method == 'POST':
        winners = {}
        losers = {}
        timestamp = {}
        map = {}
        
        for item in request.POST:
            i = item.split('.')
            if 'winner' in item:
                if 'old_name' in item and request.POST[item] != 'New':
                    try:
                        winners[i[0]][i[2]]['name'] = request.POST[item]
                    except KeyError:
                        try:
                            winners[i[0]][i[2]] = {'name':request.POST[item]}
                        except KeyError:
                            winners[i[0]] = {i[2]:{'name':request.POST[item]}}
                if 'new_name' in item and request.POST[item] != '':
                    try:
                        winners[i[0]][i[2]]['name'] = request.POST[item]
                    except KeyError:
                        try:
                            winners[i[0]][i[2]] = {'name':request.POST[item]}
                        except KeyError:
                            winners[i[0]] = {i[2]:{'name':request.POST[item]}}
                if 'race' in item:
                    try:
                        winners[i[0]][i[2]]['race'] = request.POST[item]
                    except KeyError:
                        try:
                            winners[i[0]][i[2]] = {'race':request.POST[item]}
                        except KeyError:
                            winners[i[0]] = {i[2]:{'race':request.POST[item]}}
                if 'country' in item:
                    try:
                        winners[i[0]][i[2]]['country'] = request.POST[item]
                    except KeyError:
                        try:
                            winners[i[0]][i[2]] = {'country':request.POST[item]}
                        except KeyError:
                            winners[i[0]] = {i[2]:{'country':request.POST[item]}}
            if 'loser' in item:
                if 'old_name' in item and request.POST[item] != 'New':
                    try:
                        losers[i[0]][i[2]]['name'] = request.POST[item]
                    except KeyError:
                        try:
                            losers[i[0]][i[2]] = {'name':request.POST[item]}
                        except KeyError:
                            losers[i[0]] = {i[2]:{'name':request.POST[item]}}
                if 'new_name' in item and request.POST[item] != '':
                    try:
                        losers[i[0]][i[2]]['name'] = request.POST[item]
                    except KeyError:
                        try:
                            losers[i[0]][i[2]] = {'name':request.POST[item]}
                        except KeyError:
                            losers[i[0]] = {i[2]:{'name':request.POST[item]}}
                if 'race' in item:
                    try:
                        losers[i[0]][i[2]]['race'] = request.POST[item]
                    except KeyError:
                        try:
                            losers[i[0]][i[2]] = {'race':request.POST[item]}
                        except KeyError:
                            losers[i[0]] = {i[2]:{'race':request.POST[item]}}
                if 'country' in item:
                    try:
                        losers[i[0]][i[2]]['country'] = request.POST[item]
                    except KeyError:
                        try:
                            losers[i[0]][i[2]] = {'country':request.POST[item]}
                        except KeyError:
                            losers[i[0]] = {i[2]:{'country':request.POST[item]}}
            if 'timestamp' in item:
                timestamp[i[0]] = request.POST[item]
            if 'map' in item:
                map[i[0]] = request.POST[item]            
        
        
        matches = []
        for i in map: 
            if map[i] != '' and map[i] is not None:
                w = []
                l = []
                for player in winners[i]:
                    w.append(winners[i][player]) 
                for player in losers[i]:
                    l.append(losers[i][player]) 
                    
                if all(i != '' for i in l) and all(i != '' for i in w):
                    try:
                        matches.append({'winner':w,'loser':l,'map':map[i],'time':timestamp[i]})
                    except KeyError:
                        matches.append({'winner':w,'loser':l,'map':map[i],'time':0})
        
        #assert False, locals()
        sorted_matches = sorted(matches, key=lambda k: k['time'])
        for match in sorted_matches:
            report_match(match['winner'],match['loser'],match['map'],match['time'])
            
    return HttpResponseRedirect(reverse('MatchHistory:index'))
    
    
def PlayerHistory(request, player_name):
    games = [] 
    try:
        matchs = Match.objects.order_by('-LastUpdate').all()
    except ObjectDoesNotExist:
        context = {'Games': games}    
        return render(request, 'MatchHistory/index.html', context)
    
    for match in matchs:
        try:
            teams = Team.objects.filter(MatchID=match)
        except ObjectDoesNotExist:
            continue
            
        lossers = []
        winners = []
        Add = False
        for team in teams:
            if team.Outcome == 'Win':
                try:
                    players = Player_History.objects.order_by('-Points').filter(TeamID=team)
                except ObjectDoesNotExist:
                    continue
                for player in players:
                    winners.append({'Name':player.Name, 'Points':player.Points, 'Race':player.Race, 'Country':player.Country,})
                    if (player.Name == player_name):
                        Add = True
            elif team.Outcome == 'Loss':
                try:
                    players = Player_History.objects.order_by('-Points').filter(TeamID=team)
                except ObjectDoesNotExist:
                    continue                
                for player in players:
                    lossers.append({'Name':player.Name, 'Points':player.Points, 'Race':player.Race, 'Country':player.Country,})
                    if (player.Name == player_name):
                        Add = True
        
        if Add:
            games.append({'PointDiff':match.Points, 'Map':match.Map, 'Winners':winners, 'Date':match.LastUpdate, 'Lossers':lossers, 'ID':match.id})
        
    context = {'Games': games}    
    return render(request, 'MatchHistory/PlayerHistory.html', context)
    
def FindPlayer(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/Matches/Player/'+request.POST['player_name']+'/')
    else:
        return HttpResponseRedirect(reverse('MatchHistory:index'))    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    