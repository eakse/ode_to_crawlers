from settings import *
from util import get_files_from_path, roll_dice
import json
from random import randint, seed
from pprint import pprint
import os

# randomize the randomizer
seed()


class BaseLoader(object):
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

        Returns:
            str: valid JSON string
        """
        result = {}
        for key, value in self.__dict__.items():
            if type(value) == BaseLoader:
                value = self.__dict__[key].__str__()
            elif type(value) == list and len(value) > 0 and type(value[0]) == BaseLoader:
                value = [element.__str__() for element in value]
            result[key] = value
        # please note that the line below is less stupid than it seems.
        # it's basically sanitizing escape slashes which was annoying the
        # eff out of me
        # temporarily removed :-|
        # result = json.loads()
        return json.dumps(result)

    def __repr__(self) -> str:
        return self.__str__

    @property
    def to_json(self) -> dict:
        return json.loads(self.__str__())

        


class AttackLists(BaseLoader):
    """Loads all files from path settings.py -> PATH_ATTACKS and generates a dict with lists for each dict key.
    When accessing a list item, it returns a random item from that list instead of the list itself.

    Args:
        BaseLoader (_type_): _description_
    """
    def __init__(self):
        data = {}
        for filename in get_files_from_path(PATH_ATTACKS):
            key = os.path.basename(".".join(filename.split(".")[:-1]))
            with open(filename) as infile:
                # using this instead of readlines() due to the '\n' character being added with readlines()
                value = infile.read().splitlines()
            data[key] = value
        super().__init__(data)

    def __getattribute__(self, __name: str):
        """Getter override for lists to return a random element list item

        Args:
            __name (str): _description_

        Returns:
            _type_: _description_
        """
        data = super().__getattribute__(__name)
        if type(data) == list:
            return data[randint(0, len(data)-1)]
        else:
            return data


attack_lists = AttackLists()



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
        print(self.select_attack_index)
        return self.attacks[1].attackStr.format(
                monster=self.name, 
                target="something", 
                attack_lists=attack_lists,
                damage=f"10 damage")        

    @property
    def pretty_string(self):
        width = 10
        result = f"""
Name: {self.name:>{width}} | HP:   {self.hp_string:>{width}}
Def:  {self.defense:>{width}} | Arm:  {self.armor:>{width}}
"""
        return result[1:-1]


################################################################################################################################################
### TESTING

data_dict = {
    "nameSingle": "slime",
    "namePlural": "group of slimes",
    "hpRandom": "3d6",
    "defenseRandom": 5,
    "armorRandom": 4,
    "attacks": [
        {
            "weight": 10,
            "damage": "1d3-1",
            "attack": 1,
            "name": "attack",
            "attackStr": "{monster} {attack_lists.simple} {target} for {damage}."
        },        {
            "weight": 1,
            "damage": "3d3+2",
            "attack": 1,
            "name": "slime2",
            "attackStr": "{monster} {attack_lists.notsimple} {target} for {damage}."
        }
    ]
}

data=json.dumps(data_dict)

with open(f"{PATH_MONSTERS}slime.json", "w") as outfile:
    json.dump(data_dict, outfile, indent=4)

creature = Creature(data_dict)
pprint(creature.to_json)

# for _ in range(20):
#     print(creature.testing123)

# exit(0)
# target = Monster(data)
# someMonster = Monster(data)

# # someMonster.pp()
# print(someMonster)

# someMonster.save_to_json(f"{PATH_MONSTERS}slime.json")

# someMonster.attack(target)


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