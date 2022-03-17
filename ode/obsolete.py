class MapImages:
    """Simple container class for the map images."""

    def __init__(self) -> None:
        self.floor = Image.open(f"{PATH_MAP_IMAGES}map_floor.png")
        self.empty = Image.open(f"{PATH_MAP_IMAGES}map_empty.png")
        self.solid = Image.open(f"{PATH_MAP_IMAGES}map_solid.png")

        self.wall_n = Image.open(f"{PATH_MAP_IMAGES}map_wall_n.png")
        self.wall_e = Image.open(f"{PATH_MAP_IMAGES}map_wall_e.png")
        self.wall_s = Image.open(f"{PATH_MAP_IMAGES}map_wall_s.png")
        self.wall_w = Image.open(f"{PATH_MAP_IMAGES}map_wall_w.png")

        self.door_n = Image.open(f"{PATH_MAP_IMAGES}map_door_n.png")
        self.door_e = Image.open(f"{PATH_MAP_IMAGES}map_door_e.png")
        self.door_s = Image.open(f"{PATH_MAP_IMAGES}map_door_s.png")
        self.door_w = Image.open(f"{PATH_MAP_IMAGES}map_door_w.png")

        self.door_hidden_n = Image.open(f"{PATH_MAP_IMAGES}map_door_hidden_n.png")
        self.door_hidden_e = Image.open(f"{PATH_MAP_IMAGES}map_door_hidden_e.png")
        self.door_hidden_s = Image.open(f"{PATH_MAP_IMAGES}map_door_hidden_s.png")
        self.door_hidden_w = Image.open(f"{PATH_MAP_IMAGES}map_door_hidden_w.png")

        self.corner_ne = Image.open(f"{PATH_MAP_IMAGES}map_corner_ne.png")
        self.corner_nw = Image.open(f"{PATH_MAP_IMAGES}map_corner_nw.png")
        self.corner_se = Image.open(f"{PATH_MAP_IMAGES}map_corner_se.png")
        self.corner_sw = Image.open(f"{PATH_MAP_IMAGES}map_corner_sw.png")


"""Constant for MapImages"""
MAPIMG = MapImages()


