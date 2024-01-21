from gester import Game, Entity, Rect, SwipeDetector, Text
from gester.attributes import Point, Color, Size
from gester import GestureInput

from logic_funcs import move_left, move_right, move_up, move_down
import random

game = Game()

WIDTH = 1280
HEIGHT = 720

class Board(Entity):
	CELL_COUNT = 4
	BOARD_SIZE = 520
	MARGIN = 10
	BOARD_X = 580
	BOARD_Y = 100

	CELL_SIZE = int((BOARD_SIZE - 5 * MARGIN) / CELL_COUNT)

	class Cell(Rect):
		def __init__(self, row, col):
			super().__init__()
			self.row = row
			self.col = col
			self.value = 0
			self.text = Text(Color("text_color", 0, 0, 0), Size("size", Board.CELL_SIZE, Board.CELL_SIZE))

		def start(self):
			self.size.set(Board.CELL_SIZE, Board.CELL_SIZE)

			x = Board.BOARD_X + ((Board.MARGIN) * (self.col + 1) + (Board.CELL_SIZE * self.col))
			y = Board.BOARD_Y + ((Board.MARGIN) * (self.row + 1) + (Board.CELL_SIZE * self.row))

			self.position.set(x, y)

			self.text.position.set(x, y)
			self.text.setText("0")
			game.add_ent(self.text)

			pass

		def think(self):
			import color_resolve
			color, text = color_resolve.color_resolve(self.value)

			self.color = color
			self.text.setText(text)

	def __init__(self):
		super().__init__()
		board_rect = Rect(Point("position", self.BOARD_X, self.BOARD_Y), Size("size", self.BOARD_SIZE, self.BOARD_SIZE), Color("color", 60, 60, 60))
		game.add_ent(board_rect)

		self.cells =[[Board.Cell(i, j) for i in range(self.CELL_COUNT)] for j in range(self.CELL_COUNT)]

		for i in range(0, self.CELL_COUNT):
			for j in range(0, self.CELL_COUNT):
				game.add_ent(self.cells[i][j])

	def start(self):
		self.grid = [[0 for i in range(self.CELL_COUNT)] for j in range(self.CELL_COUNT)]

		for i in range(2):
			self.new_square()

	def new_square(self):
		v = 2 * random.randint(1, 2)
		while True:
			x = random.randint(0, Board.CELL_COUNT - 1)
			y = random.randint(0, Board.CELL_COUNT - 1)

			if (self.grid[x][y] == 0):
				self.grid[x][y] = v
				break

	def isGameOver(self):
		for i in range(4):
			for j in range(4):
				if(self.grid[i][j]== 0):
					return False

		for i in range(3):
			for j in range(3):
				if(self.grid[i][j]== self.grid[i + 1][j] or self.grid[i][j]== self.grid[i][j + 1]):
					return False

		for j in range(3):
			if(self.grid[3][j]== self.grid[3][j + 1]):
				return False

		for i in range(3):
			if(self.grid[i][3]== self.grid[i + 1][3]):
				return False

		return True

	def render(self, surface):
		pass

	def think(self):
		for i in range(0, self.CELL_COUNT):
			for j in range(0, self.CELL_COUNT):
				self.cells[i][j].value = self.grid[i][j]

	def on_swipe(self, swipe : str):
		changed = False

		if (swipe == "up"):
			self.grid, changed = move_up(self.grid)
		elif (swipe == "down"):
			self.grid, changed = move_down(self.grid)
		elif (swipe == "left"):
			self.grid, changed = move_left(self.grid)
		elif (swipe == "right"):
			self.grid, changed = move_right(self.grid)

		if (changed):
			self.new_square()

		if (self.isGameOver()):
			self.start()

class HandFollower(Rect):
	def __init__(self, *args):
		super().__init__(*args)

	def start(self):
		self.size.set(20, 20)

	def think(self):
		if (GestureInput.get_hand_gesture() == "INDEX_EXTENDED"):
			self.color.setAll(200, 100, 0, 0)
		else:
			self.color.setAll(0, 0, 0, 0)

		x = GestureInput.get_pointer_x()
		y = GestureInput.get_pointer_y()

		self.position.set(x, y)

	def on_swipe(self, swipe: str):
		pass

swipe_detector = SwipeDetector()
game.add_ent(swipe_detector)

hand_follower = HandFollower()

swipe_detector.hook_ent(hand_follower)
game.add_ent(hand_follower)

board = Board()
game.add_ent(board)

swipe_detector.hook_ent(board)

game.init(WIDTH, HEIGHT, True)