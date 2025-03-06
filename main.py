from game import Game
from util import *

game = None

def main():
    game = Game()
    while not game.ended:
        game.take_turn()


if __name__ == '__main__':
    main()