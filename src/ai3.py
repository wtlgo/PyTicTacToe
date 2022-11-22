from ai import AI
from typing import TYPE_CHECKING
import sqlite3
from states import FieldState, PlayerState, GameState
from random import choice
from math import sqrt

if TYPE_CHECKING:
    from game import Game


class AI3(AI):
    def __init__(self) -> None:
        super().__init__()

        self.__db = sqlite3.connect("memory.ai")
        with self.__db:
            self.__db.executescript(
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

    @staticmethod
    def __evaluate_grid(game: "Game", favor: PlayerState) -> float:
        grid = game.grid

        res = [0, 0]

        for player, enemy, r in zip(
            [FieldState.CROSS, FieldState.NOD],
            [FieldState.NOD, FieldState.CROSS],
            [0, 1],
        ):
            for i in range(grid.size):
                if all(grid[i, j] != enemy for j in range(grid.size)):
                    res[r] = max(
                        res[r], sum(grid[i, j] == player for j in range(grid.size))
                    )

                if all(grid[j, i] != enemy for j in range(grid.size)):
                    res[r] = max(
                        res[r], sum(grid[j, i] == player for j in range(grid.size))
                    )

            if all(grid[i, i] != enemy for i in range(grid.size)):
                res[r] = max(
                    res[r], sum(grid[i, i] == player for i in range(grid.size))
                )

            if all(grid[i, grid.size - 1 - i] != enemy for i in range(grid.size)):
                res[r] = max(
                    res[r],
                    sum(grid[i, grid.size - 1 - i] == player for i in range(grid.size)),
                )

        return res[0] - res[1] if favor == PlayerState.CROSS else res[1] - res[0]

    @staticmethod
    def __evaluate(
        game: "Game", depth: int, favor: PlayerState
    ) -> tuple[float, bool] | None:
        game_state = game.game_state

        if game_state == GameState.RUNNING:
            if (
                depth >= max(game.grid.size ** (1 / game.grid.size), 2)
                and game.grid.size > 3
            ):
                return AI3.__evaluate_grid(game, favor), True

            return None

        if game_state == GameState.DRAW:
            return 0, False

        if (game_state == GameState.CROSS_WIN and favor == PlayerState.CROSS) or (
            game_state == GameState.NOD_WIN and favor == PlayerState.NOD
        ):
            return game.grid.size**2 * 10 - depth, False

        return game.grid.size**2 * (-10) + depth, False

    @staticmethod
    def __alpha_pruner(alpha: float, beta: float, score: float) -> tuple[float, float]:
        return max(alpha, score), beta

    @staticmethod
    def __beta_pruner(alpha: float, beta: float, score: float) -> tuple[float, float]:
        return alpha, min(beta, score)

    def __minmax(
        self,
        game: "Game",
        depth: int,
        isMaximizing: bool,
        favor: PlayerState,
        alpha: float,
        beta: float,
    ) -> tuple[float, bool]:
        value = self.__evaluate(game, depth, favor)
        if value is not None:
            return value

        enemy = game.clone()
        enemy.is_player_cross = not game.is_player_cross

        score: float = -float("inf") if isMaximizing else float("inf")
        score_optimizer = max if isMaximizing else min
        score_pruner = self.__alpha_pruner if isMaximizing else self.__beta_pruner

        pruned = False

        for val, i, j in game.grid.iterator():
            if val != FieldState.EMPTY:
                continue

            enemy.grid[i, j] = game.ai_figure.to_field_state()

            new_score, pruned = self.__minmax_db(
                enemy,
                depth + 1,
                not isMaximizing,
                favor,
                alpha,
                beta,
            )

            score = score_optimizer(score, new_score)

            alpha, beta = score_pruner(alpha, beta, score)

            if beta <= alpha:
                return score, True

            enemy.grid[i, j] = FieldState.EMPTY

        return score, pruned

    def __minmax_db(
        self,
        game: "Game",
        depth: int,
        isMaximizing: bool,
        pfavor: PlayerState,
        alpha: float,
        beta: float,
    ) -> tuple[float, bool]:
        favor = 0 if pfavor == PlayerState.NOD else 1
        code = game.grid.code

        res = self.__db.execute(
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
            # print(depth, code, res[0], "cache")
            return res[0], False

        score, pruned = self.__minmax(game, depth, isMaximizing, pfavor, alpha, beta)

        if not pruned:
            # print(depth, code, score, alpha, beta)

            self.__db.execute(
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

        return score, pruned

    def decide(self, game: "Game") -> tuple[int, int]:
        with self.__db:

            opts: list[tuple[int, int]] = []
            score = -float("inf")

            enemy = game.clone()
            enemy.is_player_cross = not enemy.is_player_cross

            for val, i, j in game.grid.iterator():
                if val != FieldState.EMPTY:
                    continue

                enemy.grid[i, j] = game.ai_figure.to_field_state()

                new_score, _ = self.__minmax_db(
                    enemy, 0, False, game.ai_figure, -float("inf"), float("inf")
                )

                if new_score > score:
                    opts = [(i, j)]
                    score = new_score
                elif new_score == score:
                    opts.append((i, j))

                enemy.grid[i, j] = FieldState.EMPTY

            return choice(opts)
