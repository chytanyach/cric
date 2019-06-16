from utilities import *
from constants import *


class Player:
    id=''
    first_letters=[]
    words=[]
    total_average=0
    latest_average=0
    avg_versus_opp=0
    avg_in_ground=0

    def __init__(self, name):
        self.name = name
        first_letters=find_first_letters(name)
        self.id=find_player_from_file(name)
        get_player_stats(self.name,self.id)
        player_data=read_player_stats(name)
        
        self.total_average=total_average_func(player_data)
        self.latest_average=latest_average_func(player_data)
        self.avg_versus_opp=avg_versus_opp_func(player_data)
        self.avg_in_ground=avg_in_ground_func(player_data)