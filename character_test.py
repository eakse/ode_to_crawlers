
# yes I know * imports are bad :-|
# this is just a testing file
from ode.character import *
from ode.party import *
import json
from ode.constants import *


################################################################################################################################################
### TESTING

# data = {
#     "name": "eakse",
#     "hpMax": 100,
#     "armor": 2,
#     "defense": 10,
# }

# facing = Facing()
# print(facing)
# for _ in range(10):
#     print(facing.right)
with open("data/test_char.json") as infile:
    data = json.load(infile)


pc = PlayerCharacter(**data)
# print(str(pc))