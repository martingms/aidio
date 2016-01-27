# Resources:
# http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
# https://github.com/olemb/mido/blob/master/mido/midifiles.py
# https://github.com/olemb/mido/blob/master/mido/messages.py

import io
import sys # TODO: remove

def parse_file(filename):
    midi_file = MidiFile()

    with io.open(filename, 'rb') as f:
        # Parse header.
        if not f.read(4) == b'MThd':
            raise IOError('No MThd, probably not a MIDI file.')

        header_size = _read_long(f)
        midi_file.type = _read_short(f)
        num_tracks = _read_short(f)
        midi_file.ticks_per_beat = _read_short(f)

        # Skip rest of header.
        f.read(header_size - 6)

        for i in xrange(num_tracks):
            midi_file.tracks.append(_parse_track(f))

    return midi_file

def _parse_track(f):
    track = MidiTrack()

    if not f.read(4) == b'MTrk':
        raise IOError('Track doesn\'t contain MTrk.')

    length = _read_long(f)
    start = f.tell()

    running_status = None

    while f.tell() - start < length:
        delta = _read_variable_int(f)

        status = f.peek(1)[:1] # peek(1) often returns >> 1 bytes.
        if status < 0x80:
            if not running_status:
                raise IOError('Illegal running status in track message.')

            status = running_status
        else:
            status = f.read(1)

        if status != 0xff:
            # Meta-messages does not update running status.
            running_status = status

        message = _parse_msg(status, f)
        message.delta = delta

        track.append(message)

    return track

_message_specs = {
    0x80: ('note_off', 3, ('channel', 'note', 'velocity')),
    0x90: ('note_on', 3, ('channel', 'note', 'velocity')),
    0xa0: ('polytouch', 3, ('channel', 'note', 'value')),
    0xb0: ('control_change', 3, ('channel', 'controller', 'value')),
    0xc0: ('program_change', 2, ('channel', 'program')),
    0xd0: ('aftertouch', 2, ('channel', 'value')),
    0xe0: ('pitchwheel', 3, ('channel', 'pitch')),
}

def _parse_msg(status, f):
    if status == 0xff:
        raise NotImplementedError('Meta-messages')
    elif status in [0xf0, 0xf7]:
        raise NotImplementedError('Sysex-messages')

    spec = _message_specs.get(status)
    if not spec:
        spec = _message_specs.get(status & 0xf0)
        status_data = status & 0x0f
    if not spec:
        raise NotImplementedError('Unknown msg type')

    msg = MidiMessage(spec[0])

    return msg

class MidiFile(object):
    def __init__(self):
        self.tracks = []

class MidiTrack(list):
    pass

class MidiMessage(dict):
    def __init__(self, type):
        self['type'] = type

def _read_long(f):
    d = bytearray(f.read(4))
    return d[0] << 24 | d[1] << 16 | d[2] << 8 | d[3]

def _read_short(f):
    d = bytearray(f.read(2))
    return d[0] << 8 | d[1]

def _read_variable_int(f):
    i = 0

    while True:
        d = bytearray(f.read(1))[0] # FIXME: Really the best way?
        i = (i << 7) | (d & 0x7f)
        if d < 0x80:
            return i

if __name__ == '__main__':
    parse_file('smas61.mid')
