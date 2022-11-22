from enum import IntEnum


class FieldState(IntEnum):
    EMPTY = 0
    NOD = 1
    CROSS = 2


class GameState(IntEnum):
    RUNNING = 0
    NOD_WIN = 1
    CROSS_WIN = 2
    DRAW = 3


class PlayerState(IntEnum):
    NOD = 0
    CROSS = 1
