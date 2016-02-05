def mix(*iters):
    return map(lambda *args: sum(args), *iters)

def _group(iterable, n):
    return zip(*((iterable,) * n))

def clip(it, min_val=-1.0, max_val=1.0):
    return (v for v in it if v >= min_val and v <= max_val)

# Formula from: http://subsynth.sourceforge.net/midinote2freq.html
_A4 = 440
_MIDI_NOTE_FREQS = [(_A4 / 32) * (2**((x - 9) / 12)) for x in range(127)]
def midi_to_freq(n):
    return _MIDI_NOTE_FREQS[n]
