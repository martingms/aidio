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

def pyaudio_sink(samples, sample_width=2, rate=44100, bufsize=2048):
    # Don't want stuff to fail if this sink isn't used.
    import pyaudio

    p = pyaudio.PyAudio()

    f = p.open(format=p.get_format_from_width(sample_width),
               channels=1,
               rate=rate,
               output=True)

    # Make flush a noop, since write_pcm expects it to exist.
    f.flush = lambda: None

    write_pcm(f, samples, sample_width, rate, bufsize)
