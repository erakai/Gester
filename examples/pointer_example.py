from gester import Game, Entity, GestureInput

WIDTH = 1280
HEIGHT = 720


class Checker(Entity):
    def start(self):
        pass

    def think(self):
        print(GestureInput.get_pointer_x())

    def render(self, surface):
        pass


game = Game()

game.add_ent(Checker())
game.init(WIDTH, HEIGHT)
