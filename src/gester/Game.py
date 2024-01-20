import pygame

from gester import Entity

class Game:
	_ents = []

	# Singleton
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Game, cls).__new__(cls)
		return cls.instance

	def add_ent(self, ent : Entity):
		self._ents.append(ent)

	def init(self):
		# pygame setup
		pygame.init()
		surface = pygame.display.set_mode((1280, 720))
		clock = pygame.time.Clock()
		running = True

		for ent in self._ents:
			ent.start()

		while running:
			# poll for events
			# pygame.QUIT event means the user clicked X to close your window
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			# fill the screen with a color to wipe away anything from last frame
			surface.fill("grey")

			# RENDER YOUR GAME HERE

			for ent in self._ents:
				ent.render(surface)
				ent.think()

			# flip() the display to put your work on screen
			pygame.display.flip()

			clock.tick(60)  # limits FPS to 60

		pygame.quit()