import math
import wave
import random
import struct

from itertools import count, islice, izip, imap

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

def mix(*iters):
    return imap(lambda *args: sum(args), *iters)

def write_wave(f, samples, sample_width=2, rate=44100):
    max_amplitude = float(int((2 ** (sample_width * 8)) / 2) - 1)

    w = wave.open(f, 'wb')
    w.setparams((1, sample_width, rate, 44100 * 10, 'NONE', 'uncompressed'))

    for chunk in _group(samples, 2048):
        frames = [struct.pack('h', int(max_amplitude * sample)) for sample in chunk]
        w.writeframesraw(b''.join(frames))

    w.close()

def _group(iterable, n):
    return izip(*((iterable,) * n))

if __name__ == '__main__':
    import sys
    write_wave('test.wav', islice(square(880), 44100 * 10))

    #synth = createSynth()
    #while True:
    #    synth.play(x_tics)
    #    midi_event?
    #    synth.updateParams(midi_stuffs)
