from player import Player
from card_keyword import *

def create_players(game):
    player1 = Player(game, 0)
    player2 = Player(game, 1)
    return {0: player1, 1: player2}


def position_cards(game):
    return True


def take_turn(game):
    # Wait for player input
    print_gamestate(game)
    valid_input = False
    while not valid_input:
        friendly_card = input("Friendly card: ")
        opponent_card = input("Opponent card: ")
        if friendly_card.isdigit() and opponent_card.isdigit\
            and int(friendly_card) in game.players[game.current_player].cards.keys()\
            and int(opponent_card) in game.players[game.uncurrent_player].cards.keys():
            valid_input = True
        else: print("Invalid input, please try again")
    resolve_attack(game, game.players[game.current_player].cards.get(int(friendly_card)), game.players[game.uncurrent_player].cards.get(int(opponent_card)))

    resolve_gamestate(game)
    
    game.current_player = (game.current_player + 1) % 2
    game.uncurrent_player = (game.uncurrent_player + 1) % 2


def resolve_gamestate(game):
    cards_to_remove = []
    for player in game.players.values():
        for card in player.cards.values():
            if card.health <= 0:
                cards_to_remove.append(card)

    # Update position of cards to the right of each card in cards to remove
    for card in cards_to_remove:
        for player_card in card.player.cards.values():
            if player_card.position > card.position:
                player_card.position -= 1
    
    for player in game.players.values():
        player.cards = {k: v for k, v in player.cards.items() if v not in cards_to_remove}

    if len(game.players[game.current_player].cards) == 0 and len(game.players[game.uncurrent_player].cards) == 0:
        print("Draw")
        game.ended = True
    elif len(game.players[game.current_player].cards) == 0:
        print("Player " + str(game.uncurrent_player) + " won!")
        game.ended = True
    elif len(game.players[game.uncurrent_player].cards) == 0:
        print("Player " + str(game.current_player) + " won!")
        game.ended = True


def resolve_attack(game, friendly_card, opponent_card):
    before_attack_keywords = []
    during_attack_keywords = []
    after_attack_keywords = []

    for card in [friendly_card, opponent_card]:
        for keyword in card.keywords:
            if keyword.stage == AttackStage.BEFORE_ATTACK: before_attack_keywords.append([keyword, card])
            if keyword.stage == AttackStage.DURING_ATTACK: during_attack_keywords.append([keyword, card])
            if keyword.stage == AttackStage.AFTER_ATTACK: after_attack_keywords.append([keyword, card])

    # Check for adjacent-relevant keywords on adjacent cards
    #TODO

    before_attack(game, friendly_card, opponent_card, before_attack_keywords)
    during_attack(game, friendly_card, opponent_card, during_attack_keywords)
    after_attack(game, friendly_card, opponent_card, after_attack_keywords)


def before_attack(game, friendly_card, opponent_card, keywords):
    for keyword in keywords:
        if keyword[0] == Shielded: 
            if not keyword[0].triggered: 
                keyword[1].invulnerability_charges += 1
                keyword[0].triggered = True


def during_attack(game, friendly_card, opponent_card, keywords):
    resolve_damage(game, friendly_card, opponent_card, friendly_card.power)
    resolve_damage(game, opponent_card, friendly_card, opponent_card.power)


def after_attack(game, friendly_card, opponent_card, keywords):
    pass


def resolve_damage(game, damaging_card, card_to_damage, damage_amount):
    if card_to_damage.invulnerability_charges > 0:
        card_to_damage.invulnerability_charges -= 1
        return
    else: card_to_damage.health -= damage_amount


def print_gamestate(game):
    print_board(game, game.uncurrent_player)
    print_board(game, game.current_player)


def print_board(game, player):
    print("Player: " + str(player))
    board = ""
    sorted_cards = list(game.players.get(player).cards.values())
    sorted_cards.sort(key=lambda x: x.position)
    for card in sorted_cards:
        board += "["
        board += str(card.id)
        board += ", "
        board += str(card.name)
        board += ", "
        board += str(card.power)
        board += ", "
        board += str(card.health)
        for keyword in card.keywords:
            board += ", "
            board += str(keyword.name)
        board += "]"
    print(board)