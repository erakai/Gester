import random
import math
from enum import Enum
from time import perf_counter

import pygame
from gester import Game, Entity, Rect, GestureInput
import config
from crosshair import Crosshair


class CasinoTile(Rect):
    def __init__(self, tile, column, speed, *args):
        super().__init__(*args)
        self.tile = tile
        self.column = column
        self.speed = speed

        loaded = pygame.image.load(self.tile.value[2])
        self.image = pygame.transform.scale(
            loaded, (self.size.get_width(), self.size.get_height())
        )

        if column == 0:
            self.position.set(config.FIRST_COL_X, 130)
        if column == 1:
            self.position.set(config.SECOND_COL_X, 130)
        if column == 2:
            self.position.set(config.THIRD_COL_X, 130)

        self.size.set(100, 100)

    def start(self):
        pass

    def think(self):
        if self.position.get_y() > 580:
            self.kill()

        self.position.set(self.position.get_x(), self.position.get_y() + self.speed)

    def render(self, screen):
        screen.blit(self.image, (self.position.get_x(), self.position.get_y()))


class WinningCasinoTile(Rect):
    def __init__(self, tile, column, speed, play_win, *args):
        super().__init__(*args)
        self.tile = tile
        self.column = column
        self.speed = speed
        self.play_win = play_win

        loaded = pygame.image.load(self.tile.value[2])
        self.image = pygame.transform.scale(
            loaded, (self.size.get_width(), self.size.get_height())
        )

        if column == 0:
            self.position.set(config.FIRST_COL_X, 130)
        if column == 1:
            self.position.set(config.SECOND_COL_X, 130)
        if column == 2:
            self.position.set(config.THIRD_COL_X, 130)

        self.size.set(100, 100)
        self.moving = True

    def start(self):
        pass

    def think(self):
        if self.moving and self.position.get_y() > config.HEIGHT / 2 - 115:
            self.play_win()
            self.moving = False

        if self.moving:
            self.position.set(self.position.get_x(), self.position.get_y() + self.speed)

    def render(self, screen):
        screen.blit(self.image, (self.position.get_x(), self.position.get_y()))
