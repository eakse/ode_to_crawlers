# -*- coding: utf-8 -*-
"""ODE Constants

This module is for project wide constants. It should not contain
anything that is not a constant

NOTE: There might be some obsolete constants in here.
"""

TILESIZE = 24
TKINTER_TRANSPARENT_COLOR = "#a7fdce"

##### PATHS
PATH_SAVE = "saves/"
PATH_DATA = "data/"
PATH_MONSTERS = f"{PATH_DATA}monsters/"
PATH_ATTACKS = f"{PATH_DATA}attack_strings/"
PATH_IMAGES = f"{PATH_DATA}images/"
PATH_IMAGES_EDGE = f"{PATH_IMAGES}{TILESIZE}x{TILESIZE}/edge/"
PATH_IMAGES_FLOOR = f"{PATH_IMAGES}{TILESIZE}x{TILESIZE}/floor/"
PATH_MAP_IMAGES = f"{PATH_IMAGES}{TILESIZE}x{TILESIZE}/map/"
PATH_DUMMY_IMAGE = f"{PATH_IMAGES}dummy.png"
PATH_IMAGES_PARTY = f"{PATH_IMAGES}{TILESIZE}x{TILESIZE}/party/"

##### KEY CONSTANTS
# TODO: move all other key names in here
K_PARTY_X = "party_x"
K_PARTY_Y = "party_y"
K_FACING = "facing"
K_FACING_INDEX = "facing_index"

##### POSSIBLE EDGE STYLES
NONE = "none"
WALL = "wall"
DOOR = "door"
DOOR_HIDDEN = "door_hidden"
SEPA_INV = "sepa_inv"

##### LISTS FOR EDGES
EDGE_LIST = [NONE, WALL, DOOR, DOOR_HIDDEN, SEPA_INV]
EDGE_LIST_SIMPLE = [NONE, WALL, DOOR, DOOR_HIDDEN]
EDGE_LIST_VISIBLE = [NONE, WALL, DOOR, DOOR_HIDDEN]
EDGE_LIST_VISIBLE_DEV = [NONE, WALL, DOOR, DOOR_HIDDEN, SEPA_INV]
EDGE_LIST_SOLID = [WALL, DOOR, DOOR_HIDDEN]
EDGE_LIST_SOLID_ROOM = [WALL, DOOR, DOOR_HIDDEN, SEPA_INV]
EDGE_LIST_PASSABLE = [NONE, DOOR, DOOR_HIDDEN, SEPA_INV]

##### POSSIBLE FLOOR STYLES
FLOOR = "floor"
PIT = "pit"
STAIRS_UP = "stairs_up"
STAIRS_DOWN = "stairs_down"
TELEPORTER = "teleporter"
SOLID = "solid"

##### LISTS FOR FLOORS
FLOOR_LIST = [FLOOR, PIT, STAIRS_UP, STAIRS_DOWN, TELEPORTER, SOLID, NONE]
FLOOR_LIST_SIMPLE = [FLOOR, SOLID, NONE]
FLOOR_LIST_VISIBLE = [FLOOR, PIT, STAIRS_UP, STAIRS_DOWN, TELEPORTER, SOLID, NONE]
FLOOR_LIST_VISIBLE_DEV = [
    FLOOR,
    PIT,
    STAIRS_UP,
    STAIRS_DOWN,
    TELEPORTER,
    SOLID,
    NONE,
]
FLOOR_LIST_SOLID = [SOLID]
FLOOR_LIST_PASSABLE = [FLOOR, PIT, STAIRS_UP, STAIRS_DOWN, TELEPORTER, NONE]
FLOOR_LIST_PASSABLE_WARN = [PIT, TELEPORTER, NONE]

##### FACINGS
NORTH = 'north'
EAST = 'east'
SOUTH = 'south'
WEST = 'west'

##### LIST FOR FACINGS
# note that the order needs to be NESW due to rotation functions/methods
# as the index determines the degree of rotation
FACING_LIST = [NORTH, EAST, SOUTH, WEST]

##### SOME OTHER RANDOM CONSTANTS
ORI_N = "_n"
ORI_E = "_e"
ORI_S = "_s"
ORI_W = "_w"
ORI_LIST = [ORI_N, ORI_E, ORI_S, ORI_W]

EMPTY_TILE = {
    "_n": "none",
    "_e": "none",
    "_s": "none",
    "_w": "none",
    "_f": "floor"
}

