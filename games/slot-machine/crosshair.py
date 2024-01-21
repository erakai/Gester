from gester import Rect, GestureInput
import pygame
import config


class Crosshair(Rect):
    def start(self):
        self.position.set(-100, -100)

        open = pygame.image.load("games/assets/open_hand.png")
        self.open_hand = pygame.transform.scale(
            open, (config.CROSSHAIR_SIZE, config.CROSSHAIR_SIZE)
        )
        closed = pygame.image.load("games/assets/closed_hand.png")
        self.closed_hand = pygame.transform.scale(
            closed, (config.CROSSHAIR_SIZE, config.CROSSHAIR_SIZE)
        )

        self.open = False
        self.hand_x = -100
        self.hand_y = -100

    def update_input(self, x, y, open):
        self.hand_x = x
        self.hand_y = y
        self.open = open

    def think(self):
        if self.hand_x > 0 or self.hand_y > 0:
            self.position.set(self.hand_x, self.hand_y)

    def render(self, screen):
        if self.open:
            screen.blit(self.open_hand, (self.position.get_x(), self.position.get_y()))
        else:
            screen.blit(
                self.closed_hand, (self.position.get_x(), self.position.get_y())
            )
