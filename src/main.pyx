from game import Game
from ai_memory import AIMemory


def main():
    ai = AIMemory()
    game = Game(ai)
    game.run()


if __name__ == "__main__":
    main()
