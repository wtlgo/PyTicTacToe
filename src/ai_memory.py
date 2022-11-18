from ai_alphabeta import AIAlphaBeta
from states import FieldState, PlayerState
from typing import TYPE_CHECKING
import sqlite3

if TYPE_CHECKING:
    from game import Game


class AIMemory(AIAlphaBeta):
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
                        score REAL
                    );
                """
            )

    def _code(self, game: "Game") -> int:
        res = 0

        for row in game.field:
            for val in row:
                res *= 3
                res += (
                    0 if val == FieldState.EMPTY else 1 if val == FieldState.NOD else 2
                )

        return res

    def _minmax(
        self, game: "Game", depth: int, isMaximizing: bool, pfavor: PlayerState
    ) -> float:
        with self._db:
            favor = 0 if pfavor == PlayerState.NOD else 1
            code = self._code(game)

            res = self._db.execute(
                """
                    SELECT score FROM MEMORY
                    WHERE code=:code AND favor=:favor AND
                          is_maximizing=:is_maximizing
                """,
                {
                    "code": code,
                    "favor": favor,
                    "is_maximizing": isMaximizing,
                },
            ).fetchone()

            if res is not None:
                return res[0]

            score = super()._minmax(game, depth, isMaximizing, pfavor)

            self._db.execute(
                """
                    INSERT INTO MEMORY(code, favor, is_maximizing, score)
                    VALUES(:code, :favor, :is_maximizing, :score)
                """,
                {
                    "code": code,
                    "favor": favor,
                    "is_maximizing": isMaximizing,
                    "score": score,
                },
            )

            return score
