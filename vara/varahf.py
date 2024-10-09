# OK1PKR Petr Kracik 2024

from . import Vara
from .tnc.cqframe import CQFrameHF
from .tnc.bandwidth import Bandwidth

class VaraHF(Vara):
    def _parse_vara_message(self, message):
        if message.startswith("CQFRAME"):
            self._event("on_cqframe", CQFrameHF.from_string(message))
            return

        super()._parse_vara_message(message)


    def bandwidth(self, bandwidth=Bandwidth.BW500):
        self._command_queue.append("bw")
        self._send('BW{}\r'.format(bandwidth.value).encode())


    def connect(self, source, destination):
        self._command_queue.append("connect")
        self._send('CONNECT {} {}\r'.format(source, destination).encode())


    def cq(self, call, bandwidth=Bandwidth.BW500):
        self._command_queue.append("cq")
        self._send('CQFRAME {} {}\r'.format(call, bandwidth.value).encode())
