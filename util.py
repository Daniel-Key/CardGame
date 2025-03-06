from card_keyword import *


def print_gamestate(game):
    print_board(game.uncurrent_player)
    print_board(game.current_player)
    print()


def print_board(player):
    print("Player: " + str(player.identifier))
    board = ""
    sorted_cards = list(player.cards.values())
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


def get_other_player(game, player):
    return game.players.get((player.identifier + 1) % 2)