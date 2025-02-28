from card import Card
from card_keyword import *
import random

class Player:

    def __init__(self, game, identifier):
        self.identifier = identifier
        self.cards = {}
        for i in range(0, 3):
            card = Card(game, self, "bob", [random.choice(CardKeyword.__subclasses__())], 3, 7, i)
            self.cards[card.id] = card