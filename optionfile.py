# optionfile.py
import struct
import os
import constants

class OptionFile:
    def __init__(self):
        self.data = None
        self.filename = None

    def load(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"No se encuentra el archivo: {filename}")
        with open(filename, "rb") as f:
            raw = f.read()
        # Validación básica del tamaño del OF (aproximadamente 1.191.936 bytes)
        if len(raw) < 1190000:
            raise ValueError("El archivo no parece un Option File válido (tamaño incorrecto)")
        self.data = bytearray(raw)
        self.filename = filename
        self._decrypt()
        # Guardar automáticamente el archivo descifrado (para depuración o uso externo)
        try:
            with open("decrypted_OF.bin", "wb") as f:
                f.write(self.data)
        except Exception:
            pass  # Silencioso: no interrumpir si no se puede guardar

    def _decrypt(self):
        # Aplicar XOR con keyPC usando memoryview por eficiencia
        mv = memoryview(self.data)
        k = 0
        for i in range(len(self.data)):
            mv[i] ^= constants.OF_KEY_PC[k] & 0xFF
            k = (k + 1) % 256

        # Descifrado de bloques con memoryview
        for blk in range(1, 10):
            start = constants.OF_BLOCK[blk]
            end = start + constants.OF_BLOCK_SIZE[blk]
            k = 0
            for a in range(start, end - 3, 4):
                # Leer entero little-endian directamente desde memoryview
                c = struct.unpack_from('<I', mv, a)[0]
                p = ((c - constants.OF_KEY[k]) + 0x7AB3684C) ^ 0x7AB3684C
                struct.pack_into('<I', mv, a, p & 0xFFFFFFFF)
                k = (k + 1) % 446

    def get_block(self, start, size):
        return self.data[start:start+size]
