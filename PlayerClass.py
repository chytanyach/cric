from utilities import *
from constants import *
from bowlingUtilities import *


class Player:
    id=''
    first_letters=[]
    words=[]
    id_name=''
    team1=''
    team2=''
    venue_name=''
    # total_average=0
    # latest_average=0
    # avg_versus_opp=0
    # avg_in_ground=0

    def __init__(self, name,team1,team2,venue_name):
        self.name = name
        self.team1=team1
        self.team2=team2
        self.venue_name=venue_name

        first_letters=find_first_letters(name)
        self.id=find_player_from_file(name)
        get_player_batting_stats(self.name,self.id)
        player_data=read_player_stats(name)
        self.id_name=find_id_name(self.id)
        # self.total_average=0
        self.total_average=total_average_func(player_data) 
        # if (temp != 0 ):
        # 	self.total_average=temp
        
        # self.latest_average=0
        self.latest_average=latest_average_func(player_data)
        # if (temp != 0 ):
        # 	self.latest_average=temp

        # self.avg_versus_opp=0
        self.avg_versus_opp=avg_versus_opp_func(player_data,self.id,self.team1,self.team2)
        # if (temp != 0 ):
        # 	self.avg_versus_opp=temp


        # self.avg_in_ground=0,
        self.avg_in_ground=avg_in_ground_func(player_data,self.venue_name)

        self.final_batting_score=get_final_batting_score(float(self.total_average),float(self.latest_average),
            float(self.avg_versus_opp),float(self.avg_in_ground))

        ################################bowling stats##################################

        get_player_bowling_stats(self.name,self.id)
        player_bowling_data=read_player_bowling_stats(name)
        # print(player_bowling_data)
        if(len(player_bowling_data) > 0):
            bowl_strike_rate= get_bowl_strike_rate(player_bowling_data)
            if not (math.isnan(float(bowl_strike_rate))):
                self.bowl_strike_rate=bowl_strike_rate
            else:
                self.bowl_strike_rate=0

            self.bowl_avg_in_ground= get_avg_wick_in_ground(player_bowling_data,self.venue_name)
            self.latest_bowl_avg= get_latest_bowl_avg(player_bowling_data)
            self.bowl_avg_versus_opp = get_bowl_avg_versus_opp(player_bowling_data,self.id,self.team1,self.team2)
            self.final_bowling_score=get_final_bowling_score(self.bowl_strike_rate,self.bowl_avg_in_ground,self.latest_bowl_avg,self.bowl_avg_versus_opp)
        
        else:
            self.bowl_strike_rate=0
            self.bowl_avg_in_ground=0
            self.latest_bowl_avg=0
            self.bowl_avg_versus_opp=0
            self.final_bowling_score=0


        # if (temp != 0 ):
        # 	self.avg_in_ground=temp

        # self.latest_average=latest_average_func(player_data)
        # self.avg_versus_opp=avg_versus_opp_func(player_data)
        # self.avg_in_ground=avg_in_ground_func(player_data)