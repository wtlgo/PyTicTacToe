import random
import pygame
from graphics import Graphics
from states import FieldState, GameState, PlayerState
from ai import AI


class Game:
    def __init__(self, ai: AI) -> None:
        self.field = [[FieldState.EMPTY for _ in range(3)] for _ in range(3)]
        self.is_player_cross = random.choice([True, False])
        self._ai = ai

        pass

    def reset_game(self):
        self.field = [[FieldState.EMPTY for _ in range(3)] for _ in range(3)]
        self.is_player_cross = random.choice([True, False])

        if self.ai_figure == PlayerState.CROSS:
            x, y = self._ai.decide(self)
            self.field[x][y] = FieldState.CROSS

    @property
    def player_figure(self):
        return PlayerState.CROSS if self.is_player_cross else PlayerState.NOD

    @property
    def ai_figure(self):
        return PlayerState.NOD if self.is_player_cross else PlayerState.CROSS

    @property
    def game_state(self) -> GameState:
        for i in range(3):
            if (
                self.field[i][0] == self.field[i][1] == self.field[i][2]
            ) and self.field[i][0] != FieldState.EMPTY:
                return (
                    GameState.CROSS_WIN
                    if self.field[i][0] == FieldState.CROSS
                    else GameState.NOD_WIN
                )

            if (
                self.field[0][i] == self.field[1][i] == self.field[2][i]
            ) and self.field[0][i] != FieldState.EMPTY:
                return (
                    GameState.CROSS_WIN
                    if self.field[0][i] == FieldState.CROSS
                    else GameState.NOD_WIN
                )
        if (self.field[0][0] == self.field[1][1] == self.field[2][2]) and self.field[0][
            0
        ] != FieldState.EMPTY:
            return (
                GameState.CROSS_WIN
                if self.field[0][0] == FieldState.CROSS
                else GameState.NOD_WIN
            )

        if (self.field[0][2] == self.field[1][1] == self.field[2][0]) and self.field[0][
            2
        ] != FieldState.EMPTY:
            return (
                GameState.CROSS_WIN
                if self.field[0][2] == FieldState.CROSS
                else GameState.NOD_WIN
            )

        for row in self.field:
            for val in row:
                if val == FieldState.EMPTY:
                    return GameState.RUNNING

        return GameState.DRAW

    def run(self) -> None:
        pygame.init()

        running = True

        graphics = Graphics()

        self.reset_game()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.game_state == GameState.RUNNING:
                        x, y = graphics.mouse_quadrant

                        if self.field[x][y] != FieldState.EMPTY:
                            continue

                        self.field[x][y] = (
                            FieldState.CROSS
                            if self.player_figure == PlayerState.CROSS
                            else FieldState.NOD
                        )

                        if self.game_state == GameState.RUNNING:
                            x, y = self._ai.decide(self)
                            self.field[x][y] = (
                                FieldState.CROSS
                                if self.ai_figure == PlayerState.CROSS
                                else FieldState.NOD
                            )
                    else:
                        self.reset_game()

            graphics.redraw(self)
