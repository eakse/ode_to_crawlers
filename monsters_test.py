from ode.monsters import *
import json
from pprint import pprint


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
            "attackStr": "{monster} {attack_lists.simple} {target} for {damage}.",
        },
        {
            "weight": 5, 
            "damage": "3d3+2",
            "attack": 1,
            "name": "slime2",
            "attackStr": "{monster} {attack_lists.notsimple} {target} for {damage}.",
        },
    ],
}

data = json.dumps(data_dict)

with open(f"{PATH_MONSTERS}slime.json", "w") as outfile:
    json.dump(data_dict, outfile, indent=4)

creature = Creature(data_dict)
pprint(creature.to_json)

for _ in range(20):
    print(creature.testing123)

# exit(0)
# target = Monster(data)
# someMonster = Monster(data)

# # someMonster.pp()
# print(someMonster)

# someMonster.save_to_json(f"{PATH_MONSTERS}slime.json")

# someMonster.attack(target)


