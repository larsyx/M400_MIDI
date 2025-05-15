


import threading

import mido


class Midi_port():
    _lock = threading.lock()
    _instance = None

    @classmethod
    def get_input_port(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = mido.open_input(port_name)
            return cls._instance
