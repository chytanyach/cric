from utilities import *
from constants import *


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
        get_player_stats(self.name,self.id)
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


        # self.avg_in_ground=0
        self.avg_in_ground=avg_in_ground_func(player_data,self.venue_name)

        
        # if (temp != 0 ):
        # 	self.avg_in_ground=temp

        # self.latest_average=latest_average_func(player_data)
        # self.avg_versus_opp=avg_versus_opp_func(player_data)
        # self.avg_in_ground=avg_in_ground_func(player_data)