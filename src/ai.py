from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class AI(ABC):
    def decide(self, game: "Game") -> tuple[int, int]:
        return 0, 0
