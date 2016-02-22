#!/usr/bin/python3
import sys
import io

import midi.files

if len(sys.argv) < 2:
    print('usage: {} <midifile>'.format(sys.argv[0]))
    sys.exit(1)

with io.open(sys.argv[1], 'rb') as f:
    print(midi.files.load(f))
