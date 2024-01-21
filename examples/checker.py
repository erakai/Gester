from gester import Game, Entity, GestureInput

WIDTH = 1280
HEIGHT = 720

game = Game()

class Checker(Entity):
    def start(self): pass
    def render(self, surface): pass

    def think(self):
        print(GestureInput.get_hand_gesture())
        print(GestureInput.get_hand_pos_x())

game.add_ent(Checker())

game.init(WIDTH, HEIGHT)
