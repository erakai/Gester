import pygame, random, time
from gester import sounds, Game, Entity, Rect, GestureInput
import config
from spawner import BoxSpawner

# TODO: spawn berries
# TODO: be able to grab berries and hold in your fist
# TODO: drop berries when you stop having a closed fist
# TODO: have pikachu eat the berries + play a certain noise
# TODO: use swiping to detect petting + have pikachu make a certain noise upon pet

game = Game()
score = 0

WIDTH = config.WIDTH
HEIGHT = config.HEIGHT

class HandHover(Rect):
    x = -100
    y = -100
    def start(self):
        self.position.set(self.x, self.y)
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

class Pikachu(Rect):
    test_var = True
    x = WIDTH // 3
    y = HEIGHT // 3
    moving_up = False
    moving_down = False
    moving_right = False
    moving_left = False
    last_tick = -1
    action_time = 1
    movement_amount = 1
    decision = -1

    new_action = True

    def __init__(self, *args):
        super().__init__(*args)
        self.attached_boxes = []

    def start(self):
        self.last_tick = round(time.perf_counter())
        sounds.create_sound("Pikachu", "games/assets/sounds/Pikachu.wav")
        self.position.set(self.x, self.y)
        self.size.set(100, 100)
        self.platform_image = pygame.image.load("games/assets/Pikachu.png")
        self.platform_image = pygame.transform.scale(
            self.platform_image, (self.size.get_width(), self.size.get_height())
        )
    
    def move(self, direction):
        global WIDTH, HEIGHT
        ma = self.movement_amount
        if direction == 0:
            # right
            if self.x + 100 > WIDTH:
                return
            self.x += ma
            self.position.set(self.x, self.y)
        elif direction == 1:
            # left
            if self.x - 20 < 0:
                return
            self.x -= ma
            self.position.set(self.x, self.y)
        elif direction == 2:
            # down
            if self.y + 120 > HEIGHT:
                return
            self.y += ma
            self.position.set(self.x, self.y)
        elif direction == 3:
            # up
            if self.y - 20 < 0:
                return
            self.y -= ma
            self.position.set(self.x, self.y)
        elif direction >= 4:
            # idle
            pass


    def think(self):
        cur_tick = round(time.perf_counter())

        # if enough time elapses, signify that it is time to make a new decision
        if abs(cur_tick - self.last_tick) > self.action_time:
            self.new_action = True
            self.last_tick = cur_tick
        else:
            self.move(self.decision)

        # make a decision
        if self.new_action:
            self.decision = random.randint(0,6)
            self.new_action = False

            # roll a die, 1/5 chance for Pika noise
            pika_chance = random.randint(0,4)
            if pika_chance == 0:
                sounds.play_sound("Pikachu")
            


    def render(self, screen):
        screen.blit(self.platform_image, (self.position.get_x(), self.position.get_y()))

class Background(Entity):
    def start(self):
        # raw_image = pygame.image.load("games/assets/slots/slot_machine.png")
        # self.booth = pygame.transform.scale(raw_image, (600, 660))
        raw_image = pygame.image.load("games/assets/pokemon_background.png")
        self.image = pygame.transform.scale(raw_image, (config.WIDTH, config.HEIGHT))
        
        # self.booth = pygame.transform.scale(raw_image, (600, 660))
        # self.image = pygame.image.load("games/assets/slots/background.jpeg")

    def think(self):
        pass

    def render(self, screen):
        screen.blit(self.image, (0, 0))

handhover = HandHover()
game.add_ent(Background())
game.add_ent(BoxSpawner(game.add_ent, 0, 0, handhover))
game.add_ent(handhover)
game.add_ent(Pikachu())


game.init(WIDTH, HEIGHT, False)