import pygame
import time

from gester import Entity, Game
from gester.attributes import Point, Size, Color, has_attrs


class Text(Entity):
    position: Point
    size: Size
    color: Color
    text = "Default Text"

    @has_attrs(("position", Point), ("size", Size), ("color", Color))
    def __init__(self, *args):
        super().__init__()

    def start(self):
        pass

    # call this inside of think if you want the text to change
    # it might be useful to user a timer depending on what you are trying to do
    def setText(self, inputString):
        self.text = inputString

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

        # Setting up the font
        font = pygame.font.SysFont('Comic Sans MS', 30)
        
        # Render the text
        text_color = (255, 255, 255)  # Change this to your desired text color, different from the rectangle color
        text_surface = font.render(self.text, True, text_color)
        
        # Positioning the text
        text_rect = text_surface.get_rect(center=(self.position.get_x() + self.size.get_width() // 2,
                                                self.position.get_y() + self.size.get_height() // 2))

        # Drawing the text
        surface.blit(text_surface, text_rect)

    def think(self):
        pass
