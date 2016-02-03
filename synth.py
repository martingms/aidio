import math
import wave
import random
import struct

from itertools import count, islice #, izip, imap

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

# Working.
def white_noise(amplitude=0.5):
    assert amplitude >= 0.0 and amplitude <= 1.0, 'Amplitude out of range'

    return (float(amplitude) * random.uniform(-1, 1) for i in count(0))

# Not working.
# https://ccrma.stanford.edu/~jos/filters/Definition_Simplest_Low_Pass.html
def simplestlowpass(it, init=0.0):
    for sa in it:
        yield sa + init
        init = sa

# Not working.
# https://stkrs.googlecode.com/svn/trunk/fodder/VCF/MoogVCF.c
# https://ccrma.stanford.edu/~jos/fp/
def moogvcf1(it, cutoff, res, rate=44100):
    assert cutoff >= 0.0 and cutoff <= (rate / 2), 'Cutoff out of range'
    assert res >= 0.0 and res <= 1.0, 'Resonance out of range'

    freq = cutoff / (rate / 2) # ? # Nyquist
    q = 1.0 - freq
    p = freq + 0.8 * freq * q
    f = p + p - 1.0
    q = res * (1.0 + 0.5 * q * (1.0 - q + 5.6 * q * q))

    (b0, b1, b2, b3, b4) = (0, 0, 0, 0, 0)
    for sa in it:
        # Feedback
        sa -= q * b4
        t1 = b1;  b1 = (sa + b0) * p - b1 * f
        t2 = b2;  b2 = (b1 + t1) * p - b2 * f
        t1 = b3;  b3 = (b2 + t2) * p - b3 * f
        b4 = (b3 + t1) * p - b4 * f
        # Clipping
        b4 = b4 - b4 * b4 * b4 * 0.166667
        b0 = sa

        yield b4

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

# Working
def write_pcm(f, samples, sample_width=2, rate=44100, bufsize=2048):
    max_amplitude = float(int((2 ** (sample_width * 8)) / 2) - 1)

    for chunk in _group(samples, bufsize):
        frames = [struct.pack('h', int(max_amplitude * sample)) for sample in chunk]
        f.write(b''.join(frames))
        f.flush() # Needed?

    f.close()

# Working
def _group(iterable, n):
    return zip(*((iterable,) * n))

if __name__ == '__main__':
    #import sys
    #write_wave(sys.stdout.buffer, islice(square(880), 44100 * 10))
    #write_pcm(sys.stdout.buffer, islice(square(880), 44100 * 10))

    #synth = createSynth()
    #while True:
    #    synth.play(x_tics)
    #    midi_event?
    #    synth.updateParams(midi_stuffs)
