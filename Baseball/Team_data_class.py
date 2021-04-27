import requests
from Baseball.models import Teams


class Team:
    ba = []
    obp = []
    era = []
    """team hitting stats"""
    homeruns = 0
    hits = 0
    batting_average = 0
    walks = 0
    on_base_percentage = 0
    stolen_bases = 0
    """Team pitching stats"""
    earned_run_average = 0
    innings_pitched = 0
    Wins = 0
    loses = 0
    saves = 0
    strikeouts = 0

    def fortyManRoster(self, team_id):
        response = requests.get("https://lookup-service-prod.mlb.com/TypeGET/json/named.roster_40.bam?team_id='{}'"
                                "&named.roster_40.col_in=h".format(team_id))

        team = response.json()
        full_team = team['roster_40']['queryResults']['row']
        for i in full_team:
            if str(i['position_txt']) == 'P':
                # print("ID:{}   Name: {}".format(i['player_id'], i['name_display_first_last'])
                self.pitcher_Stats(str(i['player_id']))
            else:
                # print("Name: {}".format(i['name_display_first_last']))
                self.hitter_Stats(str(i['player_id']))

    def hitter_Stats(self, player_id):
        response = requests.get(
            "https://lookup-service-prod.mlb.com/TypeGET/json/named.sport_hitting_tm.bam?league_list_id='mlb'"
            "&game_type='R'"
            "&season='2021'"
            "&player_id={}"
            "&sport_hitting_tm.col_in=hr"
            "&sport_hitting_tm.col_in=h"
            "&sport_hitting_tm.col_in=avg"
            "&sport_hitting_tm.col_in=bb"
            "&sport_hitting_tm.col_in=obp"
            "&sport_hitting_tm.col_in=sb".format(player_id))

        player = response.json()
        player_stats = player['sport_hitting_tm']['queryResults']

        if int(player_stats['totalSize']) == 1:
            self.homeruns += int(player_stats['row']['hr'])

            self.hits += int(player_stats['row']['h'])
            try:
                self.ba.append(float(player_stats['row']['avg']))
                self.batting_average = round(sum(self.ba) / len(self.ba), 3)
            except:
                self.batting_average = round(sum(self.ba) / len(self.ba), 3)

            self.walks += int(player_stats['row']['bb'])
            try:
                self.obp.append(float(player_stats['row']['obp']))
                self.on_base_percentage = round(sum(self.obp) / len(self.obp), 3)
            except:
                self.on_base_percentage = round(sum(self.obp) / len(self.obp), 3)

            self.stolen_bases += int(player_stats['row']['sb'])

    def pitcher_Stats(self, player_id):
        response = requests.get(
            "https://lookup-service-prod.mlb.com/TypeGET/json/named.sport_pitching_tm.bam?league_list_id='mlb'"
            "&game_type='R'"
            "&season='2021'"
            "&player_id={}"
            "&sport_pitching_tm.col_in=era"
            "&sport_pitching_tm.col_in=ip"
            "&sport_pitching_tm.col_in=w"
            "&sport_pitching_tm.col_in=l"
            "&sport_pitching_tm.col_in=sv"
            "&sport_pitching_tm.col_in=so"
            "&sport_pitching_tm.col_in=whip".format(player_id))
        player = response.json()
        player_stats = player['sport_pitching_tm']['queryResults']

        if int(player_stats['totalSize']) == 1:
            try:
                self.era.append(float(player_stats['row']['era']))
                self.earned_run_average = round(sum(self.era) / len(self.era), 3)
            except:
                self.earned_run_average = round(sum(self.era) / len(self.era), 3)

            self.innings_pitched += round(float(player_stats['row']['ip']), 1)
            self.strikeouts += int(player_stats['row']['so'])
            self.saves += int(player_stats['row']['sv'])
            self.loses += int(player_stats['row']['l'])
            self.Wins += int(player_stats['row']['w'])

    def get_team_stats(self):
        stats = {'hr': self.homeruns,
                 'avg': self.batting_average,
                 'bb': self.walks,
                 'h': self.hits,
                 'obp': self.on_base_percentage,
                 'sb': self.stolen_bases,
                 'era': round(self.earned_run_average, 2),
                 'ip': round(self.innings_pitched, 1),
                 'w': self.Wins,
                 'l': self.loses,
                 'sv': self.saves,
                 'so': self.strikeouts, }
        return stats




# if __name__== "__main__":
#     id = '134'
#     teamId = Team()
#     teamId.fortyManRoster(id)
#     print(teamId.get_team_stats())
