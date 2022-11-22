from enum import IntEnum


class GameState(IntEnum):
    RUNNING = 0
    NOD_WIN = 1
    CROSS_WIN = 2
    DRAW = 3


class FieldState(IntEnum):
    EMPTY = 0
    NOD = 1
    CROSS = 2

    def to_game_state(self, fallback: GameState = GameState.RUNNING) -> GameState:
        if self == FieldState.CROSS:
            return GameState.CROSS_WIN
        if self == FieldState.NOD:
            return GameState.NOD_WIN
        return fallback


class PlayerState(IntEnum):
    NOD = 0
    CROSS = 1

    def to_field_state(self) -> FieldState:
        if self == PlayerState.NOD:
            return FieldState.NOD
        else:
            return FieldState.CROSS
