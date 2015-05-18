
from mpyq.mpyq import MPQArchive
from protocols import protocol15405
from importlib import import_module
from Ladder.models import Player
from django.core.exceptions import ObjectDoesNotExist
import os, sys, re

def HandleUploadedFile(f, des):
    with open(des, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def DecodeReplay(filePath):
    # load replay with function
    archive = MPQArchive(filePath)
    
    # Read the protocol header, this can be read with any protocol
    contents = archive.header['user_data_header']['content']
    header = protocol15405.decode_replay_header(contents)

    # The header's baseBuild determines which protocol to use
    baseBuild = header['m_version']['m_baseBuild']
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/protocols')
        protocol = __import__('protocol%s' % (baseBuild,))
    except:
        return 'Unsupported base build: %d' % baseBuild
    
    # read the fiel and get basic details    
    contents = archive.read_file('replay.details')
    details = protocol.decode_replay_details(contents)
    
    # delete file from disk once the data has been read
    os.remove(filePath)
    
    #return the dict of details about the game from replaystuff.insert(0, stuff[:])
    return details

def GetPlayerCountry(name):
    try:
        player = Player.objects.get(Name=name)
        return player.Country
    except ObjectDoesNotExist:
        return 'us.png'

def BuildContentFromReplay(filepath):
    details = DecodeReplay(filepath)
    
    if details == '':
        return 'false'
        
    winners = []
    lossers = []
    # get winners and lossers
    for player in details['m_playerList']:
        if player['m_result'] == 0:
            continue
        # winners
        elif player['m_result'] == 1:
            # clan tages use <sp/> to seprate data and tag, must not include ta
            parse = re.split('<sp/>', player['m_name'])
            if len(parse) > 1:
                winners.append({'name':parse[1], 'race':player['m_race']+'.png', 'country':GetPlayerCountry(parse[1])})
            else:
                winners.append({'name':player['m_name'], 'race':player['m_race']+'.png', 'country':GetPlayerCountry(player['m_name'])})
        #lossers
        elif player['m_result'] == 2:
            # clan tages use <sp/> to seprate data and tag, must not include ta
            parse = re.split('<sp/>', player['m_name'])
            if len(parse) > 1:
                lossers.append({'name':parse[1], 'race':player['m_race']+'.png',  'country':GetPlayerCountry(parse[1])})     
            else:
                lossers.append({'name':player['m_name'], 'race':player['m_race']+'.png', 'country':GetPlayerCountry(player['m_name'])})
    
    stats = {'winners':winners, 'lossers':lossers, 'map':details['m_title'], 'datetimestamp':details['m_timeUTC']}
        
    #assert False, locals()
    return stats 
    
