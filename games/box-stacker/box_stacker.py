import pygame
from gester import Game, Entity, Rect, GestureInput
from scene import Scene
from spawner import BoxSpawner
import config

game = Game()
score = 1


def get_score():
    return score


def update_score(decrement=False):
    global score
    score = score + (1 if not decrement else -1)


class HandHover(Rect):
    def start(self):
        self.position.set(-100, -100)
        self.trans_surface = pygame.Surface(
            (config.WIDTH, config.HEIGHT), pygame.SRCALPHA
        )

    def think(self):
        hand_x = GestureInput.get_hand_pos_x()
        hand_y = GestureInput.get_hand_pos_y()
        if hand_x > 0 or hand_y > 0:
            self.position.set(hand_x, hand_y)

    def render(self, screen):
        global score
        if score >= 0:
            self.trans_surface.fill((0, 0, 0, 0))
            pygame.draw.circle(
                self.trans_surface,
                (232, 9, 225, 90),
                (self.position.get_x(), self.position.get_y()),
                40,
            )
            screen.blit(self.trans_surface, (0, 0))


class Platform(Rect):
    def __init__(self, *args):
        super().__init__(*args)
        self.attached_boxes = []

    def start(self):
        self.position.set(300, 600)
        self.size.set(250, 50)
        self.platform_image = pygame.image.load("games/assets/platform.png")
        self.platform_image = pygame.transform.scale(
            self.platform_image, (self.size.get_width(), self.size.get_height())
        )

    def think(self):
        global score
        if score < 0:
            return

        hand_x = GestureInput.get_hand_pos_x()
        dist = (self.position.get_x() + (self.size.get_width() / 2)) - hand_x

        speed = 0
        if dist > 5 and self.position.get_x() > 0:
            speed = -1 * config.PLATFORM_SPEED
        elif dist < -5 and self.position.get_x() + self.size.get_width() < config.WIDTH:
            speed = config.PLATFORM_SPEED

        self.position.set(self.position.get_x() + speed, self.position.get_y())
        for box in self.attached_boxes:
            box.position.set(box.position.get_x() + speed, box.position.get_y())

    def attach_box(self, box):
        global score
        self.attached_boxes.append(box)
        if box.position.get_y() < 0:
            update_score(decrement=True)

    def render(self, screen):
        screen.blit(self.platform_image, (self.position.get_x(), self.position.get_y()))


platform = Platform()
game.add_ent(Scene(get_score))
game.add_ent(BoxSpawner(game.add_ent, get_score, update_score, platform))
game.add_ent(HandHover())
game.add_ent(platform)

game.init(config.WIDTH, config.HEIGHT, False)
