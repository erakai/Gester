import config
import pygame
from gester import Entity


class Scene(Entity):
    def __init__(self, get_score, *args):
        super().__init__(*args)
        self.get_score = get_score
        self.score_str = f"Score: {self.get_score()}"

    def start(self):
        background = pygame.image.load("games/assets/stacker-background.jpg")
        self.score_font = pygame.font.SysFont("Comic Sans MS", 30)
        self.background = pygame.transform.scale(
            background, (config.WIDTH, config.HEIGHT)
        )

    def think(self):
        if self.get_score() < 0:
            self.score_str = "GAME OVER!"
        else:
            self.score_str = f"Score: {self.get_score()}"

    def render(self, screen: pygame.Surface):
        screen.blit(self.background, (0, 0))
        score_text = self.score_font.render(self.score_str, False, (255, 255, 255))
        screen.blit(score_text, (20, 20))
