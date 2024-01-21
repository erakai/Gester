import pygame
from gester import Game, Entity, Rect, GestureInput

game = Game()
score = 0

WIDTH = 1080
HEIGHT = 720

class HandHover(Rect):
    def start(self):
        self.position.set(-100, -100)
        self.trans_surface = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
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

game.add_ent(HandHover())

game.init(WIDTH, HEIGHT, False)