import random

from gester import *
from gester import sounds, Game, Entity
from gester import GestureInput
from gester.attributes import Point, Size, Color

game = Game()

WIDTH = 1280
HEIGHT = 720

SPEED = 10

class Ball(Rect):
	speed_x : int = 0
	speed_y : int = 0

	def __init__(self, *args):
		super().__init__()
		sounds.create_sound("slots", "games/assets/slot-machine.wav")

	def start(self):
		self.position.set(WIDTH/2, HEIGHT/2)
		self.size.set(50, 50)

		self.speed_x = random.randint(SPEED - 3, SPEED + 3)
		self.speed_y = random.randint(SPEED - 3, SPEED + 3)
		pass

	def think(self):
		x = self.position.get_x()
		y = self.position.get_y()

		# left out-of-bound
		if (x + 25 < 100):
			self.start()
			enemy.points += 1
			return

		if (x - 25 > WIDTH - 100):
			self.start()
			player.points += 1
			return

		self.position.set(x + self.speed_x, y + self.speed_y)

	def on_collide(self, obj):
		x = self.position.get_x()
		y = self.position.get_y()		
		# right paddle
		if (isinstance(obj, Enemy)):
			self.speed_x = -self.speed_x
			sounds.play_sound("slots")

		if (isinstance(obj, Player)):
			self.speed_x = -self.speed_x
			sounds.play_sound("slots")

		if (isinstance(obj, Bound)):
			self.speed_y = -self.speed_y

class Player(Rect):
	def __init__(self, ball : Ball, *args):
		super().__init__(*args)
		self.ball = ball
		self.points = 0

	def start(self):
		self.position.set(100, 100)

		self.size.set(50, 150)
		pass

	def think(self):
		x = self.position.get_x()
		y = self.position.get_y()

		hand_y = GestureInput.get_hand_pos_y()

		delta = y - hand_y 

		if (delta > 10):
			self.speed_y = -SPEED
		elif(delta < -10):
			self.speed_y = SPEED
		else:
			self.speed_y = 0
		self.position.set(x, y + self.speed_y)

class Enemy(Rect): 
	speed_y : int = 0
	def __init__(self, ball : Ball, *args):
		super().__init__(*args)
		self.ball = ball
		self.points = 0

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
		top_bound : Bound, bottom_bound : Bound, player_score : Text, enemy_score : Text):
		super().__init__()

	def start(self):
		self.size.set(0, 0)

	def think(self):
		if (check_ball_collide(ball, enemy)):
			ball.on_collide(enemy)

		if (check_ball_collide(ball, player)):
			ball.on_collide(player)


		if (check_ball_collide(ball, top_bound)):
			ball.on_collide(top_bound)

		if (check_ball_collide(ball, bottom_bound)):
			ball.on_collide(bottom_bound)

		player_score.setText("Player: " + str(player.points))
		enemy_score.setText("Enemy: " + str(enemy.points))


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

top_bound = Bound(0)
bottom_bound = Bound(HEIGHT - 2)
game.add_ent(top_bound)
game.add_ent(bottom_bound)

player_score = Text(Point("position", 200, 100), Color("text_color", 0, 0, 0, 0))
game.add_ent(player_score)

enemy_score = Text(Point("position", WIDTH - 200, 100), Color("text_color", 0, 0, 0, 0))
game.add_ent(enemy_score)


gameBound = GameBounds(ball, player, enemy, top_bound, bottom_bound, player_score, enemy_score)
game.add_ent(gameBound)

game.init(WIDTH, HEIGHT, True)