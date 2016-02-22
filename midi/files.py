import io

from . import utils
from . import messages

class MidiFile(object):
    def __init__(self):
        self.tracks = []

    def track(self, i):
        return self.tracks[i]

    def __repr__(self):
        track_reprs = map(str, self.tracks)
        return '<MidiFile type={} tpb={}\n    {}>'\
                .format(self.type, self.ticks_per_beat, '\n    '.join(track_reprs))

    def __iter__(self):
        for msg in self.merge_tracks():
            yield msg

    # TODO: generator-ize
    def merge_tracks(self):
        merged = MidiTrack()

        # Convert deltas to absolute time.
        for track in self.tracks:
            now = 0
            for msg in track:
                now += msg.delta

                # TODO: filter out track-specific meta-messages.
                new_msg = msg.copy()
                new_msg.delta = now
                merged.append(new_msg)

        merged.sort(key=lambda m: m.delta)

        # Convert back to deltas.
        last = 0
        for msg in merged:
            msg.delta -= last
            last += msg.delta

        return merged

class MidiTrack(list):
    def __repr__(self):
        messages = map(str, self)
        return '<MidiTrack\n    ' + '\n    '.join(messages) + '>'

def load(f):
    midi_file = MidiFile()

    if not f.read(4) == b'MThd':
        # TODO: MidiError
        raise IOError('No MThd, probably not a MIDI file.')

    header_size = utils.read_long(f)
    midi_file.type = utils.read_short(f)
    num_tracks = utils.read_short(f)
    midi_file.ticks_per_beat = utils.read_short(f)

    # Skip rest of header.
    f.seek(header_size - 6, 1)

    for i in range(num_tracks):
        midi_file.tracks.append(load_track(f))

    return midi_file

def loads(buf):
    f = io.BytesIO(buf)
    return load(f)

def dump(midi_file, f):
    raise NotImplementedError('MidiFile dump')

def dumps(midi_file):
    f = io.BytesIO()
    dump(midi_file, f)
    return f.getvalue()

def load_track(f):
    track = MidiTrack()

    if not f.read(4) == b'MTrk':
        raise IOError('Track doesn\'t contain MTrk.')

    length = utils.read_long(f)
    start = f.tell()

    running_status = None

    while f.tell() - start < length:
        msg = messages.load(f, running_status)

        if msg.type is not 'meta':
            running_status = msg.status

        track.append(msg)

    return track

def loads_track(buf):
    f = io.BytesIO(buf)
    return load_track(f)

def dump_track(track, f):
    raise NotImplementedError('Midi')

def dumps_track(track):
    f = io.BytesIO()
    dump_track(track, f)
    return f.getvalue()
