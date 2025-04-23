from midi.midiController import MidiController


midicontr = MidiController("pedal")
midicontr.send_command([0x00, 0x00, 0x00], [0x00, 0x00, 0x00])
