# player_db.py
import constants
from player import Player

class PlayerDatabase:
    def __init__(self, of, club_db):
        self.players = []
        self._load_players(of, club_db)

    def _build_club_map(self, data):
        """
        Construye un diccionario {id_jugador: índice_club} usando las plantillas
        de los 140 clubes. Asume que cada club tiene 32 jugadores (64 bytes)
        y que el offset base es CLUBS_PLAYERS_RELINK_OFFSET.
        """
        player_club = {}
        for club_idx in range(constants.MAX_CLUBS):
            base = constants.CLUBS_PLAYERS_RELINK_OFFSET + club_idx * constants.CLUB_SLOT_SIZE
            for pos in range(constants.CLUB_PLAYER_COUNT):
                off = base + pos * 2
                if off + 1 < len(data):
                    pid = data[off] | (data[off+1] << 8)
                    if pid != 0 and pid not in player_club:
                        player_club[pid] = club_idx
        return player_club

    def _read_nations(self):
        # Lista fija de nacionalidades (se puede ampliar)
        return [
            "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic",
            "Denmark", "England", "Finland", "France", "Germany", "Greece",
            "Hungary", "Ireland", "Italy", "Latvia", "Netherlands",
            "Northern Ireland", "Norway", "Poland", "Portugal", "Romania",
            "Russia", "Scotland", "Serbia and Montenegro", "Slovakia", "Slovenia",
            "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "Wales",
            "Angola", "Cameroon", "Cote d'Ivoire", "Ghana", "Nigeria",
            "South Africa", "Togo", "Tunisia", "Costa Rica", "Mexico",
            "Trinidad and Tobago", "United States", "Argentina", "Brazil",
            "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay",
            "Iran", "Japan", "Saudi Arabia", "South Korea", "Australia",
            "Bosnia and Herzegovina", "Estonia", "Israel", "Honduras", "Jamaica",
            "Panama", "Bolivia", "Venezuela", "China", "Uzbekistan", "Albania",
            "Cyprus", "Iceland", "Macedonia", "Armenia", "Belarus", "Georgia",
            "Liechtenstein", "Lithuania", "Algeria", "Benin", "Burkina Faso",
            "Cape Verde", "Congo", "DR Congo", "Egypt", "Equatorial Guinea",
            "Gabon", "Gambia", "Guinea", "Guinea-Bissau", "Kenya", "Liberia",
            "Libya", "Mali", "Morocco", "Mozambique", "Senegal", "Sierra Leone",
            "Zambia", "Zimbabwe", "Canada", "Grenada", "Guadeloupe", "Martinique",
            "Netherlands Antilles", "Oman", "New Zealand", "Free Nationality"
        ]

    def _decode_name(self, name_bytes):
        # Buscar terminador nulo (00 00) en UTF-16LE
        for i in range(0, len(name_bytes), 2):
            if i+1 < len(name_bytes) and name_bytes[i] == 0 and name_bytes[i+1] == 0:
                name_bytes = name_bytes[:i]
                break
        try:
            return name_bytes.decode('utf-16le').strip()
        except:
            return name_bytes.decode('latin-1', errors='replace').strip()

    def _load_players(self, of, club_db):
        data = of.data
        nations = self._read_nations()
        player_club_map = self._build_club_map(data)

        addr = constants.PLAYER_START + constants.PLAYER_SIZE
        max_end = min(len(data), constants.PLAYER_START + constants.OF_BLOCK_SIZE[4])
        pid = 1
        while addr + constants.PLAYER_SIZE <= max_end:
            name_bytes = data[addr+constants.NAME_OFFSET:addr+constants.NAME_OFFSET+constants.NAME_LEN]
            name = self._decode_name(name_bytes)
            nation_byte = data[addr+constants.NATION_OFFSET]
            nation = nations[nation_byte] if nation_byte < len(nations) else f"Unknown ({nation_byte})"
            club_idx = player_club_map.get(pid, -1)
            self.players.append(Player(pid, name, nation, club_idx))
            addr += constants.PLAYER_SIZE
            pid += 1
