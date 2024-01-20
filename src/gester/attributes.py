from abc import ABC
from typing import overload


class Attribute(ABC):
    _id: str

    def __init__(self, _id: str):
        self._id = _id
        self._data = {}

    def _get(self, key):
        return self._data[key]

    def _set(self, key, value):
        self._data[key] = value

    def __repr__(self):
        return str(self._data)


class AttributeContainer:
    _attrs = {}

    _attrs_ids = set()

    def add(self, attr: Attribute):
        self._attrs[attr._id] = attr
        self._attrs_ids.add(attr._id)

    def set(self, _id: str, attr: Attribute):
        if _id not in self._attrs_ids:
            raise RuntimeError("AttributeContainer: Unable to find id in set()")

        self._attrs[_id] = attr

    def get(self, _id: str):
        return self._attrs[_id]

    def has(self, _id: str):
        return _id in self._attrs_ids


def has_attrs(*args):
    def decorator(init):
        def wrapper(*init_args, **init_kwargs):
            from gester import Entity

            # all attrs must be a tuple of (id, AttrClass)
            for arg in args:
                assert isinstance(arg, tuple)
                assert len(arg) == 2
                assert isinstance(arg[0], str)
                assert issubclass(arg[1], Attribute)

            # first arg must be the entity of the init
            entity = init_args[0]
            assert issubclass(type(entity), Entity)

            # by default, add attrs as default
            for arg in args:
                _id = arg[0]
                _type = arg[1]
                attribute = _type(_id)
                if attribute is not None:
                    entity._attrs.add(attribute)
                    setattr(entity, _id, attribute)

            # loop through given attrs and update values
            for attr in init_args[1:]:
                assert issubclass(type(attr), Attribute)

                if entity._attrs.has(attr._id):
                    entity._attrs.set(attr._id, attr)
                    setattr(entity, attr._id, attr)

            result = init(*init_args, **init_kwargs)
            return result

        return wrapper

    return decorator


class Point(Attribute):
    DEFAULT_X = 100
    DEFAULT_Y = 100

    def __init__(self, _id: str, x=DEFAULT_X, y=DEFAULT_Y):
        super().__init__(_id)
        self._set("x", x)
        self._set("y", y)

    def set(self, x, y):
        self._set("x", x)
        self._set("y", y)

    def get(self):
        return (self._get("x"), self._get("y"))

    def get_x(self):
        return self._get("x")

    def get_y(self):
        return self._get("y")


class Size(Attribute):
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 100

    def __init__(self, _id: str, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        super().__init__(_id)
        self._set("width", width)
        self._set("height", height)

    def set(self, width, height):
        self._set("width", width)
        self._set("height", height)

    def get(self):
        return (self._get("width"), self._get("height"))

    def get_width(self):
        return self._get("width")

    def get_height(self):
        return self._get("height")


class Color(Attribute):
    DEFAULT_R = 200
    DEFAULT_B = 100
    DEFAULT_G = 0
    DEFAULT_A = 100

    def __init__(
        self, _id: str, red=DEFAULT_R, blue=DEFAULT_B, green=DEFAULT_G, alpha=DEFAULT_A
    ):
        super().__init__(_id)
        self._set("red", red)
        self._set("blue", blue)
        self._set("green", green)
        self._set("alpha", alpha)

    def set(self, key, value):
        if key not in set(self._data.keys()):
            raise RuntimeError("Invalid index of Color")

        self._set(key, value)
        pass

    def setAll(self, r, b, g, a):
        self.set("red", r)
        self.set("blue", b)
        self.set("green", g)
        self.set("alpha", a)

    def get(self):
        return (
            self._get("red"),
            self._get("blue"),
            self._get("green"),
            self._get("alpha"),
        )

    def get_red(self):
        return self._get("red")

    def get_blue(self):
        return self._get("blue")

    def get_green(self):
        return self._get("green")

    def get_alpha(self):
        return self._get("alpha")
