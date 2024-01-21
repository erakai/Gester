from gester import *
from gester.attributes import Point, Size
import time

game = Game()

Simon = SimonSays(Size("size", 1280, 120), Point("position", 0, 0))

# banner
game.add_ent(Simon)

game.init(1280, 720, True)