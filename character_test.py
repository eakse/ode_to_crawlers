# yes I know * imports are bad :-|
# this is just a testing file
from ode.character import *

################################################################################################################################################
### TESTING

data = {
    "name": "eakse",
    "hpMax": 100,
    "armor": 2,
    "defense": 10,


}


pc = PlayerCharacter(data)
print(str(pc))