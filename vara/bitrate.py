# OK1PKR Petr Kracik 2024

import re

class Bitrate():
    def __init__(self, speed_level, bps):
        self._speed_level = speed_level
        self._bps = bps

    @classmethod
    def from_string(cls, string):
        match = re.search(r'BITRATE \((\d+)\)\s+(\d+) bps', string)
        if match:
            speed_level = int(match.group(1))
            bps = int(match.group(2))
            return cls(speed_level, bps)
        else:
            return None
    
    def __str__(self):
        return f"Bitrate {self._speed_level}: {self._bps} bps"
