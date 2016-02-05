import unittest
import io
import os

from . import files

class TestMidi(unittest.TestCase):
    def test_parsing(self):
        with io.open('data/smas61.mid', 'rb') as f:
            mf = files.load(f)

        self.assertIsInstance(mf, files.MidiFile)

if __name__ == '__main__':
    unittest.main()
