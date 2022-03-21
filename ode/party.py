from ode.constants import *
from ode.util import list_next
import json


class Party:
    """Class to contain data about a party"""

    def __init__(self, x: int = 0, y: int = 0, facing=NORTH):
        if facing not in FACING_LIST:
            facing = NORTH
        self._facing = facing
        self._x = x
        self._y = y

    def forward_coords(self) -> tuple:
        """Returns a tuple(x, y) of coords which is in front of the current facing"""
        x, y = self._x, self._y
        if self.facing == NORTH:
            y -= 1
        elif self.facing == SOUTH:
            y += 1
        elif self.facing == WEST:
            x -= 1
        elif self.facing == EAST:
            x += 1
        return (x, y)

    @property
    def forward(self) -> tuple:
        """Changes the current party coordinates to move one tile forward, based
        on the current facing."""
        if self.facing == NORTH:
            self._y -= 1
        elif self.facing == SOUTH:
            self._y += 1
        elif self.facing == WEST:
            self._x += 1
        elif self.facing == EAST:
            self._x -= 1
        return (self._x, self._y)

    @property
    def left(self) -> str:
        self._facing = list_next(self._facing, FACING_LIST)
        return self._facing        

    @property
    def right(self) -> str:
        self._facing = list_next(self._facing, FACING_LIST[::-1])
        return self._facing

    @property
    def turn(self) -> str:
        self._facing = list_next(self._facing, FACING_LIST)
        self._facing = list_next(self._facing, FACING_LIST)
        return self._facing

    @property
    def dump_map_paint(self) -> dict:
        """dumps a dict to pass on to the canvas"""
        return {
            K_PARTY_X: self._x,
            K_PARTY_Y: self._y,
            K_FACING_INDEX: self.facing_index
        }

    @property
    def dump(self) -> dict:
        return {
            K_PARTY_X: self._x,
            K_PARTY_Y: self._y,
            K_FACING: self._facing
        }

    def dumps(self, **kwargs) -> str:
        return json.dumps(self.dump, **kwargs)

    @property
    def facing_index(self) -> int:
        return FACING_LIST.index(self._facing)
        
    @property
    def facing(self) -> str:
        return str(self._facing)
    
    @facing.setter
    def facing(self, value=str):
        self._facing = value

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
