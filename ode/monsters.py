# -*- coding: utf-8 -*-
"""Monster module 

This module is meant for all classes/functions that deal with
the representation of monsters in the game.

NOTE: There might be some obsolete classes/functions in here. 
I move them to ode.obsolete every now and then, if I'm sure I 
do not want to use them anymore...
"""

from .constants import *
from .util import get_files_from_path, roll_dice, BaseLoader
from random import randint, seed
import os

# randomize the randomizer
seed()


class AttackLists(BaseLoader):
    """Loads all files from path ode_constants.PATH_ATTACKS and generates a dict with lists for each dict key.
    When accessing a list item, it returns a random item from that list instead of the list itself.
    Idea is to pass this into the attackStr of the attacks (using the constant ATTACK_LISTS) so there's
    some randomization in the messages that get printed.
    """

    def __init__(self):
        data = {}
        for filename in get_files_from_path(PATH_ATTACKS):
            # generate key name from filename
            key = os.path.basename(".".join(filename.split(".")[:-1]))
            with open(filename) as infile:
                # using this instead of readlines() due to the '\n' character being added with readlines()
                value = infile.read().splitlines()
            data[key] = value
        super().__init__(data)

    def __getattribute__(self, __name: str):
        """Getter override for lists to return a random element list item
        """
        data = super().__getattribute__(__name)
        if type(data) == list:
            return data[randint(0, len(data) - 1)]
        else:
            return data


ATTACK_LISTS = AttackLists()


class Creature(BaseLoader):

    def __init__(self, data):
        super().__init__(data)
        # nice discussion here
        # https://stackoverflow.com/a/610923/9267296
        # but I don't agree. In my case I think hasattr() is better
        if not hasattr(self, "name"):
            self.name = self.nameSingle
        if not hasattr(self, "hpMax"):
            self.hpMax = roll_dice(self.hpRandom)
        if not hasattr(self, "hpCurrent"):
            self.hpCurrent = self.hpMax
        if not hasattr(self, "defense"):
            self.defense = roll_dice(self.defenseRandom)
        if not hasattr(self, "armor"):
            self.armor = roll_dice(self.armorRandom)
        if not hasattr(self, "dead"):
            self.dead = False
        self.totalWeight = sum(attack.weight for attack in self.attacks)

    @property
    def hp_string(self):
        return f"{self.hpCurrent:{len(str(self.hpMax))}}/{self.hpMax}"

    @property
    def select_attack(self):
        selectedAttackWeight = randint(1, self.totalWeight)
        for att in self.attacks:
            selectedAttackWeight -= att.weight
            if selectedAttackWeight <= 0:
                break
        return att

    @property
    def select_attack_index(self):
        return self.attacks.index(self.select_attack)

    @property
    def testing123(self):
        i = self.select_attack_index
        return self.attacks[i].attackStr.format(
            monster=self.name,
            target="something",
            attack_lists=ATTACK_LISTS,
            damage=f"{roll_dice(self.attacks[i].damage)} damage",
        )

    @property
    def pretty_string(self):
        width = 10
        result = f"""
Name: {self.name:>{width}} | HP:   {self.hp_string:>{width}}
Def:  {self.defense:>{width}} | Arm:  {self.armor:>{width}}
"""
        return result[1:-1]


"""
#####################################################################################################################################################################
##### OBSOLETE
#####################################################################################################################################################################
class AttackBase(BaseLoader):
    def __init__(self, data):
        super().__init__(data)
        # self.__dict__ = json.loads(jsonStr)

    def __str__(self):
        return json.dumps(dict(self))

    def __repr__(self) -> str:
        return self.__str__()


class CreatureBase:
    def __init__(self, jsonStr):
        self.__dict__ = json.loads(jsonStr)
    
    def __repr__(self) -> str:
        return self.__dict__

    def __str__(self) -> str:
        return json.dumps(self.to_json())

    def pp(self):
        pprint(self.__dict__, indent=4)

    def to_json(self):
        attacks = []
        for att in self.attacks:
            attacks.append(str(att))
            print(type(attacks[-1]))


    def save_to_json(self, filename):
        self.to_json()
        exit(0)
        with open(filename, "w") as outfile:
            json.dump(json.loads(self.__repr__()), outfile, indent=4)


class Monster:
    def __init__(self, jsonStr):
        super().__init__(jsonStr)
        self.name = self.nameSingle
        self.hpMax = roll_dice(self.hpRandom)
        self.hpCurrent = self.hpMax
        self.defense = roll_dice(self.defenseRandom)
        self.armor = roll_dice(self.armorRandom)
        self.dead = False
        newattacks = []
        for attack in self.attacks:
            newattacks.append(AttackBase(json.dumps(attack)))
        self.attacks = newattacks
        self.totalWeight = sum(attack.weight for attack in self.attacks)

    def take_damage(self, damage, damageType=None):
        if damageType == None:
            old_damage = damage
            damage = max(damage - self.armor, 0)
            if old_damage != damage:
                print(f"Armor stopped {old_damage-damage} damage. {old_damage}-{damage}")
        self.hpCurrent -= damage
        if self.hpCurrent <= 0:
            self.dead = True
        return damage

    def attack(self, target):
        selectedAttackWeight = randint(1, self.totalWeight)
        for att in self.attacks:
            selectedAttackWeight -= att.weight
            if selectedAttackWeight <= 0:
                break
        
        
        damage = target.take_damage(roll_dice(att.damage))
        if damage == 0:
            resultString = att.attackStr.format(
                monster=self.name, 
                target=target.name, 
                random_attack_string=random_attack_string(),
                damage=f"{damage} damage, which fails to hurt {target.name}")
        else:
            resultString = att.attackStr.format(
                monster=self.name, 
                target=target.name, 
                random_attack_string=random_attack_string(),
                damage=f"{damage} damage")
            if target.dead:
                resultString += f"\n{target.name} has died."

        print(resultString)








"""
