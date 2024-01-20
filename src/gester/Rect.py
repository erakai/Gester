import pygame

from gester import Entity, Game
from gester.attributes import Point, Size, Color, has_attrs


class Rect(Entity):
    position: Point
    size: Size
    color: Color

    @has_attrs(("position", Point), ("size", Size), ("color", Color))
    def __init__(self, *args):
        super().__init__()

    def start(self):
        pass

    def render(self, surface: pygame.Surface):
        color = pygame.Color(
            self.color.get_red(),
            self.color.get_green(),
            self.color.get_blue(),
            self.color.get_alpha(),
        )
        pygame.draw.rect(
            surface,
            color,
            pygame.Rect(
                self.position.get_x(),
                self.position.get_y(),
                self.size.get_width(),
                self.size.get_height(),
            ),
        )

    def think(self):
        x = self.position.get_x()
        y = self.position.get_y()

        self.position.set(x + 10, y)
        pass
