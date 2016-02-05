from collections import namedtuple

from . import utils

class MidiMessage(dict):
    pass

_MIN_PITCHWHEEL = -8192
_MAX_PITCHWHEEL = 8191

_MESSAGE_SPECS = {
    0x80: ('note_off', (
        ('channel', utils.read_nibble),
        ('note', utils.read_byte_int),
        ('velocity', utils.read_byte_int)
    )),
    0x90: ('note_on', (
        ('channel', utils.read_nibble),
        ('note', utils.read_byte_int),
        ('velocity', utils.read_byte_int)
    )),
    0xa0: ('polytouch', (
        ('channel', utils.read_nibble), 
        ('note', utils.read_byte_int),
        ('value', utils.read_byte_int)
    )),
    0xb0: ('control_change', (
        ('channel', utils.read_nibble),
        ('controller', utils.read_byte_int),
        ('value', utils.read_byte_int)
    )),
    0xc0: ('program_change', (
        ('channel', utils.read_nibble),
        ('program', utils.read_byte_int)
    )),
    0xd0: ('aftertouch', (
        ('channel', utils.read_nibble),
        ('value', utils.read_byte_int)
    )),
    0xe0: ('pitchwheel', (
        ('channel', utils.read_nibble),
        ('pitch', 'not_implemented')
    )),
}

# TODO does it need to be a class?
class _Parser(object):
    # TODO: Support realtime-mode.
    def __init__(self, f, mode='file'):
        self.f = f

    def load(running_status):
        msg = MidiMessage()
        msg.delta = utils.read_variable_int(self.f)

        status = ord(self.f.peek(1)[0])

        # All valid status bytes are > 0x80.
        if status < 0x80:
            if running_status is None:
                raise IOError('illegal running status in message')

            status = running_status
        #else:
        #    # Skip already peeked status byte.
        #    self.f.seek(1, 1)

        spec = _MESSAGE_SPECS.get(status) or _MESSAGE_SPECS.get(status & 0xf0)
        if spec is None:
            raise NotImplementedError('unknown message type')

        msg.type = spec[0]

        for field, parser in spec[1]:
            msg[field] = parser(self.f)

        return msg

class _Serializer(object):
    pass

### Old
_MsgSpec = namedtuple('MsgSpec', ('type', 'length', 'fields'))
_message_specs = {
    0x80: _MsgSpec('note_off', 3, ('channel', 'note', 'velocity')),
    0x90: _MsgSpec('note_on', 3, ('channel', 'note', 'velocity')),
    0xa0: _MsgSpec('polytouch', 3, ('channel', 'note', 'value')),
    0xb0: _MsgSpec('control_change', 3, ('channel', 'controller', 'value')),
    0xc0: _MsgSpec('program_change', 2, ('channel', 'program')),
    0xd0: _MsgSpec('aftertouch', 2, ('channel', 'value')),
    0xe0: _MsgSpec('pitchwheel', 3, ('channel', 'pitch')),
}

def parse_msg(status, f):
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

    msg = Message({'type': spec.type})

    length = spec.length
    fields = spec.fields
    if status_data:
        msg[fields[0]] = status_data
        fields = fields[1:]


    return msg
