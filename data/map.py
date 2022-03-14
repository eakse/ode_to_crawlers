from settings import *
from util import BaseLoader
from PIL import Image


class MapImages:
    def __init__(self) -> None:
        self.floor = Image.open(f"{PATH_MAP_IMAGES}map_floor.png")
        self.empty = Image.open(f"{PATH_MAP_IMAGES}map_empty.png")

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


mapimg = MapImages()


class MapTile(BaseLoader):
    def update(self):
        self.tile_img = Image.new()
        if self.f == "floor":
            self.tile_img = mapimg.floor
        else:
            self.tile_img = mapimg.empty

        self.solid_n = True
        if self.n == "wall":
            self.tile_img.paste(mapimg.wall_n, (0,0), mapimg.wall_n)
        elif self.n == "door":
            self.tile_img.paste(mapimg.door_n, (0,0), mapimg.door_n)
        elif self.n == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_n, (0,0), mapimg.door_hidden_n)
        else:
            self.solid_n = False

        self.solid_e = True
        if self.e == "wall":
            self.tile_img.paste(mapimg.wall_e, (0,0), mapimg.wall_e)
        elif self.e == "door":
            self.tile_img.paste(mapimg.door_e, (0,0), mapimg.door_e)
        elif self.e == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_e, (0,0), mapimg.door_hidden_e)
        else:
            self.solid_e = False

        self.solid_s = True
        if self.s == "wall":
            self.tile_img.paste(mapimg.wall_s, (0,0), mapimg.wall_s)
        elif self.s == "door":
            self.tile_img.paste(mapimg.door_s, (0,0), mapimg.door_s)
        elif self.s == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_s, (0,0), mapimg.door_hidden_s)
        else:
            self.solid_s = False

        self.solid_w = True
        if self.w == "wall":
            self.tile_img.paste(mapimg.wall_w, (0,0), mapimg.wall_w)
        elif self.w == "door":
            self.tile_img.paste(mapimg.door_w, (0,0), mapimg.door_w)
        elif self.w == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_w, (0,0), mapimg.door_hidden_w)
        else:
            self.solid_w = False

    def __init__(self, data=None):
        super().__init__(data)
        self.update()

    def save_img(self, filename="test.png"):
        self.tile_img.save(filename)

    def update_corners(self, north: "MapTile"=None, east: "MapTile"=None, south: "MapTile"=None, west: "MapTile"=None):
        """Add corners to map tile based on adjacent tiles. Needs adjacent tiles as arguments to do so...

        Args:
            north (MapTile, optional): _description_. Defaults to None.
            east (MapTile, optional): _description_. Defaults to None.
            south (MapTile, optional): _description_. Defaults to None.
            west (MapTile, optional): _description_. Defaults to None.
        """
        if not(self.solid_n or self.solid_e) and ((north and north.solid_e) or (east and east.solid_n)):
            print("ne")
            self.tile_img.paste(mapimg.corner_ne, (0,0), mapimg.corner_ne)

        if not(self.solid_n or self.solid_w) and ((north and north.solid_w) or (west and west.solid_n)):
            print("nw")
            self.tile_img.paste(mapimg.corner_nw, (0,0), mapimg.corner_nw)

        if not(self.solid_s or self.solid_e) and ((south and south.solid_e) or (east and east.solid_s)):
            print("se")
            self.tile_img.paste(mapimg.corner_se, (0,0), mapimg.corner_se)

        if not(self.solid_s or self.solid_w) and ((south and south.solid_w) or (west and west.solid_s)):
            print("sw")
            self.tile_img.paste(mapimg.corner_sw, (0,0), mapimg.corner_sw)

    # @property
    # def tile(self):
    #     pass



    # @property
    # def n(self):
    #     pass



class Map(object):
    def __init__(self) -> None:
        pass

    def load_tiles(self):
        pass





################################################################################################################################################
### TESTING


tile_data1 = {
    "n": "none",
    "e": "none",
    "s": "none",
    "w": "none",
    "f": "floor"
}
tile_data2 = {
    "n": "door",
    "e": "wall",
    "s": "wall",
    "w": "wall",
    "f": "floor"
}

tile1 = MapTile(tile_data1)
tile2 = MapTile(tile_data2)
tile1.update_corners(tile2, tile2, tile2, tile2)
tile1.save_img("tile1.png")
tile2.save_img("tile2.png")
# tile1.tile_img.show()

for image in mapimg

# print(tile1.to_json)