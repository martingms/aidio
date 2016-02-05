import math
import random
from itertools import count

# TODO: Accept start points?

def sine(freq, rate=44100, amplitude=0.5):
    assert amplitude >= 0.0 and amplitude <= 1.0, 'Amplitude out of range'

    for i in count(0):
        v = math.sin(2.0 * math.pi * float(freq) * (float(i) / float(rate)))
        yield float(amplitude) * v


def square(freq, rate=44100, amplitude=0.5):
    assert amplitude >= 0.0 and amplitude <= 1.0, 'Amplitude out of range'

    for v in sine(freq, rate, amplitude):
        if v > 0:
            yield amplitude
        if v < 0:
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
