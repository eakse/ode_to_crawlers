from .ode_constants import *
from .util import BaseLoader


class PlayerCharacter(BaseLoader):
    def __init__(self, data=None):
        super().__init__(data)
        self.hpCurrent = self.hpMax

