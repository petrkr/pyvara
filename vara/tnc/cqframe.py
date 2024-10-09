# OK1PKR Petr Kracik 2024

class CQFrame():
    def __init__(self, source):
        self._source = source


class CQFrameHF(CQFrame):
    def __init__(self, source, bandwidth):
        super().__init__(source)
        self._bandwidth = bandwidth

    @classmethod
    def from_string(cls, string):
        data = message.split()
        return cls(data[1], int(data[2]))

    
    def __str__(self):
        return f"CQ {self._source} with {self._bandwidth} Hz"
