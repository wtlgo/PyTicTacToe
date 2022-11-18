from ai_slow import AISlow
from typing import TYPE_CHECKING
from states import PlayerState, FieldState, GameState
from copy import deepcopy, copy

if TYPE_CHECKING:
    from game import Game


class AIAlphaBeta(AISlow):
    def _ab_minmax(
        self,
        game: "Game",
        depth: int,
        isMaximizing: bool,
        favor: PlayerState,
        alpha: float,
        beta: float,
    ) -> float:
        game_state = game.game_state

        if game_state != GameState.RUNNING:
            if game_state == GameState.DRAW:
                return depth
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
                    self._ab_minmax(
                        enemy, depth + 1, not isMaximizing, favor, alpha, beta
                    ),
                )

                if beta <= alpha:
                    return score

                if isMaximizing:
                    alpha = max(alpha, score)
                else:
                    beta = min(beta, score)

                enemy.field[i][j] = FieldState.EMPTY

        return score

    def _minmax(
        self, game: "Game", depth: int, isMaximizing: bool, favor: PlayerState
    ) -> float:
        return self._ab_minmax(
            game, depth, isMaximizing, favor, -float("inf"), float("inf")
        )
