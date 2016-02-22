from .utils import midi_to_freq

class Instrument(object):
    def __iter__(self):
        raise NotImplementedError('__iter__ on instrument')

    def input(self, msg):
        raise NotImplementedError('input(midi_msg) on instrument')

class MonoSynth(Instrument):
    def __init__(self, gen):
        self._gen = gen
        self._freq = 0

    def __iter__(self):
        yield from self._gen(self._freq)

    def input(self, msg):
        if msg.type == 'note_on' and msg['velocity'] > 0:
            self._freq = midi_to_freq(msg['note'])
        if msg.type == 'note_off' or (msg.type == 'note_on' and msg['velocity'] <= 0):
            self._freq = 0
