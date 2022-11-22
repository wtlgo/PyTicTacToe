from game import Game
from ai3 import AI3


def main():
    ai = AI3()
    game = Game(ai)
    game.run()


if __name__ == "__main__":
    main()
