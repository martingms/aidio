import struct
import wave

from .utils import chunk

def write_wave(f, samples, sample_width=2, rate=44100):
    max_amplitude = float(int((2 ** (sample_width * 8)) / 2) - 1)

    w = wave.open(f, 'wb')
    w.setparams((1, sample_width, rate, 44100 * 10, 'NONE', 'uncompressed'))

    for c in chunk(samples, 2048):
        frames = [struct.pack('h', int(max_amplitude * sample)) for sample in c]
        w.writeframesraw(b''.join(frames))

    w.close()

# Working
def write_pcm(f, samples, sample_width=2, rate=44100, bufsize=2048):
    max_amplitude = float(int((2 ** (sample_width * 8)) / 2) - 1)

    for c in chunk(samples, bufsize):
        frames = [struct.pack('h', int(max_amplitude * sample)) for sample in c]
        f.write(b''.join(frames))
        f.flush() # Needed?
