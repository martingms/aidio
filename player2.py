#!/usr/bin/env python3
import io
import functools

import midi.files
from synth.players import play_midifile
from synth.sinks import write_pcm
from synth.generators import sine, square
from synth.instruments import MonoSynth

with io.open('data/smb1-Theme.mid', 'rb') as f:
    mf = midi.files.load(f)

instruments = {
    1: MonoSynth(square),
    2: MonoSynth(square),
}

with io.open('test2.pcm', 'wb') as out:
    write_pcm(out, play_midifile(mf, instruments))
