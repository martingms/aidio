#!/usr/bin/env python3
import io
import sys
import math
from itertools import islice, count

import midi.files
import synth.generators
import synth.utils
import synth.sinks

TEMPO = 500000

class Player(object):
    def __init__(self):
        self.notes = {}
        self.f = io.open('test.pcm', 'wb')

    def mix(self):
        inputs = [v for _, v in self.notes.items()]
        if len(inputs) == 0:
            return count(0)

        return synth.utils.mix(*inputs)

    def update(self, note, state='on'):
        if state == 'off':
            if note in self.notes:
                del self.notes[note]
        else:
            if note not in self.notes:
                self.notes[note] = synth.generators.sine(synth.utils.midi_to_freq(note))

    def play(self, n_samples):
        #for sample in self.mix():
        #    if sample >= 1.0 or sample <= -1.0:
        #        raise Exception("out of range!")
        #    print(sample)
        synth.sinks.write_pcm(self.f, islice(synth.utils.clip(self.mix()), n_samples))
        #synth.sinks.write_wave(self.f, islice(self.mix(), n_samples))


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
