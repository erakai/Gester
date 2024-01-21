from gester import *
from gester import GestureInput

WIDTH = 1280
HEIGHT = 720

game = Game()

class HandFollower(Rect):
	def __init__(self, *args):
		super().__init__(*args)

	def start(self):
		self.size.set(20, 20)

	def think(self):
		x = GestureInput.get_hand_pos_x()
		y = GestureInput.get_hand_pos_y()

		self.position.set(x, y)

	def on_swipe(self, swipe: str):
		print("Swipe! from " + swipe)

swipe_detector = SwipeDetector()
game.add_ent(swipe_detector)

hand_follower = HandFollower()

swipe_detector.hook_ent(hand_follower)
game.add_ent(hand_follower)

game.init(WIDTH, HEIGHT, True)
