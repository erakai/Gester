import pygame
import pygame.camera
from pygame.locals import *

from gester import Entity, GestureInput


class Game:
    _ents = []

    # Singleton
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def add_ent(self, ent: Entity):
        self._ents.append(ent)

    def prefix_ent(self, ent: Entity, index=0):
        self._ents.insert(index, ent)

    def init(self, window_width, window_height, isCamera=False):
        # pygame setup
        pygame.init()
        pygame.display.set_caption("Gester")
        pygame.font.init()
        surface = pygame.display.set_mode((window_width, window_height))
        clock = pygame.time.Clock()
        running = True

        GestureInput.init((window_width, window_height))

        cam: pygame.camera.Camera
        if isCamera:
            pygame.camera.init()

            cam = pygame.camera.Camera(0, (window_width, window_height))
            if cam == None:
                raise RuntimeError("No avaliable cameras, sorry :(")

            cam.start()

        for ent in self._ents:
            ent.start()

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if isCamera:
                img = cam.get_image()
                img = pygame.transform.flip(img, True, False)
                surface.blit(img, (0, 0))
            else:
                # fill the screen with a color to wipe away anything from last frame
                surface.fill("grey")

            # RENDER YOUR GAME HERE

            to_remove = []
            for ent in self._ents:
                if ent.marked_for_death:
                    to_remove.append(ent)
                    continue
                ent.render(surface)
                ent.think()

            for e in to_remove:
                if e in self._ents:
                    self._ents.remove(e)

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        if cam and cam is not None:
            cam.stop()

        GestureInput.close()
        pygame.quit()
