# -*- coding: utf-8 -*-
"""Map class module, with all other classes that the Map class uses

The idea of this module is to provide a Map class that can be used to represent
the maps in the game.

All classes should have 2 methods (dump and dumps) similar to how json.dump and
json.dumps work. The dumps will pass any kwargs to the json.dumps method.

They should also have at least one method that functions similar to json.load to
call the class constructor with the provided args/kwargs. Preferably this should
be done directly from the dunder init.

NOTE: There might be some obsolete classes/functions in here. I move them to
ode.obsolete every now and then, if I'm sure I do not want to use them
anymore... 
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


class TileBase:
    """Base class for TileEdge and TileFloor.

    Mainly used to contain some methods/constants that are
    shared between the child classes.

    NOTE: Should not be instantiated itself, instead instantiate its
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
        if not self._dev_mode:
            if self._style == SEPA_INV:
                return f"{PATH_IMAGES_EDGE}{NONE}.png"
            else:
                return f"{PATH_IMAGES_EDGE}{self._style}.png"
        else:
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
    def dev_visible(self) -> bool:
        """only used for SEPA_INV for now, which is used to separate rooms"""
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

    def __init__(self, dev_mode=False, visited=False, seen=False, **kwargs):
        if hasattr(self, "dev_mode"):
            self._dev_mode = self.dev_mode or dev_mode
        else:
            self._dev_mode = dev_mode

        self._visited = visited
        self._seen = seen

        if "seen" in kwargs.keys():
            self._seen = kwargs["seen"]

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
            floor_random (bool, optional): Whether or not to randomize the tiles' floor. If False, floor=ode.constants.NONE. Defaults to False.

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
    def passable(self) -> dict:
        result = {}
        for index, key in enumerate(["n", "e", "s", "w"]):
            edge = getattr(self, key)
            result[FACING_LIST[index]] = edge.passable
        return result

    @property
    def dev_mode(self) -> bool:
        """dev mode override"""
        return self._dev_mode

    @dev_mode.setter
    def dev_mode(self, value: bool) -> bool:
        self._dev_mode = value
        for key in ['n', "e", "s", "w", "f"]:
            obj = getattr(self, key)
            setattr(obj, "dev_mode", self._dev_mode)
        return value

    @property
    def visisted(self) -> bool:
        """True if the MapTile has been visisted by player"""
        return self._visisted

    @visisted.setter
    def visisted(self, value: bool) -> bool:
        self._visisted = value
        return self._visisted

    @property
    def seen(self) -> bool:
        """True if the MapTile has been seen by player"""
        return self._seen

    @seen.setter
    def seen(self, value: bool) -> bool:
        self._seen = value
        return self._seen

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
    def dump_long_dict(self) -> dict:
        return {
            NORTH: self._n,
            EAST:  self._e,
            SOUTH: self._s,
            WEST:  self._w
        }

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


class MapCoord:
    """Simple class to represent and handle Map coordinates"""

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __dict__(self) -> dict:
        return self.dump

    def __eq__(self, other: "MapCoord") -> bool:
        return self.coords == other.coords

    def __ne__(self, other: "MapCoord") -> bool:
        return self.coords != other.coords

    def __lt__(self, other: "MapCoord") -> bool:
        return self.coords < other.coords

    def __gt__(self, other: "MapCoord") -> bool:
        return self.coords > other.coords

    def __le__(self, other: "MapCoord") -> bool:
        return self.coords <= other.coords

    def __ge__(self, other: "MapCoord") -> bool:
        return self.coords >= other.coords

    def __iter__(self):
        self.__cnt = 0
        return self

    def __next__(self):
        self.__cnt += 1
        if self.__cnt == 1:
            return self._x
        elif self.__cnt == 2:
            return self._y
        else:
            raise StopIteration

    @property
    def coords(self) -> tuple:
        return (self._x, self._y)

    @coords.setter
    def coords(self, coords: tuple) -> tuple:
        self._x, self._y = coords
        return self.coords

    def xy(self, **kwargs):
        """Update coords, accepts x:int, y:int, t:tuple(x,y) as kwargs"""
        for key, value in kwargs.items():
            if key == "x":
                self._x = int(value)
            elif key == "y":
                self._y = int(value)
            elif key == "t":
                self._x, self._y = value
            else:
                raise KeyError(f"Unexpected key '{key}' received...")
        return self.coords

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value) -> tuple:
        self._x = value
        return self.coords

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value) -> tuple:
        self._y = value
        return self.coords

    @property
    def dump(self) -> dict:
        return {"x": self._x, "y": self._y}

    def dumps(self, **kwargs) -> str:
        return json.dumps(self.dump, **kwargs)


