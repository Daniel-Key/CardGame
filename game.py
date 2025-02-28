from util import create_players
from card_keyword import *
import random

class Game:
    
    unique_card_id = 0

    def __init__(self):
        self.players = create_players(self)
        self.current_player = random.randrange(0,2)
        self.uncurrent_player = (self.current_player + 1) % 2
        
        self.initialised = True
        self.ended = False