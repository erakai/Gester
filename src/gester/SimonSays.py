import pygame
import time
import random

from gester import Entity, Game, GestureInput
from gester.attributes import Point, Size, Color, has_attrs


# make gestures more accurate half-DONZERONI
# add score counter DONZERONI
# TODO: decrease time over time, no floor goes all the way to milliseconds 
# TODO: make it take 10 and choose the highest match

# probably should've made display string a class member huh

# 1:52 AM - get_gesture 


class SimonSays(Entity):
    position: Point
    size: Size
    color: Color
    text = "Loading"
    started = False
    game_in_progress = False
    start_time = None
    time_to_move = 2
    gestures = ["OPEN_HAND", "CLOSED_FIST", "INDEX_EXTENDED", "MIDDLE_EXTENDED", "PINKY_EXTENDED"]
    min_value = 0
    max_value = len(gestures) - 1
    simon_said = False
    next_gest = 0
    games_played = 0
    end_turn = False
    score = 0
    guess_correct = False
    go_next = False
    hash_table = None # Used to match a gesture to its index in occurences
    occurences = [0] * (max_value + 2)

    @has_attrs(("position", Point), ("size", Size), ("color", Color))
    def __init__(self, *args):
        super().__init__()

    def start(self):
        self.start_time = round(time.perf_counter())
        self.gen_next_move()
        self.gen_simon_choice()
        self.init_hash()
        pass

    def init_hash(self):
        self.hash_table = {}

        for i in range(len(self.gestures)):
            self.hash_table[self.gestures[i]] = i

    # call this inside of think if you want the text to change
    # it might be useful to user a timer depending on what you are trying to do
    def setText(self, inputString):
        self.text = inputString

    def gen_next_move(self):
        self.next_gest = random.randint(self.min_value, self.max_value)
    
    def gen_simon_choice(self):
        choice = random.randint(0, 1)
        if choice == 0:
            self.simon_said = True
        else:
            self.simon_said = False
    
    def get_score_string(self):
        return " Score: " + str(self.score)

    def make_faster(self):
        print(self.time_to_move)
        self.time_to_move -= (0.1)
        self.time_to_move = max(self.time_to_move, 1)
    
    def reset(self):
        self.guess_correct = False
        self.gen_next_move()
        self.gen_simon_choice()
        self.games_played += 1
        self.game_in_progress = False
        self.wl_screen = True
        self.go_next = False
        self.end_turn = False
        self.occurences = [0] * (self.max_value + 1)
        # self.make_faster()

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
        if self.start_time + self.time_to_move <= round(time.perf_counter()):
            self.started = True

        if not self.started:
            # display the text with the countdown
            time_to_start = (self.start_time + self.time_to_move) - round(time.perf_counter(), 2)
            time_to_start = f"{time_to_start:.2f}"
            display_string = "Simon Says starting in: " + str(time_to_start) + self.get_score_string()
            self.setText(display_string)
        else:
            # --started--
            # gestures = ["OPEN HAND", "CLOSED_FIST", "INDEX_EXTENDED", "PEACE_SIGN",
            #             "RING_EXTENDED", "MIDDLE_EXTENDED", "PINKY_EXTENDED", "THUMB_EXTENDED"]
            # game_in_progress, next_move

            if (self.start_time + (self.time_to_move * ((2 * self.games_played) + 2))) - round(time.perf_counter()) < 1:
                self.game_in_progress = True

            if not self.game_in_progress:
                # display the text with the countdown
                time_to_start = (self.start_time + (self.time_to_move * ((2 * self.games_played) + 2))) - round(time.perf_counter(), 2)
                time_to_start = f"{time_to_start:.2f}"
                
                rand_gest = self.gestures[self.next_gest]

                if self.simon_said:
                    display_string = "Simon Says Do: " + rand_gest + " in: " + str(time_to_start)
                else:
                    display_string = "Do: " + rand_gest + " in: " + str(time_to_start)

                self.setText(display_string + self.get_score_string())
            else:
                # if to change time after 3 more seconds pass
                if (self.start_time + (self.time_to_move * ((2 * self.games_played) + 3))) - round(time.perf_counter()) < 1:
                    self.go_next = True

                if not self.end_turn:
                    closest_gesture = ""
                    for i in range(10):
                        # print("image captured")
                        get_gesture = GestureInput.get_hand_gesture()
                        closest_gesture = GestureInput.get_hand_gesture()
                        # print("get gesture: " + str(get_gesture))
                        if get_gesture in self.gestures:
                            # print("index being added to: " + str(self.hash_table[get_gesture]))
                            # for key, value in self.hash_table.items():
                            #     print(f"Key: {key}, Value: {value}")
                            self.occurences[self.hash_table[get_gesture]] += 1
                        else:
                            self.occurences[len(self.occurences) - 1] += 1

                    
                    max_val = max(self.occurences)
                    max_index = self.occurences.index(max_val)

                    if max_index == len(self.occurences) - 1:
                        closest_gesture = ""
                    else:
                        closest_gesture = self.gestures[max_index]
                    # for key, value in self.hash_table.items():
                    #     print(f"Key: {key}, Value: {value}")

                    # print("occurences: " + str(self.occurences))
                    # print("max val: " + str(max_val))
                    # print("max index: " + str(max_index))
                    # print("read: " + str(closest_gesture))
                    # print("Expected: " + str(self.gestures[self.next_gest]))

                    if closest_gesture == self.gestures[self.next_gest]:
                        if self.simon_said:
                            display_string = "You did it!"
                            self.guess_correct = True
                        else:
                            display_string = "Simon didn't say to do that!"
                    else:
                        if not self.simon_said:
                            display_string = "You did it!"
                            self.guess_correct = True
                        else:
                            display_string = "That wasn't quite right!"
                    
                    # if self.simon_said:
                    #     print("simon said")
                    # else:
                    #     print("simon didn't say")

                    if self.guess_correct:
                        self.score += 1
                    #     print("point given")
                    # else:
                    #     print("point not given")
                    self.setText(display_string + self.get_score_string())

                    self.end_turn = True
                elif self.go_next:
                    self.reset()