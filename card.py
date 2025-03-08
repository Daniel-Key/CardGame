from card_keyword import *

class Card:
    
    def __init__(self, game, player, name, keywords, power, health, position):
        self.invulnerability_charges = 0
        self.keyword_triggered = {}
        self.statuses = []

        self.id = game.unique_card_id
        game.unique_card_id += 1
        self.player = player
        self.name = name
        self.keywords = keywords
        self.power = power
        self.health = health
        self.position = position
        self.process_keywords()

    
    def process_keywords(self):
        for keyword in self.keywords:
            self.power += keyword.power_modifier
            self.health += keyword.health_modifier
            self.keyword_triggered[keyword] = False

            if keyword == Shielded: 
                self.invulnerability_charges += 1