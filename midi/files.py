import io

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


class _Parser(object):
    def __init__(self, f):
        try:
            self.file_read = f.read
        except AttributeError:
            raise TypeError('file must provide a \'read\'-function')

    def load(self):
        return MidiFile()

class _Serializer(object):
    def __init__(self, f):
        try:
            self.file_write = f.write
        except AttributeError:
            raise TypeError('file must provide a \'write\'-function')

    def dump(midi_file):
        pass
