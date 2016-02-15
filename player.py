#!/usr/bin/env python3
import io
import sys
import math
from itertools import islice, repeat

import midi.files
import synth.generators
import synth.utils
import synth.sinks

TEMPO = 500000

class Player(object):
    def __init__(self):
        self.notes = {'base': repeat(0.0)}
        self.f = io.open('test.pcm', 'wb')

    def mix(self):
        inputs = [v for _, v in self.notes.items()]

        return synth.utils.mix(*inputs)

    def update(self, note, state='on'):
        if state == 'off':
            if note in self.notes:
                del self.notes[note]
        else:
            if note not in self.notes:
                self.notes[note] = synth.generators.sine(synth.utils.midi_to_freq(note))

    def play(self, n_samples):
        synth.sinks.write_pcm(self.f, islice(synth.utils.clip(self.mix()), n_samples))
        #synth.sinks.write_wave(self.f, islice(self.mix(), n_samples))


player = Player()

with io.open('data/smb1-Theme.mid', 'rb') as f:
    smb1 = midi.files.load(f)
    seconds_per_tick = (TEMPO / 1000000.0) / smb1.ticks_per_beat

    #for msg in smb1.track(1):
    for msg in smb1:
        if msg.type == 'meta' and msg['meta_type'] == 'set_tempo':
            seconds_per_tick = (msg['tempo']/ 1000000.0) / smb1.ticks_per_beat
        if msg.type not in ('note_on', 'note_off'):
            continue

        if msg.delta > 0:
            samples = 44100 * seconds_per_tick * msg.delta
            player.play(math.ceil(samples))

        if msg.type == 'note_on' and msg['velocity'] > 0:
            player.update(msg['note'], 'on')
        else:
            player.update(msg['note'], 'off')
