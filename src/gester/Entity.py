from abc import ABC, abstractmethod
import random

import pygame

from gester.attributes import Attribute, AttributeContainer


class Entity(ABC):
    _id: str
    _ids = set()  # static

    _attrs = AttributeContainer()

    def __init__(self):
        self._id = self._gen_id()
        self.marked_for_death = False

    def _gen_id(self):
        _i = ""
        for i in range(0, 99999):
            _i = "Entity@" + str(random.randint(0, 99999)).rjust(5, "0")
            if _i not in self._ids:
                self._ids.add(_i)
                break
        return _i

    def kill(self):
        self.marked_for_death = True

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def think(self):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass

    def on_pygame_event(self, event: pygame.event.Event):
        pass

    # swipe : left, right, up, down
    def on_swipe(self, swipe : str):
        pass
