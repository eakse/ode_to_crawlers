# -*- coding: utf-8 -*-
"""Utility functions 

This module contains some simple functions and/or classes that do
not have a proper place in their own modules.

Main ones are the class BaseLoader and the function roll_dice()

NOTE: There might be some obsolete classes/functions in here. 
I move them to ode.obsolete every now and then, if I'm sure I 
do not want to use them anymore...
"""

import os
from ode.constants import *
from random import randint
import json
from PIL import Image
from time import time


def timer(func):
    '''Decorator that reports the execution time.'''
    def wrap(*args, **kwargs):
        start = time()
        # print(f"start: {start}")
        result = func(*args, **kwargs)
        end = time()
        # print(f"end:   {end}")
        print(f"diff:  {end-start}")
        return result
    return wrap

class BaseLoader(object):
    """Base class from which most other classes inherit from.
    Functionality to dynamically load/save as JSON
    """
    def __init__(self, data=None):
        if data == None:
            return
        if type(data) != dict:
            data = dict(data)
        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if type(value) is list:
            return [self.compute_attr_value(x) for x in value]
        elif type(value) is dict:
            return BaseLoader(value)
        else:
            return value

    def __str__(self) -> str:
        """Turns the BaseLoader object into a valid JSON string
        Has logic to deal with nested BaseLoader objects, both dicts and lists
        Skips PIL.Image.Image

        Returns:
            str: valid JSON string
        """
        result = {}
        for key, value in self.__dict__.items():
            if type(value) == BaseLoader:
                value = self.__dict__[key].__str__()
            elif (
                type(value) == list and len(value) > 0 and type(value[0]) == BaseLoader
            ):
                value = [element.__str__() for element in value]
            elif type(value) == Image.Image:
                # skip PIL images
                continue
            result[key] = value
        return json.dumps(result)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def to_json(self) -> dict:
        return json.loads(self.__str__())


def get_files_from_path(path: str = ".", ext=None) -> list:
    """Find files in path and return them as a list.
    Gets all files in folders and subfolders

    See the answer on the link below for a ridiculously
    complete answer for this.
    https://stackoverflow.com/a/41447012/9267296
    Args:
        path (str, optional): Which path to start on.
                              Defaults to '.'.
        ext (str/list, optional): Optional file extention.
                                  Defaults to None.

    Returns:
        list: list of full file paths
    """
    result = []
    for subdir, dirs, files in os.walk(path):
        for fname in files:
            filepath = f"{subdir}{os.sep}{fname}"
            if ext == None:
                result.append(filepath)
            elif type(ext) == str and fname.lower().endswith(ext.lower()):
                result.append(filepath)
            elif type(ext) == list:
                for item in ext:
                    if fname.lower().endswith(item.lower()):
                        result.append(filepath)
    return result


def roll_dice(dice, stored=0) -> int:
    """Recursive method to return an int from standard dice notation.
    Valid exampes:
        3d6
        2d4+2
        d6
        3d6+4+d4-1

    Args:
        dice (str or int): the dice to roll. Accepts int for arithmatic reasons, and 
                           to be able to return fixed values (eg for armor/defense etc.) 
        stored (int, optional): Stores the previous result. Defaults to 0.

    Raises:
        ValueError: Raised when the function doesn't know what to do with the input dice

    Returns:
        int: result of the dice roll(s)
    """
    if type(dice) == int or dice.isnumeric():
        stored = stored + int(dice)
        result = stored
    elif "+" in dice:
        left, right = dice.split("+")[0], "+".join(dice.split("+")[1:])
        result = roll_dice(left, stored=stored) + roll_dice(right)
    elif "-" in dice:
        left, right = dice.split("-")[0], "-".join(dice.split("-")[1:])
        result = roll_dice(left, stored=stored) - roll_dice(right)
    elif "d" in dice:
        if len(dice.split("d")[0]) == 0:
            number_of_dice = 1
        else:
            number_of_dice = int(dice.split("d")[0])
        dice_type = int(dice.split("d")[1])
        for _ in range(number_of_dice):
            stored += randint(1, dice_type)
        result = stored
    else:
        raise ValueError(
            f"ValueError exception thrown\n  Dice:  {dice}\n  Stored: {stored}"
        )
    # TODO: Not sure if I should actually use the max below. I might need to split the main function into two functions and only apply the max() on the final result.
    return max(result, 0)


def d20() -> int:
    return roll_dice("d20")


def autorename_tiles():
    """Simple function to rename sprites from piskelapp to the correct names.
    """
    prev_dir = os.getcwd()
    os.chdir(PATH_MAP_IMAGES)
    os.rename("sprite_00.png", "map_floor.png")
    os.rename("sprite_01.png", "map_wall_n.png")
    os.rename("sprite_02.png", "map_wall_w.png")
    os.rename("sprite_03.png", "map_wall_s.png")
    os.rename("sprite_04.png", "map_wall_e.png")
    os.rename("sprite_05.png", "map_door_hidden_n.png")
    os.rename("sprite_06.png", "map_door_hidden_w.png")
    os.rename("sprite_07.png", "map_door_hidden_s.png")
    os.rename("sprite_08.png", "map_door_hidden_e.png")
    os.rename("sprite_09.png", "map_door_n.png")
    os.rename("sprite_10.png", "map_door_w.png")
    os.rename("sprite_11.png", "map_door_s.png")
    os.rename("sprite_12.png", "map_door_e.png")
    os.rename("sprite_13.png", "map_corner_nw.png")
    os.rename("sprite_14.png", "map_corner_sw.png")
    os.rename("sprite_15.png", "map_corner_se.png")
    os.rename("sprite_16.png", "map_corner_ne.png")
    os.rename("sprite_17.png", "map_empty.png")
    os.rename("sprite_18.png", "map_solid.png")
    os.chdir(prev_dir)
