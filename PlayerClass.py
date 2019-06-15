from utilities import *
from constants import *


class Player:
    id=''
    first_letters=[]
    words=[]
    
    def __init__(self, name):
        self.name = name
        first_letters=find_first_letters(name)
        self.id=find_player_from_file(name)