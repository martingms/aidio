def mix(*iters):
    return map(lambda *args: sum(args), *iters)

def _group(iterable, n):
    return zip(*((iterable,) * n))

# Formula from: http://subsynth.sourceforge.net/midinote2freq.html
_A4 = 440
_MIDI_NOTE_FREQS = [(_A4 / 32) * (2**((x - 9) / 12)) for x in range(127)]
def midi_to_freq(n):
    return _MIDI_NOTE_FREQS[n]
