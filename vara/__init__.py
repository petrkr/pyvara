# OK1PKR Petr Kracik 2024
# Vara protocol implementation in Python

__author__ = "OK1PKR Petr Kracik"
__version__ = "0.0.1"
__license__ = "MIT"

import socket

class Vara():
    def __init__(self, host = "localhost", control_port = 8300):
        self._host = host
        self._cport = control_port
        self._socket = None


    def _send(self, data: bytes) -> bool:
        try:
            self._socket.sendall(data)
            return True
        except Exception as e:
            print(f"Failed to send data: {e}")
            return False


    def _receive(self) -> bytes:
        try:
            return self._socket.recv(1024)
        except Exception as e:
            print(f"Failed to receive data: {e}")
            return False


    def _flushrecv(self):
        try:
            self._socket.setblocking(False)
            self._socket.recv(1024)
        except Exception:
            pass
        finally:
            self._socket.setblocking(True)


    def connect(self) -> bool:
        try:
            self._socket = socket.create_connection((self._host, self._cport))
            return True
        except Exception as e:
            print(f"Failed to connect to socket: {e}")
            return False


    def disconnect(self) -> bool:
        try:
            self._socket.close()
            return True
        except Exception as e:
            print(f"Failed to disconnect from socket: {e}")
            return False


    def get_version(self) -> str:
        self._flushrecv()
        self.send(b'VERSION\r')
        return self._receive().decode()


    def listen(self, state = True):
        self.flushrecv()
        self.send('LISTEN {}\r'.format("ON" if state else "OFF").encode())
        return self._receive().decode()


    def listencq(self):
        self.flushrecv()
        self.send(b'LISTEN CQ\r')
        return self._receive().decode()


    def mycall(self, callsigns: list):
        if len(callsigns) > 5:
            raise ValueError("Too many callsigns")

        calls = ' '.join(callsigns)
        self._flushrecv()
        self._send(f'MYCALL {calls}\r'.encode())

