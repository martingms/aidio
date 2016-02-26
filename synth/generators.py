import math
import random
from itertools import count

# TODO: Accept start points?

def sine(freq, rate=44100, amplitude=0.5):
    assert amplitude >= 0.0 and amplitude <= 1.0, 'Amplitude out of range'

    for i in count(0):
        v = math.sin(2.0 * math.pi * float(next(freq)) * (float(i) / float(rate)))
        yield float(amplitude) * v


def square(freq, rate=44100, amplitude=0.5):
    assert amplitude >= 0.0 and amplitude <= 1.0, 'Amplitude out of range'

    for v in sine(freq, rate, amplitude):
        if v > 0:
            yield amplitude
        elif v < 0:
            yield -amplitude
        else:
            yield 0.0

def saw(freq, rate=44100, amplitude=0.5):
    assert amplitude >= 0.0 and amplitude <= 1.0, 'Amplitude out of range'

    for i in count(0):
        x = float(i) / float(freq)
        yield float(amplitude) * 2.0 * (x - math.floor(x + 0.5))

def white_noise(amplitude=0.5):
    assert amplitude >= 0.0 and amplitude <= 1.0, 'Amplitude out of range'

    return (float(amplitude) * random.uniform(-1, 1) for i in count(0))

# A, D, R are in ms, sustain is amplitude in range [0.0, 1.0].
# TODO: Make adsr-variables controllable while operating.
def adsr(cv, attack=0, decay=0, sustain=1.0, release=0, rate=44100):
    a_samples = int(attack * (rate / 1000))
    d_samples = int(decay * (rate / 1000))
    r_samples = int(release * (rate / 1000))

    for v in cv:
        # Not yet triggered
        if v == 0.0:
            yield 0.0
            continue

        # Triggered, attack-phase
        for i in range(1, a_samples + 1):
            # Take a value from cv even though we don't use it.
            next(cv)
            yield 1.0 * (i / a_samples)

        # Decay-phase
        for i in range(1, d_samples + 1):
            next(cv)
            yield 1.0 - (i / d_samples) * (1.0 - sustain)

        # Sustain phase
        for v in cv:
            if v == 0.0:
                break

            yield sustain

        # Release phase
        for i in range(r_samples, -1, -1):
            yield sustain * (i / r_samples)

class CV(object):
    def __init__(self, init_val):
        self._val = init_val

    def set(self, val):
        self._val = val

    def __iter__(self):
        while True:
            yield self._val

    def __next__(self):
        return self._val
