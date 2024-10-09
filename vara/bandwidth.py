# OK1PKR Petr Kracik 2024

from enum import Enum

class Bandwidth(Enum):
    UNKNOWN = 0
    BW500 = 500
    BW2300 = 2300
    BW2750 = 2750

    @classmethod
    def from_value(cls, value):
        return cls(value) if value in cls._value2member_map_ else cls.UNKNOWN
