from game import Game
from util import *

game = None

def main():
    game = Game()
    position_cards(game)
    while not game.ended:
        take_turn(game)


if __name__ == '__main__':
    main()