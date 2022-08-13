from .constants import *
# from .util import BaseLoader


class PlayerCharacter():
    def __init__(self, **kwargs):#data=None, 
        # super().__init__(data)
        print(kwargs)
        self.__dict__.update(kwargs)
        # for key, value in kwargs.items():
        #     print(key,value)
        #     self[key] = value
        print(self.__dict__)
        self.hpCurrent = self.hpMax
        print(self.hpCurrent)
        print(self.name)

