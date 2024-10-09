# OK1PKR Petr Kracik 2024

class CQFrame():
    def __init__(self, source):
        self._source = source


    @property
    def source(self):
        return self._source


class CQFrameHF(CQFrame):
    def __init__(self, source, bandwidth):
        super().__init__(source)
        self._bandwidth = bandwidth

    @classmethod
    def from_string(cls, string):
        data = string.split()
        return cls(data[1], int(data[2]))


    @property
    def bandwidth(self):
        return self._bandwidth


    def __str__(self):
        return f"CQ {self._source} with {self._bandwidth} Hz"