class Room:
    """Class to represent a room, which is a set of connected MapCoord in a Map

    Accepts coordinates as a list of tuples(x, y) or a list of dicts={x:int, y:int}
    The latter is needed for loading/saving to JSON

    Use to fe. place monster groups, and perhaps events."""

    def __init__(self, coords: list or dict = []):
        self._coords = []
        # TODO: this needs fixing
        if type(coords) == dict and "coords" in coords:
            _coords = coords['coords']
        else:
            _coords = coords
        for element in _coords:
            if type(element) == dict:
                self._coords.append(MapCoord(element["x"], element["y"]))
            else:
                self._coords.append(MapCoord(*element))
        self._coords.sort()

    def __len__(self) -> int:
        return self.size

    def __eq__(self, other: "Room") -> bool:
        if self.size != other.size:
            return False
        # since self._coords is a sorted property we can just do direct
        # comparison of elements by index.
        # not sure if the below is faster than using indexes of both lists
        # since this  is not a method that gets called often (likely never
        # ingame) I don't care that much about performance
        for index, element in enumerate(self.coords):
            if element != other.coords[index]:
                return False
        return True

    def __lt__(self, other: "Room") -> bool:
        if self.coords > other.coords:
            return True 
        return False
        
    def __gt__(self, other: "Room") -> bool:
        if self.coords < other.coords:
            return True
        return False

    def __iter__(self):
        self.__cnt = 0
        return self
    
    def __next__(self):
        if self.__cnt >= self.size-1:
            raise StopIteration
        else:
            self.__cnt += 1
        return self._coords[self.__cnt]

    @property
    def size(self) -> int:
        return len(self._coords)

    @property
    def coords(self) -> list[MapCoord]:
        return self._coords

    @property
    def first(self) -> tuple:
        if len(self._coords) > 0:
            return self.coords[0].coords

    @property
    def dump(self) -> dict:
        return {"coords": [coord.dump for coord in self._coords]}

    def dumps(self, **kwargs) -> str:
        return json.dumps(self.dump, **kwargs)


