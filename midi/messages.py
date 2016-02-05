from copy import deepcopy

from . import utils

class MidiMessage(dict):
    def copy(self):
        # TODO: Support changing fields here.
        # TODO: Is a shallow copy sufficient here?
        return deepcopy(self)

    def __repr__(self):
        return '<msg {0} delta={1} data={2}>'\
            .format(self.type, self.delta, super().__repr__())

MIN_PITCHWHEEL = -8192
MAX_PITCHWHEEL = 8191

def _parse_note_off(status, f):
    return {
        'channel': status & 0x0f,
        'note': ord(f.read(1)),
        'velocity': ord(f.read(1)),
    }

def _parse_note_on(status, f):
    return {
        'channel': status & 0x0f,
        'note': ord(f.read(1)),
        'velocity': ord(f.read(1)),
    }

def _parse_polytouch(status, f):
    return {
        'channel': status & 0x0f,
        'note': ord(f.read(1)),
        'value': ord(f.read(1)),
    }

def _parse_control_change(status, f):
    return {
        'channel': status & 0x0f,
        'controller': ord(f.read(1)),
        'value': ord(f.read(1)),
    }

def _parse_program_change(status, f):
    return {
        'channel': status & 0x0f,
        'program': ord(f.read(1)),
    }

def _parse_aftertouch(status, f):
    return {
        'channel': status & 0x0f,
        'value': ord(f.read(1)),
    }

def _parse_pitchwheel(status, f):
    data = bytearray(f.read(2))
    pitch = (data[0] | data[1] << 7) + MIN_PITCHWHEEL
    return {
        'channel': status & 0x0f,
        'pitch': pitch
    }

def _parse_meta(status, f):
    type = ord(f.read(1)) # TODO: parse to string
    length = utils.read_variable_int(f)
    return {
        'type': type,
        'data': f.read(length),
    }

_MESSAGE_SPECS = {
    0x80: ('note_off', _parse_note_off),
    0x90: ('note_on', _parse_note_on),
    0xa0: ('polytouch', _parse_polytouch),
    0xb0: ('control_change', _parse_control_change),
    0xc0: ('program_change', _parse_program_change),
    0xd0: ('aftertouch', _parse_aftertouch),
    0xe0: ('pitchwheel', _parse_pitchwheel),
    0xff: ('meta', _parse_meta),
}

# TODO: Support real-time mode.
def load(f, running_status=None, mode='file'):
    msg = MidiMessage()
    msg.delta = utils.read_variable_int(f)

    status = f.peek(1)[0] # Peek usually returns >> 1 byte.

    # All valid status bytes are > 0x80.
    if status < 0x80:
        if running_status is None:
            raise IOError('illegal running status in message')

        status = running_status
    else:
        # Skip status.
        f.seek(1,1)

    spec = _MESSAGE_SPECS.get(status) or _MESSAGE_SPECS.get(status & 0xf0)
    if spec is None:
        raise NotImplementedError('unknown message type: {}'.format(status))

    msg.status = status
    msg.type = spec[0]
    msg.update(spec[1](status, f))

    return msg

def loads(buf, running_status=None, mode='file'):
    f = io.BytesIO(buf)
    return load(f, running_status, mode='file')

def dump(msg, f):
    raise NotImplementedError('MidiMessage dump')

def dumps(msg):
    f = io.BytesIO()
    dump(track, f)
    return f.getvalue()
