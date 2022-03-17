# -*- coding: utf-8 -*-
"""Map class module, with all other classes that the Map class uses

The idea of this module is to provide a Map class that can be used
to represent the maps in the game.

All classes should have 2 methods (dump and dumps) similar to how
json.dump and json.dumps work. The dumps will pass any kwargs to
the json.dumps method.

They should also have at least one method that functions similar
to json.load to call the class constructor with the provided 
args/kwargs

NOTE: There might be some obsolete classes/functions in here. 
I move them to ode.obsolete every now and then, if I'm sure I 
do not want to use them anymore...
"""


from time import time
from ode.constants import *
# from ode.util import BaseLoader
from PIL import Image
from random import seed, choice
import json
import blosc
import pickle


# https://stackoverflow.com/a/68944117/9267296

seed()


def list_next(item, somelist: list):
    """Simple function to get the next item in somelist.

    Loops somelist if end reached.

    Returns element zero if item not in somelist
    """
    if item not in somelist:
        return somelist[0]
    index = somelist.index(item) + 1
    if index >= len(somelist):
        index = 0
    return somelist[index]


def list_random(somelist: list):
    """TODO: remove function and replace with choice(somelist)"""
    return choice(somelist)


class TileBase:
    """Base class for TileEdge and TileFloor.

    Mainly used to contain some methods/constants that are
    shared between the child classes.

    NOTE: Should not be instantiated itself, instead instantiate it's
    child classes.
    """

    DUMP_EXCLUDE_LIST = ["_dev_mode"]

    def __init__(self, dev_mode=False, **kwargs):
        if not hasattr(self, "style"):
            self._style = NONE
        if hasattr(self, "dev_mode"):
            self._dev_mode = self.dev_mode or dev_mode
        else:
            self._dev_mode = dev_mode
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return self.dumps()

    def __str__(self) -> str:
        return self.dumps()

    @property
    def dev_mode(self) -> bool:
        return self._dev_mode

    @dev_mode.setter
    def dev_mode(self, value: bool) -> bool:
        self._dev_mode = value
        return value

    @property
    def dump(self) -> dict:
        """Returns a dict representation of the instance"""
        result = {}
        for key, value in self.__dict__.items():
            if (
                key.startswith("_")
                and not key.startswith("__")
                and key not in self.DUMP_EXCLUDE_LIST
            ):
                result[key[1:]] = value
        return result

    def dumps(self, **kwargs) -> str:
        """Returns a json string representation of the instance.
        kwargs get passed to the used json.dumps()
        """
        return json.dumps(self.dump, **kwargs)

    @classmethod
    def random(cls, somelist: list):
        return cls(style=choice(somelist))


class TileEdge(TileBase):
    """Class to represent the edge of a MapTile"""

    def __init__(self, dev_mode=False, **kwargs):
        super().__init__(dev_mode, **kwargs)

    @property
    def style(self) -> str:
        if self._style not in EDGE_LIST:
            self._style = NONE
        return self._style

    @style.setter
    def style(self, value: str) -> bool:
        if value in EDGE_LIST:
            self._style = value
            return True
        return False

    @property
    def visible(self) -> bool:
        if self._dev_mode:
            return self._style in EDGE_LIST_VISIBLE_DEV
        else:
            return self._style in EDGE_LIST_VISIBLE

    @property
    def solid(self) -> bool:
        return self._style in EDGE_LIST_SOLID

    @property
    def solid_room(self) -> bool:
        return self._style in EDGE_LIST_SOLID_ROOM

    @property
    def passable(self) -> bool:
        return self._style in EDGE_LIST_PASSABLE

    @property
    def filename(self) -> str:
        return f"{PATH_IMAGES_EDGE}{self._style}.png"


