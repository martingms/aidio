def read_long(f):
    d = bytearray(f.read(4))
    return d[0] << 24 | d[1] << 16 | d[2] << 8 | d[3]

def read_short(f):
    d = bytearray(f.read(2))
    return d[0] << 8 | d[1]

def read_variable_int(f):
    i = 0

    while True:
        d = ord(f.read(1))
        i = (i << 7) | (d & 0x7f)
        if d < 0x80:
            return i

def read_nibble(f):
    return ord(f.read(1)) & 0x0f

def read_byte_int(f):
    return ord(f.read(1))
