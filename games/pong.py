import random

from gester import *
from gester import GestureInput
from gester.attributes import Point, Size

game = Game()

WIDTH = 1280
HEIGHT = 720

SPEED = 8

class Ball(Rect):
	speed_x : int = 0
	speed_y : int = 0

	def start(self):
		self.position.set(WIDTH/2, HEIGHT/2)
		self.size.set(50, 50)

		self.speed_x = random.randint(5, 10)
		self.speed_y = random.randint(2, 5)
		pass

	def think(self):
		x = self.position.get_x()
		y = self.position.get_y()

		# left out-of-bound
		if (x + 25 < 100):
			self.start()
			return

		if (x - 25 > WIDTH - 100):
			self.start()
			return

		self.position.set(x + self.speed_x, y + self.speed_y)

	def on_collide(self, obj):
		x = self.position.get_x()
		y = self.position.get_y()		
		# right paddle
		if (isinstance(obj, Enemy)):
			self.speed_x = -self.speed_x

		if (isinstance(obj, Player)):
			self.speed_x = -self.speed_x

		if (isinstance(obj, Bound)):
			self.speed_y = -self.speed_y

class Player(Rect):
	def __init__(self, ball : Ball, *args):
		super().__init__(*args)
		self.ball = ball

	def start(self):
		self.position.set(100, 100)

		self.size.set(50, 150)
		pass

	def think(self):
		x = self.position.get_x()
		y = self.position.get_y() + 75

		#hand_y = GestureInput.get_hand_pos_y()

		#delta = y - hand_y 
		delta = 0

		if (delta > 10):
			self.speed_y = -SPEED
		elif(delta < 5):
			self.speed_y = SPEED
		else:
			self.speed_y = 0
		#self.position.set(x, y - 75 + self.speed_y)

class Enemy(Rect): 
	speed_y : int = 0
	def __init__(self, ball : Ball, *args):
		super().__init__(*args)
		self.ball = ball

	def start(self):
		self.position.set(WIDTH - 100, 100)

		self.size.set(50, 150)

	def think(self):
		x = self.position.get_x()
		y = self.position.get_y() + 75

		ball_y = self.ball.position.get_y() + 25

		# negative = above, positive = below
		delta = y - ball_y 

		if (delta > 10):
			self.speed_y = -SPEED
		elif(delta < 5):
			self.speed_y = SPEED
		else:
			self.speed_y = 0
		self.position.set(x, y - 75 + self.speed_y)

class Bound(Rect):
	def __init__(self, y):
		super().__init__()
		self.position.set(100, y)

	def start(self):
		self.size.set(WIDTH - 200, 2)

		self.color.set("alpha", 255)
		pass

	def think(self):
		pass

class GameBounds(Rect):
	def __init__(self, ball : Ball, player : Player, enemy : Enemy, 
		topBound : Bound, bottomBound : Bound):
		super().__init__()

	def start(self):
		self.size.set(0, 0)

	def think(self):
		if (check_ball_collide(ball, enemy)):
			ball.on_collide(enemy)

		if (check_ball_collide(ball, player)):
			ball.on_collide(player)


		if (check_ball_collide(ball, topBound)):
			ball.on_collide(topBound)

		if (check_ball_collide(ball, bottomBound)):
			ball.on_collide(bottomBound)


def check_ball_collide(ball : Ball, obj : Rect):
	r1x = ball.position.get_x()
	r1y = ball.position.get_y()
	r1w = ball.size.get_width()
	r1h = ball.size.get_height()

	r2x = obj.position.get_x()
	r2y = obj.position.get_y()
	r2w = obj.size.get_width()
	r2h = obj.size.get_height()
	return r1x + r1w >= r2x and r1x <= r2x + r2w and r1y + r1h >= r2y and r1y <= r2y + r2h

ball = Ball()
game.add_ent(ball)

player = Player(ball)
game.add_ent(player)

enemy = Enemy(ball)
game.add_ent(enemy)

topBound = Bound(0)
bottomBound = Bound(HEIGHT - 2)
game.add_ent(topBound)
game.add_ent(bottomBound)

gameBound = GameBounds(ball, player, enemy, topBound, bottomBound)
game.add_ent(gameBound)

game.init(WIDTH, HEIGHT, True)