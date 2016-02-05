#!/usr/bin/env python3
import io
import sys
import math
from itertools import islice

import midi.files
import synth.generators
import synth.utils
import synth.sinks

TEMPO = 500000

class Player(object):
    def __init__(self):
        self.notes = {}

    def mix(self):
        return synth.utils.mix(*[v for _, v in self.notes.items()])

    def update(self, note, state='on'):
        if state == 'off':
            try:
                del self.notes[note]
            except KeyError:
                raise Exception('off on note that was never on')

        if note not in self.notes:
            self.notes[note] = synth.generators.sine(synth.utils.midi_to_freq(note))

    def play(self, n_samples):
        for sample in self.mix():
            print(sample)
        #synth.sinks.write_pcm(sys.stdout.buffer, islice(self.mix(), n_samples))


player = Player()

with io.open('data/smas61.mid', 'rb') as f:
    smas61 = midi.files.load(f)
    seconds_per_tick = (TEMPO / 1000000.0) / smas61.ticks_per_beat

    for msg in smas61:
        if msg.type not in ('note_on', 'note_off'):
            continue

        if msg.delta > 0:
            samples = 44100 * seconds_per_tick * msg.delta
            player.play(math.ceil(samples))

        if msg.type == 'note_on' and msg['velocity'] > 0:
            player.update(msg['note'], 'on')
        else:
            player.update(msg['note'], 'off')
