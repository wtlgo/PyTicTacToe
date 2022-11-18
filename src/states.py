from enum import Enum


class FieldState(Enum):
    EMPTY = 0
    NOD = 1
    CROSS = 2


class GameState(Enum):
    RUNNING = 0
    NOD_WIN = 1
    CROSS_WIN = 2
    DRAW = 3


class PlayerState(Enum):
    NOD = 0
    CROSS = 1
