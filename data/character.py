from settings import *
from util import BaseLoader


class PlayerCharacter(BaseLoader):
    def __init__(self, data=None):
        super().__init__(data)
        self.hpCurrent = self.hpMax






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