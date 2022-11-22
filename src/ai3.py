from ai import AI
from typing import TYPE_CHECKING
import sqlite3
from states import FieldState, PlayerState, GameState
from random import choice

if TYPE_CHECKING:
    from game import Game


class AI3(AI):
    def __init__(self) -> None:
        super().__init__()

        self._db = sqlite3.connect("memory.ai")
        with self._db:
            self._db.executescript(
                """
                    CREATE TABLE IF NOT EXISTS MEMORY (
                        code INTEGER,
                        favor INTEGER,
                        is_maximizing INTEGER,
                        grid_size INTEGER,
                        score REAL
                    );
                """
            )

    def __code(self, game: "Game") -> int:
        res = 0

        for val, _, _ in game.grid.iterator():
            res *= 3
            res += 0 if val == FieldState.EMPTY else 1 if val == FieldState.NOD else 2

        return res

    def _evaluate(self, game: "Game", depth: int, favor: PlayerState) -> float | None:
        game_state = game.game_state

        if game_state == GameState.RUNNING:
            return None

        if game_state == GameState.DRAW:
            return depth

        if (game_state == GameState.CROSS_WIN and favor == PlayerState.CROSS) or (
            game_state == GameState.NOD_WIN and favor == PlayerState.NOD
        ):
            return 100 - depth

        return -100 + depth

    def __minmax(
        self,
        game: "Game",
        depth: int,
        isMaximizing: bool,
        favor: PlayerState,
        alpha: float,
        beta: float,
    ) -> float:
        value = self._evaluate(game, depth, favor)
        if value is not None:
            return value

        enemy = game.clone()
        enemy.is_player_cross = not game.is_player_cross

        score: float = -float("inf") if isMaximizing else float("inf")
        score_optimizer = max if isMaximizing else min

        for val, i, j in game.grid.iterator():
            if val != FieldState.EMPTY:
                continue

            enemy.grid[i, j] = (
                FieldState.CROSS
                if game.ai_figure == PlayerState.CROSS
                else FieldState.NOD
            )

            score = score_optimizer(
                score,
                self.__minmax_db(
                    enemy,
                    depth + 1,
                    not isMaximizing,
                    favor,
                    alpha,
                    beta,
                ),
            )

            if isMaximizing:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)

            if beta <= alpha:
                return score

            enemy.grid[i, j] = FieldState.EMPTY

        return score

    def __minmax_db(
        self,
        game: "Game",
        depth: int,
        isMaximizing: bool,
        pfavor: PlayerState,
        alpha: float,
        beta: float,
    ) -> float:
        favor = 0 if pfavor == PlayerState.NOD else 1
        code = self.__code(game)

        res = self._db.execute(
            """
                    SELECT score FROM MEMORY
                    WHERE code=:code AND favor=:favor AND
                          is_maximizing=:is_maximizing AND grid_size=:grid_size
                """,
            {
                "code": code,
                "favor": favor,
                "is_maximizing": isMaximizing,
                "grid_size": game.grid.size,
            },
        ).fetchone()

        if res is not None:
            return res[0]

        score = self.__minmax(game, depth, isMaximizing, pfavor, alpha, beta)

        self._db.execute(
            """
                    INSERT INTO MEMORY(code, favor, is_maximizing, grid_size, score)
                    VALUES(:code, :favor, :is_maximizing, :grid_size, :score)
                """,
            {
                "code": code,
                "favor": favor,
                "is_maximizing": isMaximizing,
                "score": score,
                "grid_size": game.grid.size,
            },
        )

        return score

    def decide(self, game: "Game") -> tuple[int, int]:
        with self._db:

            opts: list[tuple[int, int]] = []
            score = -float("inf")

            enemy = game.clone()
            enemy.is_player_cross = not enemy.is_player_cross

            for val, i, j in game.grid.iterator():
                if val != FieldState.EMPTY:
                    continue

                enemy.grid[i, j] = (
                    FieldState.CROSS
                    if game.ai_figure == PlayerState.CROSS
                    else FieldState.NOD
                )

                new_score = self.__minmax_db(
                    enemy,
                    1,
                    False,
                    game.ai_figure,
                    -float("inf"),
                    float("inf"),
                )

                if new_score > score:
                    opts = [(i, j)]
                    score = new_score
                elif new_score == score:
                    opts.append((i, j))

                enemy.grid[i, j] = FieldState.EMPTY

            return choice(opts)
