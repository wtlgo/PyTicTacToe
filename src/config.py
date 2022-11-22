from typing import Final
import pygame


class Config:
    SIZE: Final = 500

    GRID_SIZE: Final = 4

    BACKGROUND_COLOR: Final = pygame.Color(0, 0, 0)
    GRID_COLOR: Final = pygame.Color(255, 0, 0)
    NOD_COLOR: Final = pygame.Color(0, 255, 0)
    CROSS_COLOR: Final = pygame.Color(0, 0, 255)

    DIAMETER_SCALE: Final = 0.8
    GRID_SCALE: Final = 0.02

    WINDOW_TITLE: Final = "Tic-Tac-Toe"


config = Config()
