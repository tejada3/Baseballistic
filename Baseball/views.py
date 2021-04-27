from django.shortcuts import render, redirect
import requests
from .forms import *

from .Team_data_class import *


"""In this function we need to grab the league leaders, and the stats we are going to display:
-homeruns(name, hr, rbi, ops), 
-hits(name ab, hits,xbh) 
-average(name, hits, avgerage, onBase percentage)
-stolen basebases(name, hits, stolenbases, stolenbase%) """

"""Please refer the MLB abbriviations for the correct Key words for the stats"""
# https://www.mlb.com/glossary/standard-stats

"""here are all the endpoints for the API"""
# https://appac.github.io/mlb-data-api-docs/

"""TO DO LIST:
-FIX THE VIEWS TO ADJUST FOR MORE THEN ONE LEADER
-FINISH MAIN TEMPLATE DESIGN 
"""


####################################### grab the other 3 stats leaders and their stats ##################################


def home_page(request):
    T = Teams.objects.all()
    form = SelectForm()


    if request.method =="POST":
        form = SelectForm(request.POST)
        if form.is_valid():
            form.save()
            pk = form.cleaned_data.get('team_id')
            print(pk)
            redirect('team_stats', pk=pk)

    return render(request, "api_info/html/player_info.html", {'y': piching_info(request),
                                                                  'n': hitting_info(request),
                                                                 't':T,
                                                              'form':form})




def hitting_info(request):
    responsehr = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_hitting_repeater.bam?sport_code='mlb'"
        "&results=1"  # the number of results you wanted
        "&game_type='R'"  # (postseason, spring training etc.) refer to API page
        "&season='2021'"  # the year for those leaders
        "&sort_column='hr'"  # the stat that they are leading in 
        "&leader_hitting_repeater.col_in=name_display_first_last"  # The are the 
        "&leader_hitting_repeater.col_in=hr"
        "&leader_hitting_repeater.col_in=rbi"
        "&leader_hitting_repeater.col_in=ops"
        "&leader_hitting_repeater.col_in=league"
    )
    homerun = responsehr.json()
    homerunLeaders = homerun['leader_hitting_repeater']['leader_hitting_mux']['queryResults']

    responseavg = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_hitting_repeater.bam?sport_code='mlb'"
        "&results='1'"
        "&game_type='R'"
        "&season='2021'"
        "&sort_column='avg'"
        "&leader_hitting_repeater.col_in=name_display_first_last"
        "&leader_hitting_repeater.col_in=h"
        "&leader_hitting_repeater.col_in=avg"
        "&leader_hitting_repeater.col_in=obp"
        "&leader_hitting_repeater.col_in=league"
    )
    avg = responseavg.json()
    avgleaders = avg['leader_hitting_repeater']['leader_hitting_mux']['queryResults']

    responseh = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_hitting_repeater.bam?sport_code='mlb'"
        "&results='1'"
        "&game_type='R'"
        "&season='2021'"
        "&sort_column='h'"
        "&leader_hitting_repeater.col_in=name_display_first_last"
        "&leader_hitting_repeater.col_in=ab"
        "&leader_hitting_repeater.col_in=h"
        "&leader_hitting_repeater.col_in=xbh"
        "&leader_hitting_repeater.col_in=league"

    )
    hits = responseh.json()
    leagueHits = hits['leader_hitting_repeater']['leader_hitting_mux']['queryResults']

    reponsesb = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_hitting_repeater.bam?sport_code='mlb'"
        "&results='1'"
        "&game_type='R'"
        "&season='2021'"
        "&sort_column='sb'"
        "&leader_hitting_repeater.col_in=name_display_first_last"
        "&leader_hitting_repeater.col_in=h"
        "&leader_hitting_repeater.col_in=sb"
        "&leader_hitting_repeater.col_in=cs"
        "&leader_hitting_repeater.col_in=league"

    )

    sb = reponsesb.json()
    sbleaders = sb['leader_hitting_repeater']['leader_hitting_mux']['queryResults']
    if sbleaders['totalSize'] == '1':
        sbp = int(sbleaders['row']["sb"]) / (int(sbleaders['row']["sb"]) + int(sbleaders['row']["cs"]))
    else:
        sbp = int(sbleaders['row'][0]["sb"]) / (int(sbleaders['row'][0]["sb"]) + int(sbleaders['row'][0]["cs"]))
    return  {'hr': homerunLeaders,
              'h': leagueHits,
              'avg': avgleaders,
              'sb': sbleaders,
              'sbp': "{:.2f}".format(sbp)}


def piching_info(request):
    # wins
    responseW = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_pitching_repeater.bam?sport_code='mlb"
        "&results='1'"
        "&game_type='R'"
        "&season='2021'"
        "&sort_column='w'"
        "&leader_pitching_repeater.col_in=name_display_first_last"
        "&leader_pitching_repeater.col_in=gs"
        "&leader_pitching_repeater.col_in=w"
        "&leader_pitching_repeater.col_in=l"
        "&leader_pitching_repeater.col_in=league"

    )
    rW = responseW.json()
    wins = rW['leader_pitching_repeater']['leader_pitching_mux']['queryResults']

    # earned run average
    responseERA = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_pitching_repeater.bam?sport_code='mlb"
        "&results='1'"
        "&game_type='R'"
        "&season='2021'"
        "&sort_column='era'"
        "&leader_pitching_repeater.col_in=name_display_first_last"
        "&leader_pitching_repeater.col_in=era"
        "&leader_pitching_repeater.col_in=er"
        "&leader_pitching_repeater.col_in=ip"
        "&leader_pitching_repeater.col_in=league"

    )

    rERA = responseERA.json()
    eRA = rERA['leader_pitching_repeater']['leader_pitching_mux']['queryResults']


    # STRIKE OUTS
    responseSO = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_pitching_repeater.bam?sport_code='mlb"
        "&results='1'"
        "&game_type='R'"
        "&season='2021'"
        "&sort_column='so'"
        "&leader_pitching_repeater.col_in=name_display_first_last"
        "&leader_pitching_repeater.col_in=so"
        "&leader_pitching_repeater.col_in=hr9"
        "&leader_pitching_repeater.col_in=np"
        "&leader_pitching_repeater.col_in=league"

    )

    rSO = responseSO.json()
    so = rSO['leader_pitching_repeater']['leader_pitching_mux']['queryResults']


    # SAVES
    responseSV = requests.get(
        "https://lookup-service-prod.mlb.com/json/named.leader_pitching_repeater.bam?sport_code='mlb"
        "&results='1'"
        "&game_type='R'"
        "&season='2021'"
        "&sort_column='sv'"
        "&leader_pitching_repeater.col_in=name_display_first_last"
        "&leader_pitching_repeater.col_in=so"
        "&leader_pitching_repeater.col_in=sv"
        "&leader_pitching_repeater.col_in=svo"
        "&leader_pitching_repeater.col_in=league"

    )

    rSV = responseSV.json()
    sv = rSV['leader_pitching_repeater']['leader_pitching_mux']['queryResults']

    return {'w': wins,
                                                                   'era': eRA,
                                                                   'so': so,
                                                                   'sv': sv, }


def team_stats(request, pk):
    T = Teams.objects.all()
    team = Team()
    team.fortyManRoster(pk)
    name = Teams.objects.get(team_id=pk)


    return render(request, "api_info/html/player_info.html", {'ts': team.get_team_stats(),
                                                              'y': piching_info(request),
                                                              'n': hitting_info(request),
                                                              't': T,
                                                              'name':name})
