from dataclasses import dataclass
from states import PlayerState, FieldState, GameState
from typing import TYPE_CHECKING
from copy import deepcopy, copy
from random import choice
from ai import AI

if TYPE_CHECKING:
    from game import Game


class AISlow(AI):
    def _minmax(
        self, game: "Game", depth: int, isMaximizing: bool, favor: PlayerState
    ) -> float:
        game_state = game.game_state

        if game_state != GameState.RUNNING:
            if game_state == GameState.DRAW:
                return -depth
            elif (game_state == GameState.CROSS_WIN and favor == PlayerState.CROSS) or (
                game_state == GameState.NOD_WIN and favor == PlayerState.NOD
            ):
                return 100 - depth
            elif (game_state == GameState.CROSS_WIN and favor == PlayerState.NOD) or (
                game_state == GameState.NOD_WIN and favor == PlayerState.CROSS
            ):
                return -100 + depth

        enemy = copy(game)
        enemy.field = deepcopy(game.field)
        enemy.is_player_cross = not enemy.is_player_cross

        score: float = -float("inf") if isMaximizing else float("inf")
        score_optimizer = max if isMaximizing else min

        for i in range(3):
            for j in range(3):
                if enemy.field[i][j] != FieldState.EMPTY:
                    continue

                enemy.field[i][j] = (
                    FieldState.CROSS
                    if game.ai_figure == PlayerState.CROSS
                    else FieldState.NOD
                )

                score = score_optimizer(
                    score,
                    self._minmax(enemy, depth + 1, not isMaximizing, favor),
                )

                enemy.field[i][j] = FieldState.EMPTY

        return score

    def decide(self, game: "Game") -> tuple[int, int]:
        opts: list[tuple[int, int]] = []
        score = -float("inf")

        enemy = copy(game)
        enemy.field = deepcopy(game.field)
        enemy.is_player_cross = not enemy.is_player_cross

        for i in range(3):
            for j in range(3):
                if enemy.field[i][j] != FieldState.EMPTY:
                    continue

                enemy.field[i][j] = (
                    FieldState.CROSS
                    if game.ai_figure == PlayerState.CROSS
                    else FieldState.NOD
                )

                new_score = self._minmax(enemy, 1, False, game.ai_figure)

                if new_score > score:
                    opts = [(i, j)]
                    score = new_score
                elif new_score == score:
                    opts.append((i, j))

                enemy.field[i][j] = FieldState.EMPTY

        # print(opts, score)

        return choice(opts)
