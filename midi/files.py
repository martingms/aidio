import io

from . import utils
from . import messages

class MidiFile(list):
    pass

class MidiTrack(list):
    pass

class _Parser(object):
    def __init__(self, f):
        self.f = f

    def load(self):
        midi_file = MidiFile()

        if not self.f.read(4) == b'MThd':
            # TODO: MidiError
            raise IOError('No MThd, probably not a MIDI file.')

        header_size = utils.read_long(self.f)
        midi_file.type = utils.read_short(self.f)
        num_tracks = utils.read_short(self.f)
        midi_file.ticks_per_beat = utils.read_short(self.f)

        # Skip rest of header.
        f.seek(header_size - 6, 1)

        for i in range(num_tracks):
            midi_file.append(self.load_track())

        return midi_file

    def load_track(self):
        track = MidiTrack()

        if not self.f.read(4) == b'MTrk':
            raise IOError('Track doesn\'t contain MTrk.')

        length = utils.read_long(self.f)
        start = self.f.tell()

        running_status = None

        while self.f.tell() - start < length:
            msg = messages._Parser(f).load(running_status)

            if msg.type is not 'meta':
                running_status = msg.status

            track.append(msg)

        return track

class _Serializer(object):
    def __init__(self, f):
        self.f = f

    def dump(midi_file):
        raise NotImplementedError('serialization of MIDI files')

def load(f):
    return _Parser(f).load()

def loads(buf):
    f = io.BytesIO(buf)
    return load(f)

def dump(midi_file, f):
    _Serializer(f).dump(midi_file)

def dumps(midi_file):
    f = io.BytesIO()
    dump(midi_file, f)
    return f.getvalue()
