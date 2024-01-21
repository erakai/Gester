import pygame
import time

from gester import Entity, Game
from gester.attributes import Point, Size, Color, has_attrs


class Text(Entity):
    position: Point
    size: Size
    color: Color
    text = "Default Text"
    text_color : Color

    @has_attrs(("position", Point), ("size", Size), ("color", Color), ("text_color", Color))
    def __init__(self, *args):
        super().__init__()

    def start(self):
        pass

    # call this inside of think if you want the text to change
    # it might be useful to user a timer depending on what you are trying to do
    def setText(self, inputString):
        self.text = inputString

    def render(self, surface: pygame.Surface):
        # Setting up the font
        font = pygame.font.SysFont('Comic Sans MS', 30)
        
        # Render the text
        text_surface = font.render(self.text, True, self.text_color.to_pygame())
        
        # Positioning the text
        text_rect = text_surface.get_rect(center=(self.position.get_x() + self.size.get_width() // 2,
                                                self.position.get_y() + self.size.get_height() // 2))

        # Drawing the text
        surface.blit(text_surface, text_rect)

    def think(self):
        pass
