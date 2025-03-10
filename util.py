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
        for status in card.statuses:
            board += ", "
            board += str(status.name)
        board += "]"
    print(board)


def get_other_player(game, player):
    return game.players.get((player.identifier + 1) % 2)


def are_cards_adjacent(card1, card2):
    return card1.player == card2.player and abs(card1.position - card2.position) == 1