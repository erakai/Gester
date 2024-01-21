import random
import math
from enum import Enum
from time import perf_counter

import pygame
from gester import Game, Entity, Rect, GestureInput, sounds
import config
from crosshair import Crosshair
from tiles import CasinoTile, WinningCasinoTile

game = Game()


# weight, bonus, path
SlotTotal = 250 + 250 + 125 + 125 + 50 + 50 + 25 + 25 + 10 + 2


class SlotTile(Enum):
    LEMON = (250, 1, "games/assets/slots/banana.png")
    ORANGE = (250, 1, "games/assets/slots/orange.png")
    GRAPE = (125, 5, "games/assets/slots/grape.png")
    WATERMELON = (125, 5, "games/assets/slots/watermelon.png")
    BANANA = (50, 5, "games/assets/slots/banana.png")
    CHERRY = (50, 10, "games/assets/slots/cherry.png")
    SEVEN = (25, 25, "games/assets/slots/seven.png")
    BELL = (25, 50, "games/assets/slots/bell.png")
    BAR = (10, 100, "games/assets/slots/bar.png")
    DIAMOND = (2, 1000, "games/assets/slots/diamond.png")


def calculate_outcome():
    if random.random() < config.CHANCE_OF_TRIPLE:
        return ([generate_tile()] * 3, True)
    return ([generate_tile(), generate_tile(), generate_tile()], False)


def generate_tile() -> SlotTile:
    chosen = random.randint(0, SlotTotal)
    count = 0
    for tile in SlotTile:
        count += tile.value[0]
        if chosen <= count:
            return tile


class Background(Entity):
    def start(self):
        self.image = pygame.image.load("games/assets/slots/background.jpeg")

    def think(self):
        pass

    def render(self, screen):
        screen.blit(self.image, (0, 0))


class Casino(Entity):
    def __init__(self, add_ent, *args):
        super().__init__(*args)
        self.add_ent = add_ent

        self.animation_playing = False
        self.animation_start = -1
        self.last_dispatch = -1
        self.total_dispatches = 0
        self.win = False
        self.existing_tiles = []

        self.hand_x = -1
        self.hand_y = -1

    def start(self):
        raw_image = pygame.image.load("games/assets/slots/slot_machine.png")
        self.booth = pygame.transform.scale(raw_image, (600, 660))
        self.display_font = pygame.font.SysFont("Comic Sans MS", 20)

        self.crosshair = Crosshair(self.start_spin)
        game.add_ent(self.crosshair)

        sounds.create_sound(
            "lever-crank", "games/assets/sounds/lever-crank.wav", volume=1.5
        )
        sounds.create_sound(
            "casino-ambience", "games/assets/sounds/casino-ambiance.mp3", volume=2
        )
        sounds.create_sound("big-win", "games/assets/sounds/big-win.mp3", volume=3)
        sounds.create_sound(
            "regular-win", "games/assets/sounds/regular-win.mp3", volume=1.5
        )
        sounds.create_sound(
            "slot-machine", "games/assets/sounds/slot-machine.wav", volume=0.05
        )

        sounds.start_looping_sound("casino-ambience")

    def play_win(self):
        if self.win:
            if self.existing_tiles[0].tile.value[1] > 25:
                sounds.play_sound("big-win")
            else:
                sounds.play_sound("regular-win")

    def start_spin(self):
        sounds.play_sound("lever-crank")
        if self.animation_playing:
            return

        self.animation_playing = True
        self.animation_start = perf_counter()
        self.dispatch_tiles()
        self.last_dispatch = perf_counter()
        self.total_dispatches = 0
        self.win = False

        for tile in self.existing_tiles:
            tile.kill()
        self.existing_tiles = []

    def calc_speed(self):
        speed = config.TILE_SPEED / ((perf_counter() - self.animation_start) - 1)
        return speed

    def dispatch_winning_tiles(self):
        tiles, win = calculate_outcome()
        self.win = win
        for i, tile in enumerate(tiles):
            winner = WinningCasinoTile(tile, i, self.calc_speed(), self.play_win)
            self.existing_tiles.append(winner)
            self.add_ent(winner, index=1)

    def dispatch_tiles(self):
        sounds.play_sound("slot-machine")
        self.total_dispatches += 1
        tiles = [generate_tile(), generate_tile(), generate_tile()]
        for i, tile in enumerate(tiles):
            speed = self.calc_speed()
            if speed < 0:
                speed = speed * -1
            self.add_ent(CasinoTile(tile, i, speed), index=1)

    def think(self):
        self.hand_x = GestureInput.get_hand_pos_x()
        self.hand_y = GestureInput.get_hand_pos_y()
        gesture = GestureInput.get_hand_gesture()
        self.crosshair.update_input(
            self.hand_x, self.hand_y, (gesture != "CLOSED_FIST")
        )

        if self.animation_playing:
            now = perf_counter()
            if (1000 * (now - self.last_dispatch)) > config.TIME_BETWEEN_TILES_MS + (
                45 * self.total_dispatches
            ):
                if 1000 * (now - self.animation_start) > config.TIME_OF_SPIN_MS:
                    self.dispatch_winning_tiles()
                    self.animation_playing = False
                else:
                    self.dispatch_tiles()
                    self.last_dispatch = now

    def render(self, screen):
        screen.blit(self.booth, (350, 50))


game.add_ent(Background())
game.add_ent(Casino(game.prefix_ent))

game.init(config.WIDTH, config.HEIGHT, False)
