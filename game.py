from util import *
from card_keyword import *
from status import *
from player import Player
from card import Card
from copy import deepcopy
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

    
    def resolve_victory_conditions(self):
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

        for card in list(self.current_player.cards.values()) + list(self.uncurrent_player.cards.values()):
            for keyword in card.keywords:
                if keyword.stage == AttackStage.BEFORE_ATTACK: before_attack_keyword_and_card.append([keyword, card])
                if keyword.stage == AttackStage.DURING_ATTACK: during_attack_keyword_and_card.append([keyword, card])
                if keyword.stage == AttackStage.AFTER_ATTACK: after_attack_keywords_and_card.append([keyword, card])

        self.before_attack(friendly_card, opponent_card, before_attack_keyword_and_card)
        self.during_attack(friendly_card, opponent_card, during_attack_keyword_and_card)
        self.after_attack(friendly_card, opponent_card, after_attack_keywords_and_card)
        self.resolve_poison()


    def before_attack(self, friendly_card, opponent_card, keyword_and_cards):
        for keyword_and_card in keyword_and_cards:
            if keyword_and_card[0] == Eager and keyword_and_card[1] is friendly_card:
                self.resolve_damage(friendly_card, opponent_card, 1)
                self.resolve_victory_conditions()
            if keyword_and_card[0] == Spiky and keyword_and_card[1] == opponent_card:
                self.resolve_damage(opponent_card, friendly_card, 1)
                self.resolve_victory_conditions()


    def during_attack(self, friendly_card, opponent_card, keyword_and_cards):
        # Check if both cards in planned attack are still alive
        if friendly_card.id in self.current_player.cards and opponent_card.id in self.uncurrent_player.cards:
            self.resolve_attack_damage(friendly_card, opponent_card)


    def after_attack(self, friendly_card, opponent_card, keyword_and_cards):
        for keyword_and_card in keyword_and_cards:
            if keyword_and_card[0] == Explosive: 
                if keyword_and_card[1].health <= 0:
                    for card in get_other_player(self, keyword_and_card[1].player).cards.values():
                        self.resolve_damage(keyword_and_card[1], card, 2)
                        self.resolve_victory_conditions()
            elif keyword_and_card[0] == Whirling and keyword_and_card[1] is friendly_card and friendly_card in self.current_player.cards.values():
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
            elif keyword_and_card[0] == Ramping and keyword_and_card[1] is friendly_card and friendly_card in self.current_player.cards.values():
                friendly_card.power += 1
            elif keyword_and_card[0] == Furious and keyword_and_card[1] is friendly_card and friendly_card in self.current_player.cards.values():
                if opponent_card.health < 0:
                    opponent_card_adjacent_cards = []
                    for card in self.uncurrent_player.cards.values():
                        if are_cards_adjacent(card, opponent_card):
                            opponent_card_adjacent_cards.append(card)
                    card_to_damage = random.choice(opponent_card_adjacent_cards)
                    self.resolve_damage(friendly_card, card_to_damage, abs(opponent_card.health))
            elif keyword_and_card[0] == Cheerleading and keyword_and_card[1].player == self.current_player and\
                keyword_and_card[1] != friendly_card and keyword_and_card[0] in self.current_player.cards:
                    if are_cards_adjacent(keyword_and_card[1], friendly_card):
                        friendly_card.health += 1
            elif keyword_and_card[0] == Avenging:
                for card in keyword_and_card[1].player.cards.values():
                    if card != keyword_and_card[1]:
                        if card.health <= 0:
                            keyword_and_card[1].power += 1
            elif keyword_and_card[0] == Skulking and keyword_and_card[1].health <= 0:
                stealable_cards = [] 
                for card in get_other_player(self, keyword_and_card[1].player).cards.values():
                    if (card.health > 0):
                        stealable_cards.append(card)
                card_to_steal = random.choice(stealable_cards)
                card_to_steal.player = keyword_and_card[1].player
                highest_position_value = 0
                for card in keyword_and_card[1].player.cards.values():
                    if card.position > highest_position_value: highest_position_value = card.position
                card_to_steal.position = highest_position_value + 1
                keyword_and_card[1].player.cards[card_to_steal.id] = card_to_steal
                del get_other_player(self, keyword_and_card[1].player).cards[card_to_steal.id]
            elif keyword_and_card[0] == Disruptive and keyword_and_card[1] is friendly_card and friendly_card in self.current_player.cards.values():
                valid_input = False
                while not valid_input:
                    card_to_swap_with = input("Adjacent card to swap with: ")
                    if not (card_to_swap_with.isdigit() and int(card_to_swap_with) in self.uncurrent_player.cards.keys() and\
                                are_cards_adjacent(self.uncurrent_player.cards.get(int(card_to_swap_with)), opponent_card)):
                            print("Invalid input, please try again")
                            continue 
                    initial_opponent_card_position = opponent_card.position
                    opponent_card.position = self.uncurrent_player.cards.get(int(card_to_swap_with)).position
                    self.uncurrent_player.cards.get(int(card_to_swap_with)).position = initial_opponent_card_position
                    valid_input = True

        for keyword_and_card in keyword_and_cards:
            if keyword_and_card[0] == Rooted:
                if keyword_and_card[1].position != keyword_and_card[1].initial_position:
                    # Not technically damage
                    keyword_and_card[1].health -= 2


    def resolve_poison(self):
        for card in self.current_player.cards.values():
            if Poisoned in card.statuses:
                print("Ending turn with poisoned card")
                self.resolve_damage(None, card, card.poison_amount)


    def resolve_attack_damage(self, friendly_card, opponent_card):
        self.resolve_damage(friendly_card, opponent_card, friendly_card.power)
        self.resolve_damage(opponent_card, friendly_card, opponent_card.power)
        self.resolve_victory_conditions()

    
    def resolve_damage(self, damaging_card, card_to_damage, damage_amount):
        if damaging_card != None and Distractible in damaging_card.keywords:
            damage_to_resolve = {}
            for x in range(damage_amount):
                card_to_damage = random.choice(list(card_to_damage.player.cards.values()))
                if card_to_damage in damage_to_resolve: damage_to_resolve[card_to_damage] += 1
                else: damage_to_resolve[card_to_damage] = 1

            dummy_card = deepcopy(damaging_card)
            dummy_card.keywords.remove(Distractible)
            
            for card in damage_to_resolve.keys():
                self.resolve_damage(dummy_card, card, damage_to_resolve[card])
        if damaging_card != None and Vicious in damaging_card.keywords and card_to_damage.health < damaging_card.health:
            damage_amount += 1
        if damaging_card != None and Toxic in damaging_card.keywords:
            if not Poisoned in card_to_damage.statuses:
                card_to_damage.statuses.append(Poisoned)
                card_to_damage.poison_amount = 1
            else: 
                card_to_damage.poison_amount += 1
        if damaging_card != None and Charmed in damaging_card.keywords:
            rightmost_opponent_card = None
            for card in get_other_player(self, damaging_card.player).cards.values():
                if rightmost_opponent_card == None: rightmost_opponent_card == card
                elif card.position > rightmost_opponent_card.position: rightmost_opponent_card == card
            if card_to_damage == rightmost_opponent_card:
                return

        else:
            if card_to_damage.invulnerability_charges > 0:
                card_to_damage.invulnerability_charges -= 1
                return
            card_to_damage.health -= damage_amount
        self.resolve_gamestate()
    
    
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