class TileFloor(TileBase):
    """Class to represent the floor of a MapTile"""

    def __init__(self, dev_mode=False, **kwargs):
        # check because new tiles should start with floor instead of none
        if "style" not in kwargs.keys():
            kwargs["style"] = FLOOR
        super().__init__(dev_mode, **kwargs)

    @property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self, value: str) -> bool:
        if value in FLOOR_LIST:
            self._style = value
            return True
        self._style = FLOOR
        return False

    @property
    def visible(self) -> bool:
        if self._dev_mode:
            return self._style in FLOOR_LIST_VISIBLE_DEV
        else:
            return self._style in FLOOR_LIST_VISIBLE

    @property
    def solid(self) -> bool:
        return self._style in FLOOR_LIST_SOLID

    @property
    def passable(self) -> bool:
        return self._style in FLOOR_LIST_PASSABLE

    @property
    def passable_warn(self) -> bool:
        return self._style in FLOOR_LIST_PASSABLE_WARN

    @property
    def filename(self) -> str:
        return f"{PATH_IMAGES_FLOOR}{self._style}.png"


class MapTile:
    """Class to represent a map tile."""

    DUMP_EXCLUDE_LIST = ["_dev_mode", "_image"]

    def __init__(self, dev_mode=False, **kwargs):
        if hasattr(self, "dev_mode"):
            self._dev_mode = self.dev_mode or dev_mode
        else:
            self._dev_mode = dev_mode

        for edge in ["n", "e", "s", "w"]:
            if not hasattr(self, edge):
                if edge in kwargs.keys():
                    if type(kwargs[edge]) == str:
                        setattr(self, f"_{edge}", TileEdge(style=kwargs[edge]))
                    else:
                        setattr(self, f"_{edge}", TileEdge(**kwargs[edge]))
                else:
                    setattr(self, f"_{edge}", TileEdge())

        # TODO: add roof
        for floor in ["f"]:
            if not hasattr(self, floor):
                if floor in kwargs.keys():
                    if type(kwargs[floor]) == str:
                        setattr(self, f"_{floor}", TileFloor(style=kwargs[floor]))
                    else:
                        setattr(self, f"_{floor}", TileFloor(**kwargs[floor]))
                else:
                    setattr(self, f"_{floor}", TileFloor())

    @classmethod
    def random(
        cls,
        edge_list: list = EDGE_LIST_SIMPLE,
        floor_list: list = FLOOR_LIST_SIMPLE,
        floor_random: bool = False,
        **kwargs,
    ) -> "MapTile":
        """Generates and constructs a random instance of MapTile

        Args:
            edge_list (list, optional): List of edges to choose from. Defaults to EDGE_LIST_SIMPLE.
            floor_list (list, optional): Lis of floors to choose from. Only used when floor_random==True. Defaults to FLOOR_LIST_SIMPLE.
            floor_random (bool, optional): Whether or not to randomize the tiles' floor. If False, floor=edo.constants.NONE. Defaults to False.

        Returns:
            MapTile: New instance
        """
        if floor_random:
            _kwargs = {"f": choice(floor_list)}
        else:
            _kwargs = {}
        for edge in ["n", "e", "s", "w"]:
            _kwargs[edge] = choice(edge_list)
        return cls(**_kwargs, **kwargs)

    @property
    def dev_mode(self) -> bool:
        return self._dev_mode

    @dev_mode.setter
    def dev_mode(self, value: bool) -> bool:
        self._dev_mode = value
        return value

    @property
    def image(self) -> Image:
        """Returns a PIL.Image() representation of the tile

        TODO: implement logic for hidden doors etc.
        """
        # TODO: perhaps move to class Map due to corners
        __image = Image.open(self._f.filename)
        __paste = Image.open(self._n.filename)
        __image.paste(__paste, (0, 0), __paste)
        __paste = Image.open(self._e.filename).transpose(Image.ROTATE_270)
        __image.paste(__paste, (TILESIZE - 2, 0), __paste)
        __paste = Image.open(self._s.filename).transpose(Image.ROTATE_180)
        __image.paste(__paste, (0, TILESIZE - 2), __paste)
        __paste = Image.open(self._w.filename).transpose(Image.ROTATE_90)
        __image.paste(__paste, (0, 0), __paste)
        return __image

    @property
    def dump(self) -> dict:
        """Returns a dict representation of the instance"""
        result = {}
        for key, value in self.__dict__.items():
            if (
                key.startswith("_")
                and not key.startswith("__")
                and key not in self.DUMP_EXCLUDE_LIST
            ):
                if type(value) == TileEdge or type(value) == TileFloor:
                    result[key[1:]] = value.dump
                else:
                    result[key[1:]] = value
        return result

    def dumps(self, **kwargs) -> str:
        """Returns a json string representation of the instance
        kwargs get passed to the used json.dumps()
        """
        return json.dumps(self.dump, **kwargs)

    @property
    def n(self) -> TileEdge:
        return self._n

    @n.setter
    def n(self, value: str) -> bool:
        if value in EDGE_LIST:
            self._n = self._n.style(value)
        return value in EDGE_LIST

    @property
    def e(self) -> TileEdge:
        return self._e

    @e.setter
    def e(self, value: str) -> bool:
        if value in EDGE_LIST:
            self._e = self._e.style(value)
        return value in EDGE_LIST

    @property
    def s(self) -> TileEdge:
        return self._s

    @s.setter
    def s(self, value: str) -> bool:
        if value in EDGE_LIST:
            self._s = self._s.style(value)
        return value in EDGE_LIST

    @property
    def w(self) -> TileEdge:
        return self._w

    @w.setter
    def w(self, value: str) -> bool:
        if value in EDGE_LIST:
            self._w = self._w.style(value)
        return value in EDGE_LIST

    @property
    def f(self) -> TileFloor:
        return self._f

    @f.setter
    def f(self, value: str) -> bool:
        if value in FLOOR_LIST:
            self._f = self._f.style(value)
        return value in FLOOR_LIST


