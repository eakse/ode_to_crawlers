
# yes I know * imports are bad :-|
# this is just a testing file
from ode.character import *
from ode.party import *

################################################################################################################################################
### TESTING

data = {
    "name": "eakse",
    "hpMax": 100,
    "armor": 2,
    "defense": 10,
}

facing = Facing()
print(facing)
for _ in range(10):
    print(facing.right)

pc = PlayerCharacter(data)
print(str(pc))