class MapTile_old(BaseLoader):
    def __init__(self, data=None):
        super().__init__(data)
        self.tilesize = TILESIZE
        self.update()

    @property
    def pretty_text(self):
        # data = self.to_json
        return f"""
{self._n:^36}
{self._e:>12}{self._f:^12}{self._w:12}
{self._s:^36}
"""[
            1:-1
        ]

    def update(self):
        # start with new empty image on update
        self.tile_img = Image.new("RGBA", (self.tilesize, self.tilesize))
        if self._f == "floor":
            self.tile_img.paste(MAPIMG.floor, (0, 0), MAPIMG.floor)
        elif self._f == "solid":
            self.tile_img.paste(MAPIMG.solid, (0, 0), MAPIMG.solid)
            self._n = "wall"
            self._e = "wall"
            self._s = "wall"
            self._w = "wall"

        if not hasattr(self, "corner_n"):
            self.corner_n = True
        if not hasattr(self, "solid_n"):
            self.solid_n = False or self.n == "wall"
        if self._n == "wall":
            self.tile_img.paste(MAPIMG.wall_n, (0, 0), MAPIMG.wall_n)
        elif self._n == "door":
            self.tile_img.paste(MAPIMG.door_n, (0, 0), MAPIMG.door_n)
        elif self._n == "door_hidden":
            self.tile_img.paste(MAPIMG.door_hidden_n, (0, 0), MAPIMG.door_hidden_n)
        else:
            self.corner_n = False

        if not hasattr(self, "corner_e"):
            self.corner_e = True
        if not hasattr(self, "solid_e"):
            self.solid_e = False or self.e == "wall"
        if self._e == "wall":
            self.tile_img.paste(MAPIMG.wall_e, (0, 0), MAPIMG.wall_e)
        elif self._e == "door":
            self.tile_img.paste(MAPIMG.door_e, (0, 0), MAPIMG.door_e)
        elif self._e == "door_hidden":
            self.tile_img.paste(MAPIMG.door_hidden_e, (0, 0), MAPIMG.door_hidden_e)
        else:
            self.corner_e = False

        if not hasattr(self, "corner_s"):
            self.corner_s = True
        if not hasattr(self, "solid_s"):
            self.solid_s = False or self.s == "wall"
        if self._s == "wall":
            self.tile_img.paste(MAPIMG.wall_s, (0, 0), MAPIMG.wall_s)
        elif self._s == "door":
            self.tile_img.paste(MAPIMG.door_s, (0, 0), MAPIMG.door_s)
        elif self._s == "door_hidden":
            self.tile_img.paste(MAPIMG.door_hidden_s, (0, 0), MAPIMG.door_hidden_s)
        else:
            self.corner_s = False

        if not hasattr(self, "corner_w"):
            self.corner_w = True
        if not hasattr(self, "solid_w"):
            self.solid_w = False or self.w == "wall"
        if self._w == "wall":
            self.tile_img.paste(MAPIMG.wall_w, (0, 0), MAPIMG.wall_w)
        elif self._w == "door":
            self.tile_img.paste(MAPIMG.door_w, (0, 0), MAPIMG.door_w)
        elif self._w == "door_hidden":
            self.tile_img.paste(MAPIMG.door_hidden_w, (0, 0), MAPIMG.door_hidden_w)
        else:
            self.corner_w = False

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self._n = value
        self.update()

    @property
    def e(self):
        return self._e

    @e.setter
    def e(self, value):
        self._e = value
        self.update()

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, value):
        self._s = value
        self.update()

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self.update()

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, value):
        self._f = value
        self.update()

    def save_img(self, filename="test.png"):
        self.tile_img.save(filename)

    def update_corners(
        self,
        north: "MapTile" = None,
        east: "MapTile" = None,
        south: "MapTile" = None,
        west: "MapTile" = None,
    ):
        """Add corners to map tile based on adjacent tiles. Needs adjacent tiles as arguments to do so...

        Args:
            north (MapTile, optional): _description_. Defaults to None.
            east (MapTile, optional): _description_. Defaults to None.
            south (MapTile, optional): _description_. Defaults to None.
            west (MapTile, optional): _description_. Defaults to None.
        """
        if not (self.corner_n or self.corner_e) and (
            (north and north.corner_e) or (east and east.corner_n)
        ):
            self.tile_img.paste(MAPIMG.corner_ne, (0, 0), MAPIMG.corner_ne)

        if not (self.corner_n or self.corner_w) and (
            (north and north.corner_w) or (west and west.corner_n)
        ):
            self.tile_img.paste(MAPIMG.corner_nw, (0, 0), MAPIMG.corner_nw)

        if not (self.corner_s or self.corner_e) and (
            (south and south.corner_e) or (east and east.corner_s)
        ):
            self.tile_img.paste(MAPIMG.corner_se, (0, 0), MAPIMG.corner_se)

        if not (self.corner_s or self.corner_w) and (
            (south and south.corner_w) or (west and west.corner_s)
        ):
            self.tile_img.paste(MAPIMG.corner_sw, (0, 0), MAPIMG.corner_sw)



class TileEdgeRandomizer:
    """Simple class to do some simple manipulation of tile edges"""

    def __init__(self, extra_empty=0, start_type=None) -> None:
        self.types = EDGE_LIST_SIMPLE
        for _ in range(extra_empty):
            self.types.insert(0, NONE)
        if start_type:
            self.index = self.types.index(start_type)
        else:
            self.index = 0

    @property
    def current(self):
        return self.types[self.index]

    @property
    def next(self):
        self.index += 1
        if self.index >= len(self.types):
            self.index = 0
        return self.current

    @property
    def random(self):
        self.index = randint(0, len(self.types) - 1)
        return self.current


class TileFloorRandomizer:
    """Simple class to do some simple manipulation of floors"""

    def __init__(self, extra_empty=0, extra_floor=0, start_type=FLOOR) -> None:
        self.types = FLOOR_LIST_SIMPLE
        for _ in range(extra_empty):
            self.types.insert(0, NONE)
        for _ in range(extra_floor):
            self.types.insert(0, FLOOR)
        self.index = self.types.index(start_type)

    @property
    def current(self):
        return self.types[self.index]

    @property
    def next(self):
        self.index += 1
        if self.index >= len(self.types):
            self.index = 0
        return self.current

    @property
    def random(self):
        self.index = randint(0, len(self.types) - 1)
        return self.current

