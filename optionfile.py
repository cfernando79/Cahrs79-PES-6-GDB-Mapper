# optionfile.py
import struct
import constants

class OptionFile:
    def __init__(self):
        self.data = None
        self.filename = None

    def load(self, filename):
        with open(filename, "rb") as f:
            self.data = bytearray(f.read())
        self.filename = filename
        self._decrypt()

    def _decrypt(self):
        k = 0
        for i in range(len(self.data)):
            self.data[i] ^= constants.OF_KEY_PC[k] & 0xFF
            k = (k + 1) % 256
        for blk in range(1, 10):
            start = constants.OF_BLOCK[blk]
            end = start + constants.OF_BLOCK_SIZE[blk]
            k = 0
            for a in range(start, end - 3, 4):
                c = struct.unpack_from('<I', self.data, a)[0]
                p = ((c - constants.OF_KEY[k]) + 0x7AB3684C) ^ 0x7AB3684C
                struct.pack_into('<I', self.data, a, p & 0xFFFFFFFF)
                k = (k + 1) % 446

    def get_block(self, start, size):
        return self.data[start:start+size]