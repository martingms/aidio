import operator
from functools import reduce
from itertools import islice

def mix(*iters):
    return map(lambda *args: sum(args), *iters)

def _product(factors):
    return reduce(operator.mul, factors, 1)

def modulate(*iters):
    return map(lambda *args: _product(args), *iters)

def amplify(signal, factor):
    return (s * factor for s in signal)

def clip(it, min_val=-1.0, max_val=1.0):
    return (v for v in it if v >= min_val and v <= max_val)

def chunk(iterable, n):
    return zip(*((iterable,) * n))

# Formula from: http://subsynth.sourceforge.net/midinote2freq.html
_A4 = 440
_MIDI_NOTE_FREQS = [(_A4 / 32) * (2**((x - 9) / 12)) for x in range(127)]
def midi_to_freq(n):
    return _MIDI_NOTE_FREQS[n]

_DEFAULT_MIDI_TEMPO = 500000

def play_midifile(mf, instruments):
    def pass_msg(msg):
        for channel, instrument in instruments.items():
            msg_channel = msg.get('channel')
            if msg_channel is None or msg_channel == channel:
                instrument.input(msg)

    seconds_per_tick = (_DEFAULT_MIDI_TEMPO / 1000000.0) / mf.ticks_per_beat
    for msg in mf:
        if msg.type == 'meta' and msg['meta_type'] == 'set_tempo':
            seconds_per_tick = (msg['tempo']/ 1000000.0) / mf.ticks_per_beat
        if msg.type not in ('note_on', 'note_off'):
            continue

        if msg.delta > 0:
            n_samples = int(44100 * seconds_per_tick * msg.delta)
            audio = clip(mix(*[i for i in instruments.values()]))
            yield from islice(audio, n_samples)

        pass_msg(msg)
