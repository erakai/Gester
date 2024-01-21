from gester import *
from gester import GestureInput

from time import perf_counter

SWIPE_DELTA_THRESHOLD = 150
SWIPE_TIME_THRESHOLD = 0.3

class DiffQueue():
	SIZE = 10

	def __init__(self):
		self._queue = [0 for i in range(self.SIZE)]

	def append(self, v : int):
		if (len(self._queue) < self.SIZE):
			self._queue.append(v)
		else:
			self._queue.pop(0)
			self._queue.append(v)

	def flush(self):
		self._queue = [-1 for i in range(self.SIZE)]

	def get_diff(self):
		if (self._queue[0] == -1 or self._queue[self.SIZE - 1] == -1):
			return 0
		return self._queue[0] - self._queue[self.SIZE - 1]


class SwipeDetector(Entity):
	def __init__(self, *args):
		super().__init__()
		self._x_queue = DiffQueue()
		self._y_queue = DiffQueue()

		self.on_wait = False
		self.time_start = 0

		self._ents = []

	def hook_ent(self, ent : Entity):
		self._ents.append(ent)

	def unhook_ent(self, ent : Entity):
		self._ents.remove(ent)

	def call_hooked_ents(self, swipe : str):
		for ent in self._ents:
			ent.on_swipe(swipe)

	def start(self):
		pass

	def render(self, surface):
		pass

	def think(self):
		self._x_queue.append(GestureInput.get_hand_pos_x())
		self._y_queue.append(GestureInput.get_hand_pos_y())

		if (GestureInput.get_hand_gesture() == "INDEX_EXTENDED"):
			if (not self.on_wait and abs(self._x_queue.get_diff()) > SWIPE_DELTA_THRESHOLD):
				self.on_wait = True
				self.time_start = perf_counter() 

				if (self._x_queue.get_diff() > 0):
					self.call_hooked_ents("left")

				if (self._x_queue.get_diff() < 0):
					self.call_hooked_ents("right")

			if (not self.on_wait and abs(self._y_queue.get_diff()) > SWIPE_DELTA_THRESHOLD):
				self.on_wait = True
				self.time_start = perf_counter() 

				if (self._y_queue.get_diff() > 0):
					self.call_hooked_ents("up")

				if (self._y_queue.get_diff() < 0):
					self.call_hooked_ents("down")
		else:
			self._x_queue.flush()
			self._y_queue.flush()

		if (perf_counter() - self.time_start > SWIPE_TIME_THRESHOLD):
			self.on_wait = False
			self.time_start = 0