from vara.varahf import VaraHF
from vara.bandwidth import Bandwidth
from time import sleep
import Hamlib

modem = None
rig = None
registered = False

def initialize_rig(rig_address):
    Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_NONE)
    rig = Hamlib.Rig(Hamlib.RIG_MODEL_NETRIGCTL)
    rig.set_conf("rig_pathname", rig_address)
    rig.open()
    print(f"Connected to rig at {rig_address}")
    print(f"Rig model: {rig.get_info()}")
    print(f"Rig frequency: {rig.get_freq()} Hz")
    print(f"Rig mode: {rig.get_mode()}")
    print(f"Rig power: {int(rig.get_level_f('RFPOWER') * 100)} W")

    return rig

def on_keepalive():
    print("Still alive")

def on_ok(reason):
    print(f"OK: {reason}")

def on_busy(data):
    print(f"Got busy {data}")

def on_version(data):
    print(f"Got version {data}")

def on_registered(calls):
    global registered
    print(f"Registered calls {calls}")
    registered = True

def on_bitrate(bitrate):
    print(f"Bitrate {bitrate}")

def on_cqframe(call, bandwidth):
    print(f"CQ from {call} with {bandwidth}Hz")

def on_sn(sn):
    print(f"SN {sn} dB")

def on_connect(source, dest, bandwidth):
    print(f"Connected from {source} to {dest} at {bandwidth} Hz")

def on_pending():
    print("Something is pending")

def on_cancelpending():
    print("Something canceled pending")

def on_ptt(state):
    print(f"PTT: {state}")
    if not rig:
        return

    rig.set_ptt(Hamlib.RIG_VFO_CURR, Hamlib.RIG_PTT_ON if state else Hamlib.RIG_PTT_OFF)


def main():
    global rig
    global modem
    rig = initialize_rig("localhost")


    modem = VaraHF()

    modem.on_bitrate(on_bitrate)
    modem.on_cqframe(on_cqframe)
    modem.on_busy(on_busy)
    modem.on_keepalive(on_keepalive)
    modem.on_version(on_version)
    modem.on_ok(on_ok)
    modem.on_registered(on_registered)
    modem.on_sn(on_sn)
    modem.on_connect(on_connect)
    modem.on_pending(on_pending)
    modem.on_cancelpending(on_cancelpending)
    modem.on_ptt(on_ptt)

    print(modem.modem_connect())

    modem.version()
    modem.bandwidth(Bandwidth.BW500)
    modem.chat()
    modem.listen()
    modem.listencq()
    modem.mycall(["MYCALL","MYCALL-T"])
    modem.bandwidth(Bandwidth.BW500)
    modem.compression()

    while not registered:
        sleep(1)


    def interact():
        import code
        code.InteractiveConsole(locals=globals()).interact()

    interact()

    while True:
        sleep(1)


if __name__ == "__main__":
    main()
