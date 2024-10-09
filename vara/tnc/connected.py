# OK1PKR Petr Kracik 2024

class Connected():
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    @property
    def source(self):
        return self._source


    @property
    def destination(self):
        return self._destination


class ConnectedHF(Connected):
    def __init__(self, source, destination, bandwidth):
        super().__init__(source, destination)
        self._bandwidth = bandwidth


    @classmethod
    def from_string(cls, string):
        data = string.split()
        return cls(data[1], data[2], int(data[3]))


    @property
    def bandwidth(self):
        return self._bandwidth


    def __str__(self):
        return f"CONNECTED {self._source}<-->{self._destination} with {self._bandwidth} Hz"