class Map:
    """Main class in this module to represent a map."""

    def __init__(
        self, width: int = 50, height: int = 50, tiles=None, dev_mode=False
    ) -> None:
        self.width = width
        self.height = height
        self.dev_mode = dev_mode
        if tiles:
            self.tiles = [
                [MapTile(dev_mode=dev_mode, **tiles[x][y]) for x in range(self.width)]
                for y in range(self.height)
            ]
        else:
            self.tiles = [
                [MapTile(dev_mode=dev_mode) for _ in range(self.width)]
                for _ in range(self.height)
            ]

    @property
    def dump(self) -> dict:
        """Returns a dict representation of the instance"""
        return {
            "width": self.width,
            "height": self.height,
            "tiles": [
                [self.tiles[x][y].dump for x in range(self.width)]
                for y in range(self.height)
            ],
        }

    def dumps(self, **kwargs) -> str:
        """Returns a json string representation of the instance
        kwargs get passed to the used json.dumps()
        """
        return json.dumps(self.dump, **kwargs)

    @classmethod
    def from_json(cls, **kwargs) -> "Map":
        return cls(**kwargs)

    def randomize(self, fix_edges=True):
        """Randomizes the map.

        Args:
            fix_edges (bool, optional): Set to true to call fix_edges() after randomization. Defaults to True.
        """
        self.tiles = [
            [MapTile().random() for _ in range(self.width)] for _ in range(self.height)
        ]
        if fix_edges:
            self.fix_edges()

    def clear(self, fix_edges=True):
        """Clears the map.

        Args:
            fix_edges (bool, optional): Set to true to call self.fix_edges() after clearing. Defaults to True.
        """
        self.tiles = [
            [MapTile(EMPTY_TILE) for _ in range(self.width)] for _ in range(self.height)
        ]
        if fix_edges:
            self.fix_edges()

    def fix_edges(self):
        """Makes sure the edges of the map have walls."""
        for y in range(self.height):
            self.tiles[0][y].w.style = WALL
            self.tiles[-1][y].e.style = WALL
        for x in range(self.width):
            self.tiles[x][0].n.style = WALL
            self.tiles[x][-1].s.style = WALL

    def adjust_surrounding(self, x, y):
        """Makes the surrounding tiles' edges match the provided tile."""
        if x - 1 >= 0:
            self.tiles[x - 1][y].e.style = self.tiles[x][y].w.style
        if x + 1 < self.width:
            self.tiles[x + 1][y].w.style = self.tiles[x][y].e.style
        if y - 1 >= 0:
            self.tiles[x][y - 1].s.style = self.tiles[x][y].n.style
        if y + 1 < self.width:
            self.tiles[x][y + 1].n.style = self.tiles[x][y].s.style

    def coord_in_all_rooms(self, coords: tuple) -> bool:
        for room in self.all_rooms:
            if coords in room:
                return True
        return False

    def get_rooms_all(self) -> list:
        """Currently borked, do not use"""
        self.all_rooms_visisted = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]
        self.all_rooms = []
        for x in range(self.width):
            for y in range(self.width):
                room = self.get_room((x, y), check_all=True)
                if len(room) > 0:
                    self.all_rooms.append(room)
        print(len(self.all_rooms))
        return self.all_rooms

    def get_room(self, start: tuple, visited: list = [], check_all=False) -> list:
        """Recursive function to find boundaries of a room.

        Args:
            start (tuple): start (x, y) coordinates
            visited (list of tuples, optional): list to keep track of which tiles have been checked. Defaults to None.

        Returns:
            list: (x, y) coordinates as a list
        """
        x, y = start
        if check_all and self.all_rooms_visisted[x][y]:
            return visited
        elif start in visited:
            if check_all:
                self.all_rooms_visisted[x][y] = True
            return visited
        else:
            if check_all:
                self.all_rooms_visisted[x][y] = True
            visited.append(start)
        if not (self.tiles[x][y].w.solid_room) and x - 1 >= 0:
            new_coords = (x - 1, y)
            if not (new_coords in visited):
                self.get_room(new_coords, visited=visited)
        if not (self.tiles[x][y].e.solid_room) and x + 1 < self.height:
            new_coords = (x + 1, y)
            if not (new_coords in visited):
                self.get_room(new_coords, visited=visited)
        if not (self.tiles[x][y].n.solid_room) and y - 1 >= 0:
            new_coords = (x, y - 1)
            if not (new_coords in visited):
                self.get_room(new_coords, visited=visited)
        if not (self.tiles[x][y].s.solid_room) and y + 1 < self.height:
            new_coords = (x, y + 1)
            if not (new_coords in visited):
                self.get_room(new_coords, visited=visited)
        return sorted(visited)

    # @property
    # def randomtile(self):
    #     edge = TileEdgeRandomizer(extra_empty=2)
    #     return {
    #         "_n": edge.random,
    #         "_e": edge.random,
    #         "_s": edge.random,
    #         "_w": edge.random,
    #         "_f": "floor",
    #     }

    # def load_tiles(self):
    #     pass

    @classmethod
    def load_blosc(cls, filename="test.map"):
        """Load map object.

        Maps is stored as a blosc compressed pickled Map object"""
        with open(filename, "rb") as infile:
            obj = pickle.loads(blosc.decompress(infile.read()))
        return obj

    @classmethod
    def load_blosc_json(cls, filename="test.map"):
        """DEPRECATED.

        Load map object.

        Maps is stored as a blosc compressed pickled JSON"""
        with open(filename, "rb") as infile:
            obj = pickle.loads(blosc.decompress(infile.read()))
        return cls(obj)

    def save_blosc_json(self, filename="test.map"):
        """DEPRECATED.

        Save map object.

        Maps is stored as a blosc compressed pickled JSON"""
        with open(filename, "wb") as outfile:
            outfile.write(blosc.compress(pickle.dumps(self.to_json)))

    def save_blosc(self, filename="test.map"):
        """Save map object.

        Maps is stored as a blosc compressed pickled Map object"""
        start = time()
        print(f"start: {start}")
        with open(filename, "wb") as outfile:
            outfile.write(blosc.compress(pickle.dumps(self)))
        end = time()
        print(f"end:   {end}")
        print(f"diff:  {end-start}")
