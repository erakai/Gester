from gester import *
from gester.attributes import Point, Size

game = Game()

rect = Rect(Size("size", 200, 200), Point("position", 400, 400))
game.add_ent(rect)

game.init()