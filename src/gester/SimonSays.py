import pygame
import time

from gester import Entity, Game
from gester.attributes import Point, Size, Color, has_attrs


class SimonSays(Entity):
    position: Point
    size: Size
    color: Color
    text = "Loading"
    started = False
    start_time = None
    last_tick = None
    gestures = ["OPEN HAND", "CLOSED_FIST", "INDEX_EXTENDED", "NO_HAND", "PEACE_SIGN",
                        "RING_EXTENDED", "MIDDLE_EXTENDED", "PINKY_EXTENDED", "THUMB_EXTENDED"]

    @has_attrs(("position", Point), ("size", Size), ("color", Color))
    def __init__(self, *args):
        super().__init__()

    def start(self):
        # initialize timer
        self.start_time = round(time.perf_counter())
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
        # new_str = self.text + "a"
        # self.setText(new_str)

        # --Set Up--
        # For the first 5 seconds just say "Simon Says starting in: [remaining seconds]"
        if self.start_time + 5 < round(time.perf_counter()):
            self.started = True

        if not self.started:
            # display the text with the countdown
            time_to_start = (self.start_time + 5) - round(time.perf_counter())
            display_string = "Simon Says starting in: " + str(time_to_start)
            self.setText(display_string)
        else: 
            # --started--
            # now it has started
            # pick a random gesture out of the set (create some maybe)
            # display the name with either "Simon says [name]" or just "[name]"
            # gestures = ["OPEN HAND", "CLOSED_FIST", "INDEX_EXTENDED", "NO_HAND", "PEACE_SIGN",
            #             "RING_EXTENDED", "MIDDLE_EXTENDED", "PINKY_EXTENDED", "THUMB_EXTENDED"]
            

            # display counting down timer
            # once it hits zero check the current gesture
            # if it's the same gesture and the text didn't say "Simon Says" then show "Simon didn't say go!"
            # otherwise show "you did it!"
            
            # show name of gesture
            # display counting down timer

            # once it hits 0 then check the current hand gesture
            
            # check if timer done
            # if so then check hand gesture, if correct say "good job" otherwise say "that was not quite it"
            # reinitilize timer and 
            # if timer isn't done, display how many seconds remaining until it will check
            pass
