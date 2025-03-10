from card import Card
from card_keyword import *
import random

class Player:

    def __init__(self, game, identifier):
        self.identifier = identifier
        self.cards = {}
        card = Card(game, self, "bob", [Charmed], 3, 7, 0)
        self.cards[card.id] = card
        for i in range(1, 3):
            card = Card(game, self, "bob", [random.choice(CardKeyword.__subclasses__())], 3, 7, i)
            self.cards[card.id] = card
        
        card_ids = []
        for card in self.cards.values():
            card_ids.append(card.id)

        for id in card_ids:
            card = self.cards.get(id)
            if Generous in card.keywords:
                del self.cards[id]
                for x in range(card.power):
                    random.choice(list(self.cards.values())).power += 1
                for x in range(card.health):
                    random.choice(list(self.cards.values())).health += 1
