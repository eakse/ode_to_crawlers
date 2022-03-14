from settings import *
from util import BaseLoader
from PIL import Image
import json
import pickle
# https://stackoverflow.com/a/68944117/9267296



EMPTY_TILE = {
    "n": "",
    "e": "",
    "s": "",
    "w": "",
    "f": ""
}

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
        # start with new empty image on update
        self.tile_img = Image.new("RGBA", (32, 32))
        if self.f == "floor":
            self.tile_img.paste(mapimg.floor, (0,0), mapimg.floor)
        # below removed as it's stupid to paste empty on empty :-|
        # else:
        #     self.tile_img.paste(mapimg.empty, (0,0), mapimg.empty)


        if not hasattr(self, "corner_n"):
            self.corner_n = True
        if not hasattr(self, "solid_n"):
            self.solid_n = False or self.n == "wall"
        if self.n == "wall":
            self.tile_img.paste(mapimg.wall_n, (0,0), mapimg.wall_n)
        elif self.n == "door":
            self.tile_img.paste(mapimg.door_n, (0,0), mapimg.door_n)
        elif self.n == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_n, (0,0), mapimg.door_hidden_n)
        else:
            self.corner_n = False

        if not hasattr(self, "corner_e"):
            self.corner_e = True
        if not hasattr(self, "solid_e"):
            self.solid_e = False or self.e == "wall"
        if self.e == "wall":
            self.tile_img.paste(mapimg.wall_e, (0,0), mapimg.wall_e)
        elif self.e == "door":
            self.tile_img.paste(mapimg.door_e, (0,0), mapimg.door_e)
        elif self.e == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_e, (0,0), mapimg.door_hidden_e)
        else:
            self.corner_e = False

        if not hasattr(self, "corner_s"):
            self.corner_s = True
        if not hasattr(self, "solid_s"):
            self.solid_s = False or self.s == "wall"
        if self.s == "wall":
            self.tile_img.paste(mapimg.wall_s, (0,0), mapimg.wall_s)
        elif self.s == "door":
            self.tile_img.paste(mapimg.door_s, (0,0), mapimg.door_s)
        elif self.s == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_s, (0,0), mapimg.door_hidden_s)
        else:
            self.corner_s = False

        if not hasattr(self, "corner_w"):
            self.corner_w = True
        if not hasattr(self, "solid_w"):
            self.solid_w = False or self.w == "wall"
        if self.w == "wall":
            self.tile_img.paste(mapimg.wall_w, (0,0), mapimg.wall_w)
        elif self.w == "door":
            self.tile_img.paste(mapimg.door_w, (0,0), mapimg.door_w)
        elif self.w == "door_hidden":
            self.tile_img.paste(mapimg.door_hidden_w, (0,0), mapimg.door_hidden_w)
        else:
            self.corner_w = False

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
        if not(self.corner_n or self.corner_e) and ((north and north.corner_e) or (east and east.corner_n)):
            self.tile_img.paste(mapimg.corner_ne, (0,0), mapimg.corner_ne)

        if not(self.corner_n or self.corner_w) and ((north and north.corner_w) or (west and west.corner_n)):
            self.tile_img.paste(mapimg.corner_nw, (0,0), mapimg.corner_nw)

        if not(self.corner_s or self.corner_e) and ((south and south.corner_e) or (east and east.corner_s)):
            self.tile_img.paste(mapimg.corner_se, (0,0), mapimg.corner_se)

        if not(self.corner_s or self.corner_w) and ((south and south.corner_w) or (west and west.corner_s)):
            self.tile_img.paste(mapimg.corner_sw, (0,0), mapimg.corner_sw)

    # def __str__(self) -> str:
    #     """Turns the BaseLoader object into a valid JSON string
    #     Has logic to deal with nested BaseLoader objects, both dicts and lists

    #     Returns:
    #         str: valid JSON string
    #     """
    #     result = {}
    #     for key, value in self.__dict__.items():
    #         if type(value) != Image.Image:
    #             result[key] = value

    #     return json.dumps(result)

    # def __repr__(self) -> str:
    #     return self.__str__()

    # @property
    # def to_json(self) -> dict:
    #     return json.loads(self.__str__())


class Map(BaseLoader):
    def __init__(self, width: int=50, height: int=50) -> None:
        self.tiles = [[MapTile(EMPTY_TILE) for i in range(width)] for j in range(height)]
        
    @property
    def to_json(self) -> dict:
        return self.tiles

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

map = Map()

print()
with open("testmap.pickle", "wb") as outfile:
    pickle.dump(map, outfile)
    # json.dump(str(map.to_json), outfile, indent=4)

# for image in mapimg

# print(tile1.to_json)