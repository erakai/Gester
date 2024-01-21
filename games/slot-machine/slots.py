from gester import Game, Entity, Rect, GestureInput
import config
from crosshair import Crosshair

game = Game()


class Casino(Entity):
    def __init__(self, crosshair, *args):
        super().__init__(*args)
        self.crosshair = crosshair

        self.animation_playing = False
        self.animation_start = -1
        self.slot_rows = []

    def start(self):
        pass

    def start_spin(self):
        if self.animation_playing:
            return

        self.animation_playing

    def think(self):
        hand_x = GestureInput.get_hand_pos_x()
        hand_y = GestureInput.get_hand_pos_y()
        gesture = GestureInput.get_hand_gesture()
        self.crosshair.update_input(hand_x, hand_y, (gesture != "CLOSED_FIST"))

    def render(self, screen):
        pass


crosshair = Crosshair()
game.add_ent(Casino(crosshair))
game.add_ent(crosshair)

game.init(config.WIDTH, config.HEIGHT, False)
