import os
from random import randint


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
    # print(dice, stored)
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
    return max(result, 0)


def d20() -> int:
    return roll_dice("d20")
