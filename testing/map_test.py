# yes I know * imports are bad :-|
# this is just a testing file
from ..ode.map import *
import pickle
import blosc


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
with open("testmap.blosc", "wb") as outfile:
    outfile.write(blosc.compress(pickle.dumps(map)))
    # json.dump(str(map.to_json), outfile, indent=4)

for image in MAPIMG:
    pass

print(tile1.to_json)
