from util import *
from card_keyword import *
from player import Player
import random

class Game:
    
    unique_card_id = 0

    def __init__(self):
        self.players = self.create_players()
        self.current_player = self.players.get(random.randrange(0,2))
        self.uncurrent_player = self.players.get((self.current_player.identifier + 1) % 2)
        
        self.initialised = True
        self.ended = False


    def create_players(self):
        player1 = Player(self, 0)
        player2 = Player(self, 1)
        return {0: player1, 1: player2}


    def take_turn(self):
        # Wait for player input
        print_gamestate(self)
        valid_input = False
        while not valid_input:
            friendly_card_id = input("Friendly card: ")
            opponent_card_id = input("Opponent card: ")

            if not (friendly_card_id.isdigit() and opponent_card_id.isdigit\
                and int(friendly_card_id) in self.current_player.cards.keys()\
                and int(opponent_card_id) in self.uncurrent_player.cards.keys()):
                    print("Invalid input, please try again")
                    continue 

            elif Prideful in self.current_player.cards.get(int(friendly_card_id)).keywords\
                and not self.prideful_attack_is_valid(self.current_player.cards.get(int(friendly_card_id)), self.uncurrent_player.cards.get(int(opponent_card_id))):
                    print("Prideful cards can only attack the highest health opponent card")
                    continue
            
            elif Myopic in self.current_player.cards.get(int(friendly_card_id)).keywords\
                and not self.myopic_attack_is_valid(self.current_player.cards.get(int(friendly_card_id)), self.uncurrent_player.cards.get(int(opponent_card_id))):
                    print("Myopic cards can only attack the leftmost opponent card")
                    continue
            
            else:
                valid_input = True

        self.resolve_attack(self.current_player.cards.get(int(friendly_card_id)), self.uncurrent_player.cards.get(int(opponent_card_id)))

        self.resolve_gamestate()
        
        self.change_current_player()


    def resolve_gamestate(self):
        cards_to_remove = []
        for player in self.players.values():
            for card in player.cards.values():
                if card.health <= 0:
                    cards_to_remove.append(card)

        # Update position of cards to the right of each card in cards to remove
        for card in cards_to_remove:
            for player_card in card.player.cards.values():
                if player_card.position > card.position:
                    player_card.position -= 1
        
        for player in self.players.values():
            player.cards = {k: v for k, v in player.cards.items() if v not in cards_to_remove}

        if len(self.current_player.cards) == 0 and len(self.uncurrent_player.cards) == 0:
            print("Draw")
            self.ended = True
        elif len(self.current_player.cards) == 0:
            print("Player " + str(self.uncurrent_player.identifier) + " won!")
            self.ended = True
        elif len(self.uncurrent_player.cards) == 0:
            print("Player " + str(self.current_player.identifier) + " won!")
            self.ended = True


    def resolve_attack(self, friendly_card, opponent_card):
        before_attack_keyword_and_card = []
        during_attack_keyword_and_card = []
        after_attack_keywords_and_card = []

        for card in [friendly_card, opponent_card]:
            for keyword in card.keywords:
                if keyword.stage == AttackStage.BEFORE_ATTACK: before_attack_keyword_and_card.append([keyword, card])
                if keyword.stage == AttackStage.DURING_ATTACK: during_attack_keyword_and_card.append([keyword, card])
                if keyword.stage == AttackStage.AFTER_ATTACK: after_attack_keywords_and_card.append([keyword, card])

        # Check for adjacent-relevant keywords on adjacent cards
        #TODO

        self.before_attack(friendly_card, opponent_card, before_attack_keyword_and_card)
        self.during_attack(friendly_card, opponent_card, during_attack_keyword_and_card)
        self.after_attack(friendly_card, opponent_card, after_attack_keywords_and_card)


    def before_attack(self, friendly_card, opponent_card, keyword_and_cards):
        for keyword_and_card in keyword_and_cards:
            if keyword_and_card[0] == Ranged and keyword_and_card[1] is friendly_card:
                self.resolve_damage(friendly_card, opponent_card, 1)


    def during_attack(self, friendly_card, opponent_card, keyword_and_cards):
        self.resolve_damage(friendly_card, opponent_card, friendly_card.power)
        self.resolve_damage(opponent_card, friendly_card, opponent_card.power)


    def after_attack(self, friendly_card, opponent_card, keyword_and_cards):
        for keyword_and_card in keyword_and_cards:
            if keyword_and_card[0] == Explosive: 
                if keyword_and_card[1].health <= 0:
                    for card in get_other_player(self, keyword_and_card[1].player).cards.values():
                        self.resolve_damage(keyword_and_card[1], card, 2)
            elif keyword_and_card[0] == Dervish and keyword_and_card[1] is friendly_card:
                valid_input = False
                while not valid_input:
                    target_card_id = input("Card to swap with: ")
                    if target_card_id.isdigit() and\
                        int(target_card_id) in self.current_player.cards.keys():
                            initial_friendly_card_position = friendly_card.position
                            friendly_card.position = self.current_player.cards.get(int(target_card_id)).position
                            self.current_player.cards.get(int(target_card_id)).position = initial_friendly_card_position
                            valid_input = True
                    else: print("Invalid input")
            elif keyword_and_card[0] == Ramping and keyword_and_card[1] is friendly_card:
                friendly_card.power += 1
            elif keyword_and_card[0] == Furious and keyword_and_card[1] is friendly_card:
                if opponent_card.health < 0:
                    opponent_card_adjacent_cards = []
                    for card in opponent_card.player.cards.values():
                        if abs(card.position - opponent_card.position) == 1:
                            opponent_card_adjacent_cards.append(card)
                    card_to_damage = random.choice(opponent_card_adjacent_cards)
                    self.resolve_damage(friendly_card, card_to_damage, abs(opponent_card.health))


    def resolve_damage(self, damaging_card, card_to_damage, damage_amount):
        if card_to_damage.invulnerability_charges > 0:
            card_to_damage.invulnerability_charges -= 1
            return
        else: card_to_damage.health -= damage_amount
    
    
    def change_current_player(self):
        self.current_player = self.players.get((self.current_player.identifier + 1) % 2)
        self.uncurrent_player = self.players.get((self.uncurrent_player.identifier + 1) % 2)


    def prideful_attack_is_valid(self, friendly_card, opponent_card):
        current_highest_health = None
        current_highest_health_cards = []
        for card in self.uncurrent_player.cards.values():
            if current_highest_health == None: 
                current_highest_health = card.health
                current_highest_health_cards.append(card)
            elif card.health == current_highest_health:
                current_highest_health_cards.append(card)
            elif card.health > current_highest_health: 
                current_highest_health = card.health
                current_highest_health_cards = [card]
        return opponent_card in current_highest_health_cards
    
    def myopic_attack_is_valid(self, friendly_card, opponent_card):
        return opponent_card.position == 0