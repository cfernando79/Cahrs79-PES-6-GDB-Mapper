# club_db.py
import constants

class ClubDatabase:
    def __init__(self, of):
        self.clubs = []
        for i in range(constants.MAX_CLUBS):
            addr = constants.CLUB_START + i * constants.CLUB_SIZE
            name_bytes = of.data[addr:addr+48].split(b'\x00', 1)[0]
            try:
                name = name_bytes.decode('utf-8', errors='replace')
            except UnicodeDecodeError:
                name = f"Club_{i}"
            self.clubs.append(name)

    def get_name(self, idx):
        if 0 <= idx < len(self.clubs):
            return self.clubs[idx]
        return "Free Agent"
