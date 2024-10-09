# OK1PKR Petr Kracik 2024

from enum import Enum

class Compression(Enum):
    OFF = "OFF"
    TEXT = "TEXT"
    FILES = "FILES"

    @classmethod
    def from_value(cls, value):
        return cls(value) if value in cls._value2member_map_ else cls.TEXT