class Map:
    """Main class in this module to represent a map."""

    def __init__(self, width: int = 50, height: int = 50, tiles=None, dev_mode=False, room_list=[]):
        self.width = width
        self.height = height
        self._dev_mode = dev_mode
        # Load a dummy image for easy code completion (eg, set the type correctly)
        self._image = Image.open(PATH_DUMMY_IMAGE)
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
        self._room_list = []
        if len(room_list) > 0:
            self._room_list = [Room(room) for room in room_list]

    @property
    def dev_mode(self) -> bool:
        return self._dev_mode
    
    @dev_mode.setter
    def dev_mode(self, value: bool):
        self._dev_mode = value
        for row in self.tiles:
            for tile in row:
                tile.dev_mode = value

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
            "room_list": [room.dump for room in self._room_list]
        }

    def dumps(self, **kwargs) -> str:
        """Returns a json string representation of the instance
        kwargs get passed to the used json.dumps()
        """
        return json.dumps(self.dump, **kwargs)

    @property
    def room_list(self) -> list:
        """Returns a list of Room objects"""
        return self._room_list

    def add_room(self, room: Room):
        if room not in self._room_list:
            self._room_list.append(room)
            self._room_list.sort()

    def get_image(
        self, xt: int = None, yt: int = None, xb: int = None, yb: int = None
    ) -> Image:
        if xt:
            xt = max(0, xt)
        else:
            xt = 0
        if xb:
            xb = min(self.width, xb)
        else:
            xb = self.width
        if xt > xb:
            raise ValueError(f"Top Left X ({xt}) > Bottom Left X ({xb})")
        if yt:
            yt = max(0, yt)
        else:
            yt = 0
        if yb:
            yb = min(self.height, yb)
        else:
            yb = self.height
        if yt > yb:
            raise ValueError(f"Top Left Y ({yt}) > Bottom Left Y ({yb})")
        # print(xt, yt, xb, yb)
        img_size = lambda a, b: (a - b) * TILESIZE
        tile_mult = lambda a: a * TILESIZE
        paste_coord = lambda x, y: (tile_mult(x), tile_mult(y))
        # print(cf(xb, xt))
        # print(cf(yb, yt))
        self._image = Image.new("RGB", (img_size(xb, xt), img_size(yb, yt)))
        for x in range(xt, xb):
            for y in range(yt, yb):
                # print(self.tiles[x][y].dump, cc(x, y), ct(y))
                self._image.paste(self.tiles[x][y].image, paste_coord(x,y), self.tiles[x][y].image)
        return self._image

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
        # print(len(self.all_rooms))
        return self.all_rooms

    def get_room(self, start: tuple, visited_coords: list = [], first=False) -> list:
        """Recursive function to find boundaries of a room.

        Args:
            start (tuple): start (x, y) coordinates
            visited (list of tuples, optional): list to keep track of which tiles have been checked. Defaults to None.

        Returns:
            list: (x, y) coordinates as a list
        """
        x, y = start
        # if check_all and self.all_rooms_visisted[x][y]:
        #     return visited
        # elif start in visited:
        #     if check_all:
        #         self.all_rooms_visisted[x][y] = True
        #     return visited
        # else:
        # if check_all:
        #     self.all_rooms_visisted[x][y] = True
        visited_coords.append(start)
        if not (self.tiles[x][y].w.solid_room) and x - 1 >= 0:
            new_coords = (x - 1, y)
            if not (new_coords in visited_coords):
                self.get_room(new_coords, visited_coords=visited_coords)
        if not (self.tiles[x][y].e.solid_room) and x + 1 < self.height:
            new_coords = (x + 1, y)
            if not (new_coords in visited_coords):
                self.get_room(new_coords, visited_coords=visited_coords)
        if not (self.tiles[x][y].n.solid_room) and y - 1 >= 0:
            new_coords = (x, y - 1)
            if not (new_coords in visited_coords):
                self.get_room(new_coords, visited_coords=visited_coords)
        if not (self.tiles[x][y].s.solid_room) and y + 1 < self.height:
            new_coords = (x, y + 1)
            if not (new_coords in visited_coords):
                self.get_room(new_coords, visited_coords=visited_coords)
        if first:
            self.add_room(Room(visited_coords))
        return sorted(visited_coords)

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
    def load_blosc(cls, filename="test.map") -> "Map":
        """Load map object.

        Maps is stored as a blosc compressed pickled Map object"""
        with open(filename, "rb") as infile:
            obj = pickle.loads(blosc.decompress(infile.read()))
        return obj

    @classmethod
    def from_json(cls, **kwargs) -> "Map":
        return cls(**kwargs)

    @classmethod
    def from_json_file(cls, filename) -> "Map":
        with open(filename) as infile:
            data = json.load(infile)
        return cls(**data)

    @classmethod
    def load_blosc_json(cls, filename="test.map") -> "Map":
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
        old_dev = self._dev_mode
        self._dev_mode = False
        with open(filename, "wb") as outfile:
            outfile.write(blosc.compress(pickle.dumps(self)))
        self._dev_mode = old_dev
        end = time()
        print(f"end:   {end}")
        print(f"diff:  {end-start}")

