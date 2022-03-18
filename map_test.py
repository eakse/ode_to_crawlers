# yes I know * imports are bad :-|
# this is just a testing file
from ode.map import *
import pickle
import blosc


################################################################################################################################################
### TESTING



room = Room([(5, 10), (6, 9), (6, 10), (7, 9), (7, 10)])
room2 = Room([{"x": 5, "y": 10}, {"x": 6, "y": 9}, {"x": 6, "y": 10}, {"x": 7, "y": 9}, {"x": 7, "y": 10}])
print(room2 == room)



exit(0)
coord = MapCoord(3,5)
coord.x = 1
print(*coord.coords)
coord.y=3
coord.coords = (3,5)
print(coord.coords)
# print(coord.xy(z=3))

tile = MapTile.random(floor_random=True)
print(tile.dump)


# tile.image.show()


tile_edge = TileEdge.random(EDGE_LIST)
print(tile_edge.dump)
print(tile_edge.EDGE_LIST_VISIBLE)
print(tile_edge.dump)
tile_edge.style = "wall"
print(tile_edge.dump)
print(type(tile_edge))

tile_edge2 = TileEdge(style="door")
print(tile_edge2.dumps(indent=4))
print(tile_edge2.filename)
print(tile_edge, str(tile_edge2))

floor1 = TileFloor()
print(floor1)
exit(0)


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


print(tile1.to_json)
