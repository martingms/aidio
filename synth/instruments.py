from .utils import midi_to_freq, modulate
from .generators import CV, adsr

class Instrument(object):
    def __iter__(self):
        raise NotImplementedError('__iter__ on instrument')

    def input(self, msg):
        raise NotImplementedError('input(midi_msg) on instrument')

class MonoSynth(Instrument):
    def __init__(self, osc):
        self._freq = CV(0)
        self._gate = CV(0)
        self._out = modulate(osc(self._freq), self._gate)

    def __iter__(self):
        yield from self._out

    def input(self, msg):
        if msg.type == 'note_on' and msg['velocity'] > 0:
            self._freq.set(midi_to_freq(msg['note']))
            self._gate.set(1.0)
        if msg.type == 'note_off' or (msg.type == 'note_on' and msg['velocity'] <= 0):
            self._gate.set(0.0)

class ADSRMonoSynth(Instrument):
    def __init__(self, osc):
        self._freq = CV(0)
        self._gate = CV(0)
        gate = adsr(self._gate, 50, 20, 0.8, 10)
        self._out = modulate(osc(self._freq), gate)

    def __iter__(self):
        yield from self._out

    def input(self, msg):
        if msg.type == 'note_on' and msg['velocity'] > 0:
            self._freq.set(midi_to_freq(msg['note']))
            self._gate.set(1.0)
        if msg.type == 'note_off' or (msg.type == 'note_on' and msg['velocity'] <= 0):
            self._gate.set(0.0)
