import random
import pygame
from graphics import Graphics
from states import FieldState, GameState, PlayerState
from ai import AI
from copy import copy
from typing import Iterable
from first import first
from grid import Grid
from config import config


class Game:
    def __init__(self, ai: AI) -> None:
        self.grid = Grid(config.GRID_SIZE)
        self.is_player_cross = random.choice([True, False])
        self.__ai = ai

        pass

    def reset_game(self):
        self.grid = Grid(self.grid.size)
        self.is_player_cross = random.choice([True, False])

        if self.ai_figure == PlayerState.CROSS:
            x, y = self.__ai.decide(self)
            self.grid[x, y] = FieldState.CROSS

    @property
    def player_figure(self):
        return PlayerState.CROSS if self.is_player_cross else PlayerState.NOD

    @property
    def ai_figure(self):
        return PlayerState.NOD if self.is_player_cross else PlayerState.CROSS

    @staticmethod
    def __get_winner(items: Iterable[FieldState]) -> GameState | None:
        first_item = first(items)

        if first_item is None or first_item == FieldState.EMPTY:
            return None

        for val in items:
            if val != first_item:
                return None

        return first_item.to_game_state()

    @property
    def game_state(self) -> GameState:
        for i in range(self.grid.size):
            winner = self.__get_winner([self.grid[i, j] for j in range(self.grid.size)])
            if winner is not None:
                return winner

            winner = self.__get_winner([self.grid[j, i] for j in range(self.grid.size)])
            if winner is not None:
                return winner

        winner = self.__get_winner([self.grid[i, i] for i in range(self.grid.size)])
        if winner is not None:
            return winner

        winner = self.__get_winner(
            [self.grid[i, self.grid.size - 1 - i] for i in range(self.grid.size)]
        )

        if winner is not None:
            return winner

        if any(val == FieldState.EMPTY for val, _, _ in self.grid.iterator()):
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
                        x, y = graphics.mouse_quadrant(self.grid.size)

                        if self.grid[x, y] != FieldState.EMPTY:
                            continue

                        self.grid[x, y] = self.player_figure.to_field_state()

                        if self.game_state == GameState.RUNNING:
                            x, y = self.__ai.decide(self)
                            self.grid[x, y] = self.ai_figure.to_field_state()

                    else:
                        self.reset_game()

            graphics.redraw(self)

    def clone(self) -> "Game":
        game = copy(self)
        game.grid = self.grid.clone()

        return game
