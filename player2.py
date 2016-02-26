#!/usr/bin/env python3
import io
import sys
import functools

import midi.files
from synth.utils import play_midifile
from synth.sinks import write_pcm
from synth.generators import sine, square
from synth.instruments import MonoSynth, ADSRMonoSynth

if len(sys.argv) < 2:
    print('usage: {} <midifile>'.format(sys.argv[0]))
    sys.exit(1)

with io.open(sys.argv[1], 'rb') as f:
    mf = midi.files.load(f)

instruments = {
    1: ADSRMonoSynth(square),
    2: ADSRMonoSynth(square),
}

write_pcm(sys.stdout.buffer, play_midifile(mf, instruments))
