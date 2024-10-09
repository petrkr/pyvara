# OK1PKR Petr Kracik 2024
# Vara protocol implementation in Python

__author__ = "OK1PKR Petr Kracik"
__author_email__ = "pyvara@ok1pkr.radio"
__version__ = "0.0.1"
__license__ = "MIT"

import socket
import threading
from vara.tnc.compression import Compression
from vara.tnc.cleantxbuffer import CleanTxBuffer
from vara.tnc.encryption import Encryption
from vara.tnc.link import Link
from vara.tnc.bitrate import Bitrate

class Vara():
    def __init__(self, host = "localhost", control_port = 8300):
        self._host = host
        self._cport = control_port
        self._socket = None
        self._events = {}
        self._is_running = True
        self._command_queue = list()
        self._connected = None
        self._mycalls = None


    def _send(self, data: bytes) -> bool:
        try:
            self._socket.sendall(data)
            return True
        except Exception as e:
            print(f"Failed to send data: {e}")
            return False


    def _parse_vara_message(self, message):
        if message == "IAMALIVE":
            self._event("on_keepalive")
            return

        if message == "DISCONNECTED":
            self._connected = None
            self._event("on_disconnect")
            return

        if message == "PENDING":
            self._event("on_pending")
            return

        if message == "CANCELPENDING":
            self._event("on_cancelpending")
            return

        if message == "ENCRYPTED LINK":
            self._event("on_link", Link.ENCRYPTED)
            return

        if message == "UNENCRYPTED LINK":
            self._event("on_link", Link.UNENCRYPTED)
            return


        if message == "OK":
            if self._command_queue:
              cmd = self._command_queue[0]
              del self._command_queue[0]

            self._event("on_ok", cmd)
            return

        if message == "WRONG":
            if self._command_queue:
              cmd = self._command_queue[0]
              del self._command_queue[0]

            self._event("on_wrong", cmd)
            return

        if message.startswith("VERSION"):
            self._event("on_version", message.replace("VERSION ", ""))
            return

        if message.startswith("BUSY"):
            self._event("on_busy", True if message == "BUSY ON" else False)
            return

        if message.startswith("PTT"):
            self._event("on_ptt", True if message == "PTT ON" else False)
            return

        if message.startswith("REGISTERED"):
            self._event("on_registered", message.replace("REGISTERED ", "").split())
            return

        if message.startswith("SN"):
            self._event("on_sn", float(message.replace("SN ", "")))
            return

        if message.startswith("TUNE"):
            self._event("on_tune", float(message.replace("TUNE ", "")))
            return

        if message.startswith("BUFFER"):
            data = message.split()
            self._event("on_buffer", int(data[1]))
            return

        if message.startswith("CLEANTXBUFFER"):
            data = message.replace("CLEANTXBUFFER ", "").strip()
            self._event("on_cleantxbuffer", CleanTxBuffer.from_value(data))
            return

        if message.startswith("LINK"):
            data = message.replace("LINK ", "")
            self._event("on_link", Link.from_value(data))
            return

        if message.startswith("BITRATE"):
            self._event("on_bitrate", Bitrate.from_string(message))
            return

        if message.startswith("ENCRYPTION"):
            data = message.replace("ENCRYPTION ", "")
            self._event("on_encryption", Encryption.from_value(data))
            return

        print(f"Unknown message: {message}")


    def _receive(self) -> bytes:
        try:
            while self._is_running:
                data = self._socket.recv(1024)
                if not data:
                    print("Connection closed by the modem")
                    break

                messages = data.decode().split('\r')

                for m in messages:
                    if m:
                        self._parse_vara_message(m)


        except Exception as e:
            print(f"Failed to receive data: {e}")

        finally:
            self.modem_disconnect()


    def _add_event(self, event, callback):
        if event not in self._events:
            self._events[event] = list()

        if callback not in self._events[event]:
            self._events[event].append(callback)


    def _event(self, event, *args):
        if event not in self._events:
            print(f"Received event {event} without handler: {args}")
            return

        for f in self._events[event]:
            try:
                f(*args)
            except Exception as e:
                print(f"Error while calling user function: {e}")


    def modem_connect(self) -> bool:
        try:
            self._socket = socket.create_connection((self._host, self._cport))

            listener_thread = threading.Thread(target=self._receive)
            listener_thread.daemon = True
            listener_thread.start()
            return True
        except Exception as e:
            print(f"Failed to connect to socket: {e}")
            return False


    def modem_disconnect(self):
        if self._socket is None:
            return

        self._socket.close()
        self._is_running = False
        self._event("on_modem_disconnect")


    @property
    def is_connected(self):
        return self._connected is not None

    @property
    def remote_call(self):
        return self._connected


    def on_modem_disconnect(self, callback):
        self._add_event("on_modem_disconnect", callback)


    def on_bitrate(self, callback):
        self._add_event("on_bitrate", callback)


    def on_buffer(self, callback):
        self._add_event("on_buffer", callback)


    def on_busy(self, callback):
        self._add_event("on_busy", callback)


    def on_connect(self, callback):
        self._add_event("on_connect", callback)


    def on_disconnect(self, callback):
        self._add_event("on_disconnect", callback)


    def on_cqframe(self, callback):
        self._add_event("on_cqframe", callback)


    def on_cancelpending(self, callback):
        self._add_event("on_cancelpending", callback)


    def on_pending(self, callback):
        self._add_event("on_pending", callback)


    def on_sn(self, callback):
        self._add_event("on_sn", callback)


    def on_ptt(self, callback):
        self._add_event("on_ptt", callback)


    def on_ok(self, callback):
        self._add_event("on_ok", callback)


    def on_keepalive(self, callback):
        self._add_event("on_keepalive", callback)


    def on_registered(self, callback):
        self._add_event("on_registered", callback)


    def on_version(self, callback):
        self._add_event("on_version", callback)


    def version(self):
        self._send(b'VERSION\r')


    def abort(self):
        self._command_queue.append("abort")
        self._send('ABORT\r'.encode())


    def chat(self, state = True):
        self._command_queue.append("chat")
        self._send('CHAT {}\r'.format("ON" if state else "OFF").encode())


    def cleantxbuffer(self):
        self._send('CLEANTXBUFFER\r'.encode())


    def compression(self, compression=Compression.TEXT):
        self._command_queue.append("compression")
        self._send('COMPRESSION {}\r'.format(compression.value).encode())


    def disconnect(self):
        self._command_queue.append("disconnect")
        self._send('DISCONNECT\r'.encode())


    def listen(self, state = True):
        self._command_queue.append("listen")
        self._send('LISTEN {}\r'.format("ON" if state else "OFF").encode())


    def listencq(self):
        self._command_queue.append("listencq")
        self._send(b'LISTEN CQ\r')


    def mycall(self, callsigns: list):
        if len(callsigns) > 5:
            raise ValueError("Too many callsigns")

        self._command_queue.append("mycall")
        calls = ' '.join(callsigns)
        self._send(f'MYCALL {calls}\r'.encode())


    def tune(self, tune="?"):
        if tune is not "?":
            self._command_queue.append("tune")

        self._send('TUNE {}\r'.format(tune).encode())
