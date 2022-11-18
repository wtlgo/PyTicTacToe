from states import FieldState, GameState, PlayerState
from config import config
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game


class Graphics:
    def __init__(self) -> None:
        pygame.display.set_caption(config.WINDOW_TITLE)

        logo = pygame.Surface((32, 32))
        pygame.draw.circle(logo, config.NOD_COLOR, (16, 16), 12, 3)

        pygame.display.set_icon(logo)

        self._screen = pygame.display.set_mode((config.SIZE, config.SIZE))

    def _draw_grid(self) -> None:
        delta = config.SIZE / 3

        for i in range(2):
            pygame.draw.line(
                self._screen,
                config.GRID_COLOR,
                (delta + delta * i, 0),
                (delta + delta * i, config.SIZE),
                round(config.SIZE * config.GRID_SCALE),
            )

            pygame.draw.line(
                self._screen,
                config.GRID_COLOR,
                (0, delta + delta * i),
                (config.SIZE, delta + delta * i),
                round(config.SIZE * config.GRID_SCALE),
            )

    def _draw_nod(self, coords: tuple[int, int], color: pygame.Color) -> None:
        delta = config.SIZE / 3
        diameter = delta * config.DIAMETER_SCALE
        line_width = round(delta / 10)

        pygame.draw.circle(
            self._screen,
            color,
            (delta / 2 + delta * coords[0], delta / 2 + delta * coords[1]),
            diameter / 2,
            line_width,
        )

    def _draw_cross(self, coords: tuple[int, int], color: pygame.Color) -> None:
        delta = config.SIZE / 3
        diameter = delta * config.DIAMETER_SCALE
        line_width = round(delta / 10)

        pygame.draw.line(
            self._screen,
            color,
            (
                coords[0] * delta + delta - diameter,
                coords[1] * delta + delta - diameter,
            ),
            (coords[0] * delta + diameter, coords[1] * delta + diameter),
            line_width,
        )

        pygame.draw.line(
            self._screen,
            color,
            (coords[0] * delta + delta - diameter, coords[1] * delta + diameter),
            (coords[0] * delta + diameter, coords[1] * delta + delta - diameter),
            line_width,
        )

    @property
    def mouse_quadrant(self) -> tuple[int, int]:
        mouse_pos = pygame.mouse.get_pos()
        mouse_qadrant = tuple(x * 3 // config.SIZE for x in mouse_pos)

        return mouse_qadrant

    def redraw(self, game: "Game") -> None:
        self._screen.fill(config.BACKGROUND_COLOR)

        self._draw_grid()

        for x, row in enumerate(game.field):
            for y, val in enumerate(row):
                if val == FieldState.NOD:
                    self._draw_nod((x, y), config.NOD_COLOR)
                elif val == FieldState.CROSS:
                    self._draw_cross((x, y), config.CROSS_COLOR)

        if game.game_state == GameState.RUNNING:
            mouse_color = (
                config.NOD_COLOR
                if game.player_figure == PlayerState.NOD
                else config.CROSS_COLOR
            )

            mouse_color = pygame.Color(
                mouse_color.r // 2, mouse_color.g // 2, mouse_color.b // 2, 128
            )

            x, y = self.mouse_quadrant

            if game.field[x][y] == FieldState.EMPTY:
                if game.player_figure == PlayerState.NOD:
                    self._draw_nod(self.mouse_quadrant, mouse_color)
                else:
                    self._draw_cross(self.mouse_quadrant, mouse_color)

        pygame.display.flip()
