from gester import Rect, GestureInput
import pygame
import config


class Crosshair(Rect):
    def __init__(self, on_handle_pulled, *args):
        super().__init__(*args)
        self.on_handle_pulled = on_handle_pulled

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

        self.closed_at = (-1, -1)

    def update_input(self, x, y, open):
        self.hand_x = x
        self.hand_y = y

        if self.open and not open:
            self.closed_at = (x, y)
        elif not self.open and open:
            if (
                self.closed_at[0] < 950
                and self.closed_at[0] > 820
                and self.closed_at[1] > 55
                and self.closed_at[1] < 155
                and x < 1100
                and x > 700
                and y > 200
            ):
                self.on_handle_pulled()

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
