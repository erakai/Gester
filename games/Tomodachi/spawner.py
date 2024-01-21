from time import perf_counter
import random

import pygame

from gester import Entity, Rect, sounds
import config
from gester.attributes import Point, Size


class BoxSpawner(Entity):
    def __init__(self, add_ent, get_score, update_score, platform, *args):
        super().__init__(*args)
        self.add_ent = add_ent
        self.get_score = get_score
        self.update_score = update_score
        self.platform = platform

    def start(self):
        berry_image = pygame.image.load("games/assets/berry.png")
        self.berry_image = berry_image
        self.last_spawned = perf_counter()

    def think(self):
        # if self.get_score() < 0:
        #     return

        cur = perf_counter()
        if (1000 * (cur - self.last_spawned)) > config.TIME_BETWEEN_BOXES_MS:
            if config.TIME_BETWEEN_BOXES_MS > 50:
                config.TIME_BETWEEN_BOXES_MS -= config.TIME_DECREMENT_PER_BOX_MS
            self.spawn()
            self.last_spawned = cur

    def render(self, screen):
        pass

    def spawn(self):
        spawn_x = random.randint(35, config.WIDTH - 35)
        spawn_y = random.randint(35, config.HEIGHT - 35)
        self.add_ent(
            Box(
                self.berry_image,
                self.update_score,
                self.platform,
                Point("position", spawn_x, spawn_y),
                Size("size", 35, 35),
            )
        )


class Box(Rect):
    def __init__(self, berry_image, update_score, platform, *args):
        super().__init__(*args)
        self.berry_image = pygame.transform.scale(
            berry_image, (self.size.get_width(), self.size.get_height())
        )
        self.update_score = update_score
        self.fixed = False
        self.platform = platform
        sounds.create_sound("box", "games/assets/sounds/pika.wav")

    def start(self):
        pass

    def think(self):
        # if self.position.get_y() > config.HEIGHT:
        #     self.update_score(decrement=True)
        #     self.kill()

        if not self.fixed:
            # self.position.set(
            #     self.position.get_x(), self.position.get_y() + config.BOX_SPEED
            # )
            
            self.position.set(
                self.position.get_x(), self.position.get_y()
            )

            # for box in self.platform.attached_boxes:
            #     if self.check_collision(box):
            #         self.fix()
            if self.check_collision(self.platform):
                self.eaten()

    # fix()
    def eaten(self):
        sounds.play_sound("box")
        self.kill()

    def check_collision(self, entity: Rect):
        x = self.position.get_x()
        y = self.position.get_y()
        width = self.size.get_width()
        height = self.size.get_height()

        px = entity.position.get_x()
        pwidth = entity.size.get_width()

        if (y + height) >= entity.position.get_y() - 1 and (
            y + height
        ) <= entity.position.get_y() + 15:
            if (x <= px + pwidth and x >= px) or (
                px + pwidth >= x + width and x + width >= px
            ):
                return True
        return False

    def render(self, screen: pygame.Surface):
        screen.blit(self.berry_image, (self.position.get_x(), self.position.get_y()))
