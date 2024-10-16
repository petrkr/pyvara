# OK1PKR Petr Kracik 2024

from enum import Enum

class Encryption(Enum):
    DISABLED = "DISABLED"
    READY = "READY"

    @classmethod
    def from_value(cls, value):
        return cls(value) if value in cls._value2member_map_ else None
