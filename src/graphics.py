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

        self.__screen = pygame.display.set_mode((config.SIZE, config.SIZE))

    def __draw_line_round_corners(
        self,
        color: pygame.Color,
        pos1: tuple[float, float],
        pos2: tuple[float, float],
        width: float,
    ):
        pos1_v = pygame.math.Vector2(pos1)
        pos2_v = pygame.math.Vector2(pos2)

        lv = (pos2_v - pos1_v).normalize()
        lnv = pygame.math.Vector2(-lv.y, lv.x) * width // 2

        pts = [pos1_v + lnv, pos2_v + lnv, pos2_v - lnv, pos1_v - lnv]

        pygame.draw.polygon(self.__screen, color, pts)
        pygame.draw.circle(self.__screen, color, pos1, round(width / 2))
        pygame.draw.circle(self.__screen, color, pos2, round(width / 2))

    def __draw_grid(self, grid_size: int) -> None:
        delta = config.SIZE / grid_size

        for i in range(grid_size - 1):
            pygame.draw.line(
                self.__screen,
                config.GRID_COLOR,
                (delta + delta * i, 0),
                (delta + delta * i, config.SIZE),
                round(config.SIZE * config.GRID_SCALE),
            )

            pygame.draw.line(
                self.__screen,
                config.GRID_COLOR,
                (0, delta + delta * i),
                (config.SIZE, delta + delta * i),
                round(config.SIZE * config.GRID_SCALE),
            )

    def __draw_nod(
        self, coords: tuple[int, int], color: pygame.Color, grid_size: int
    ) -> None:
        delta = config.SIZE / grid_size
        diameter = delta * config.DIAMETER_SCALE
        line_width = round(delta / 10)

        pygame.draw.circle(
            self.__screen,
            color,
            (delta / 2 + delta * coords[0], delta / 2 + delta * coords[1]),
            diameter / 2,
            line_width,
        )

    def __draw_cross(
        self, coords: tuple[int, int], color: pygame.Color, grid_size: int
    ) -> None:
        delta = config.SIZE / grid_size
        diameter = delta * config.DIAMETER_SCALE
        line_width = round(delta / 10)

        self.__draw_line_round_corners(
            color,
            (
                coords[0] * delta + delta - diameter,
                coords[1] * delta + delta - diameter,
            ),
            (coords[0] * delta + diameter, coords[1] * delta + diameter),
            line_width,
        )

        self.__draw_line_round_corners(
            color,
            (coords[0] * delta + delta - diameter, coords[1] * delta + diameter),
            (coords[0] * delta + diameter, coords[1] * delta + delta - diameter),
            line_width,
        )

    def mouse_quadrant(self, grid_size: int) -> tuple[int, int]:
        mouse_pos = pygame.mouse.get_pos()
        mouse_qadrant = tuple(x * grid_size // config.SIZE for x in mouse_pos)

        return mouse_qadrant

    def redraw(self, game: "Game", auto: bool) -> None:
        self.__screen.fill(config.BACKGROUND_COLOR)

        self.__draw_grid(game.grid.size)

        for val, x, y in game.grid.iterator():
            if val == FieldState.NOD:
                self.__draw_nod((x, y), config.NOD_COLOR, game.grid.size)
            elif val == FieldState.CROSS:
                self.__draw_cross((x, y), config.CROSS_COLOR, game.grid.size)

        if game.game_state == GameState.RUNNING:
            mouse_color = (
                config.NOD_COLOR
                if game.player_figure == PlayerState.NOD
                else config.CROSS_COLOR
            )

            mouse_color = pygame.Color(
                mouse_color.r // 2, mouse_color.g // 2, mouse_color.b // 2, 128
            )

            x, y = self.mouse_quadrant(game.grid.size)

            if not auto and game.grid[x, y] == FieldState.EMPTY:
                if game.player_figure == PlayerState.NOD:
                    self.__draw_nod((x, y), mouse_color, game.grid.size)
                else:
                    self.__draw_cross((x, y), mouse_color, game.grid.size)

        pygame.display.flip()
