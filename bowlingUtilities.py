import pandas as pd
from constants import *
from utilities import *
import math


def get_player_bowling_stats(name,id):
    player_url=f'{odi_bowling_stats_url}{id}'
    player_stats_path=f'{stats_path}{name}_bowling.txt'
    raw_html=simple_get(player_url)
    html= BeautifulSoup(raw_html, 'html.parser')
    table = html.find_all('table',attrs={'class':'TableLined','cellspacing':'0', 'cellpadding':'4'})
    tab=table[0]
    with open (player_stats_path,'w+') as r:
        for row in tab.find_all('tr'):
            for y in row.find_all('td'):
                if not (("Progressive" in y.text) or ("Innings" in y.text) or ("nbsp" in y.text)):
                    line=f'{y.text.strip()};'
                    r.write(line)
            r.write('\n')





def read_player_bowling_stats(name):
    # words=name.split(" ")
    player_data=''
    player_stats_path=f'{stats_path}{name}_bowling.txt'
    player_data = pd.read_csv(player_stats_path, sep=";", header='infer',skiprows=2, engine='python',dtype=str)
    player_data.columns = ["Match_Number","Date","Versus","Ground","Batsman_Out","Overs","Figures","Extra1","Strike_Rate","Economy","Wickets","Average","Extra2"]
    
    player_data1= alter_data(player_data)
    return player_data1

def alter_data(player_data):
    temp7=0
    for index, row in player_data.iterrows():
        if (len(str(row[2])) != 3):
            temp=row[2];temp1=row[0];temp2=row[3];temp3=row[8];temp4=row[9];temp5=row[11];temp6=row[1]
        else:
            row[2]=temp;row[0]=temp1;row[3]=temp2;row[8]=temp3;row[9]=temp4;row[11]=temp5;row[1]=temp6

        if not (math.isnan(float(row[10]))):
            temp7=row[10]
        else:
            row[10]=temp7

    return player_data

def get_bowl_strike_rate(player_data):
    strikeRateDF=player_data.tail(n=1)
    strikeRate=strikeRateDF['Strike_Rate'].values[0]
    return float(strikeRate)


def write_bowling_stats(final_squad_objects):
    with open (output_bowling_stats_path,'w+') as r:
        for x in final_squad_objects:
            row=f'{x.name};{x.id};{x.id_name};{x.bowl_strike_rate};{x.bowl_avg_in_ground};{x.latest_bowl_avg};{x.bowl_avg_versus_opp}\n'
            r.write(row)

def get_latest_bowl_avg(player_data):
    temp_DF=player_data.tail(n=10)
    df_size=len(temp_DF)
    total_wickets=float(temp_DF['Wickets'].values[df_size-1])
    temp_wickets=float(temp_DF['Wickets'].values[0])
    matches=len(temp_DF["Date"].unique())

    if (math.isnan(temp_wickets)):
        temp_wickets=0

    if (math.isnan(total_wickets)):
        total_wickets=0

    if (math.isnan(matches)):
        matches=0
    
    if(total_wickets != 0 and matches != 0 and temp_wickets != 0):
        latest_bowling_average=(total_wickets-temp_wickets)/matches
        return latest_bowling_average
    else:

        return 0

def get_bowl_avg_versus_opp(player_data,id,team1,team2):
    opposition=''
    team_name=get_team_name(id)

    if(team_name.lower() == team1.lower()):
        opposition=team2
    else:
        opposition=team1
    
    matches_ver_opp_DF=player_data.loc[player_data['Versus'] == opposition]
    matches=len(matches_ver_opp_DF["Date"].unique())
    
    tempDF=player_data.loc[player_data["Versus"] == opposition]
    wickets_ver_opp_DF=tempDF.loc[tempDF["Batsman_Out"] != 'nan']
    
    wickets_versus_opp=len(wickets_ver_opp_DF)
    
    if(wickets_versus_opp != 0 and matches != 0):
        return (wickets_versus_opp/matches)
    else:
        return 0

def get_avg_wick_in_ground(player_data,ground):
    bowler_in_ground_DF=player_data.loc[(player_data["Ground"] == ground) & (player_data["Batsman_Out"] != 'nan') ]
    wickets_in_ground=len(bowler_in_ground_DF)
    matches_in_ground_DF=player_data.loc[player_data["Ground"] == ground]
    matches_in_ground=len(matches_in_ground_DF)
    
    if(wickets_in_ground != 0 and matches_in_ground != 0):
        avg_in_ground=(wickets_in_ground/matches_in_ground)
        return avg_in_ground

    else:
        return 0
    
    