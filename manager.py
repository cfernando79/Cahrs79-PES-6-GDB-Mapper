import tkinter as tk
from tkinter import filedialog, ttk
import struct
from pathlib import Path

# ------------------------------------------------------------
# CONSTANTES GLOBALES (se pueden mover a una clase Config)
# ------------------------------------------------------------
OF_BLOCK = [12, 5144, 9544, 14288, 37116, 657956, 751472, 763804, 911144, 1170520]
OF_BLOCK_SIZE = [4844, 1268, 4730, 22816, 620000, 93501, 12320, 147328, 259364, 21032]

# ========== COMPLETAR CON TUS LISTAS ==========
OF_KEY = [
    2058578050, 2058578078, 2058578109, 2058578079, 2058578084, 2058578115,
    2058578073, 2058578105, 2058578068, 2058578101, 2058578095, 2058578045,
    2058578100, 2058578111, 2058578096, 2058578068, 2058578101, 2058578117,
    2058578115, 2058578071, 2058578064, 2058578045, 2058578078, 2058578085,
    2058578062, 2058578116, 2058578109, 2058578045, 2058578115, 2058578076,
    2058578049, 2058578093, 2058578066, 2058578051, 2058578082, 2058578114,
    2058578045, 2058578093, 2058578052, 2058578112, 2058578073, 2058578063,
    2058578100, 2058578102, 2058578103, 2058578053, 2058578085, 2058578078,
    2058578077, 2058578115, 2058578076, 2058578086, 2058578116, 2058578111,
    2058578083, 2058578109, 2058578072, 2058578047, 2058578081, 2058578049,
    2058578074, 2058578048, 2058578086, 2058578110, 2058578098, 2058578102,
    2058578105, 2058578050, 2058578046, 2058578086, 2058578095, 2058578083,
    2058578065, 2058578062, 2058578047, 2058578116, 2058578109, 2058578100,
    2058578068, 2058578100, 2058578109, 2058578104, 2058578079, 2058578084,
    2058578084, 2058578083, 2058578084, 2058578098, 2058578096, 2058578070,
    2058578068, 2058578110, 2058578094, 2058578045, 2058578114, 2058578082,
    2058578116, 2058578068, 2058578114, 2058578097, 2058578085, 2058578115,
    2058578072, 2058578068, 2058578047, 2058578099, 2058578076, 2058578101,
    2058578086, 2058578117, 2058578052, 2058578109, 2058578070, 2058578050,
    2058578118, 2058578046, 2058578109, 2058578098, 2058578099, 2058578064,
    2058578048, 2058578103, 2058578069, 2058578075, 2058578068, 2058578085,
    2058578110, 2058578111, 2058578114, 2058578110, 2058578081, 2058578084,
    2058578077, 2058578073, 2058578084, 2058578100, 2058578104, 2058578063,
    2058578083, 2058578049, 2058578065, 2058578109, 2058578105, 2058578099,
    2058578105, 2058578062, 2058578069, 2058578070, 2058578065, 2058578066,
    2058578047, 2058578100, 2058578107, 2058578077, 2058578062, 2058578050,
    2058578113, 2058578080, 2058578065, 2058578083, 2058578095, 2058578111,
    2058578096, 2058578044, 2058578116, 2058578053, 2058578084, 2058578077,
    2058578118, 2058578100, 2058578072, 2058578044, 2058578073, 2058578104,
    2058578117, 2058578074, 2058578069, 2058578110, 2058578050, 2058578045,
    2058578045, 2058578047, 2058578047, 2058578106, 2058578064, 2058578099,
    2058578095, 2058578063, 2058578067, 2058578068, 2058578049, 2058578108,
    2058578098, 2058578115, 2058578099, 2058578097, 2058578106, 2058578097,
    2058578116, 2058578116, 2058578110, 2058578118, 2058578099, 2058578111,
    2058578106, 2058578109, 2058578101, 2058578093, 2058578077, 2058578053,
    2058578061, 2058578098, 2058578050, 2058578086, 2058578104, 2058578098,
    2058578113, 2058578102, 2058578065, 2058578077, 2058578082, 2058578044,
    2058578050, 2058578085, 2058578117, 2058578045, 2058578117, 2058578113,
    2058578082, 2058578051, 2058578110, 2058578103, 2058578096, 2058578069,
    2058578052, 2058578114, 2058578046, 2058578044, 2058578047, 2058578108,
    2058578083, 2058578075, 2058578077, 2058578069, 2058578050, 2058578101,
    2058578063, 2058578082, 2058578052, 2058578108, 2058578106, 2058578109,
    2058578112, 2058578062, 2058578071, 2058578051, 2058578047, 2058578097,
    2058578062, 2058578100, 2058578048, 2058578080, 2058578080, 2058578077,
    2058578047, 2058578048, 2058578096, 2058578100, 2058578118, 2058578105,
    2058578096, 2058578072, 2058578085, 2058578084, 2058578061, 2058578114,
    2058578044, 2058578049, 2058578053, 2058578093, 2058578064, 2058578049,
    2058578083, 2058578069, 2058578073, 2058578104, 2058578080, 2058578098,
    2058578103, 2058578093, 2058578049, 2058578044, 2058578099, 2058578094,
    2058578070, 2058578103, 2058578070, 2058578062, 2058578078, 2058578102,
    2058578104, 2058578109, 2058578068, 2058578067, 2058578108, 2058578108,
    2058578076, 2058578086, 2058578053, 2058578104, 2058578093, 2058578070,
    2058578105, 2058578110, 2058578094, 2058578112, 2058578086, 2058578049,
    2058578101, 2058578086, 2058578108, 2058578071, 2058578095, 2058578079,
    2058578097, 2058578116, 2058578111, 2058578046, 2058578103, 2058578071,
    2058578067, 2058578063, 2058578096, 2058578048, 2058578079, 2058578103,
    2058578068, 2058578114, 2058578079, 2058578072, 2058578102, 2058578115,
    2058578053, 2058578047, 2058578084, 2058578046, 2058578110, 2058578044,
    2058578108, 2058578101, 2058578078, 2058578073, 2058578086, 2058578049,
    2058578107, 2058578069, 2058578077, 2058578086, 2058578079, 2058578110,
    2058578048, 2058578116, 2058578101, 2058578108, 2058578081, 2058578093,
    2058578113, 2058578065, 2058578045, 2058578080, 2058578109, 2058578075,
    2058578097, 2058578071, 2058578049, 2058578053, 2058578078, 2058578050,
    2058578075, 2058578067, 2058578083, 2058578061, 2058578116, 2058578116,
    2058578075, 2058578093, 2058578116, 2058578100, 2058578093, 2058578052,
    2058578085, 2058578047, 2058578095, 2058578081, 2058578045, 2058578044,
    2058578101, 2058578097, 2058578110, 2058578115, 2058578096, 2058578069,
    2058578053, 2058578050, 2058578112, 2058578085, 2058578104, 2058578082,
    2058578073, 2058578099, 2058578081, 2058578045, 2058578079, 2058578071,
    2058578080, 2058578047, 2058578113, 2058578076, 2058578082, 2058578117,
    2058578086, 2058578046, 2058578099, 2058578068, 2058578074, 2058578108,
    2058578064, 2058578077, 2058578115, 2058578066, 2058578074, 2058578104,
    2058578082, 2058578115, 2058578117, 2058578082, 2058578117, 2058578048,
    2058578053, 2058578107, 2058578079, 2058578116, 2058578081, 2058578086,
    2058578064, 2058577996
]

# Clave de 256 elementos (keyPC)
OF_KEY_PC = [
    115, 96, -31, -58, 31, 60, -83, 66, 11, 88, -71, -2, 55, -76, 5, -6,
    -93, 80, -111, 54, 79, 44, 93, -78, 59, 72, 105, 110, 103, -92, -75, 106,
    -45, 64, 65, -90, 127, 28, 13, 34, 107, 56, 25, -34, -105, -108, 101, -38,
    3, 48, -15, 22, -81, 12, -67, -110, -101, 40, -55, 78, -57, -124, 21, 74,
    51, 32, -95, -122, -33, -4, 109, 2, -53, 24, 121, -66, -9, 116, -59, -70,
    99, 16, 81, -10, 15, -20, 29, 114, -5, 8, 41, 46, 39, 100, 117, 42,
    -109, 0, 1, 102, 63, -36, -51, -30, 43, -8, -39, -98, 87, 84, 37, -102,
    -61, -16, -79, -42, 111, -52, 125, 82, 91, -24, -119, 14, -121, 68, -43, 10,
    -13, -32, 97, 70, -97, -68, 45, -62, -117, -40, 57, 126, -73, 52, -123, 122,
    35, -48, 17, -74, -49, -84, -35, 50, -69, -56, -23, -18, -25, 36, 53, -22,
    83, -64, -63, 38, -1, -100, -115, -94, -21, -72, -103, 94, 23, 20, -27, 90,
    -125, -80, 113, -106, 47, -116, 61, 18, 27, -88, 73, -50, 71, 4, -107, -54,
    -77, -96, 33, 6, 95, 124, -19, -126, 75, -104, -7, 62, 119, -12, 69, 58,
    -29, -112, -47, 118, -113, 108, -99, -14, 123, -120, -87, -82, -89, -28, -11, -86,
    19, -128, -127, -26, -65, 92, 77, 98, -85, 120, 89, 30, -41, -44, -91, 26,
    67, 112, 49, 86, -17, 76, -3, -46, -37, 104, 9, -114, 7, -60, 85, -118
]

# =============================================

PLAYER_START = 37116
PLAYER_SIZE = 124
NAME_OFFSET = 0
NAME_LEN = 32
NATION_OFFSET = 112

CLUB_START = 751472
CLUB_SIZE = 88
MAX_CLUBS = 140

# ------------------------------------------------------------
# CLASE OptionFile: carga, descifrado y acceso a datos
# ------------------------------------------------------------
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
        # Convertir datos con keyPC
        k = 0
        for i in range(len(self.data)):
            self.data[i] ^= OF_KEY_PC[k] & 0xFF
            k = (k + 1) % 256
        # Descifrar bloques
        for blk in range(1, 10):
            start = OF_BLOCK[blk]
            end = start + OF_BLOCK_SIZE[blk]
            k = 0
            for a in range(start, end - 3, 4):
                c = struct.unpack_from('<I', self.data, a)[0]
                p = ((c - OF_KEY[k]) + 0x7AB3684C) ^ 0x7AB3684C
                struct.pack_into('<I', self.data, a, p & 0xFFFFFFFF)
                k = (k + 1) % 446

    def get_block(self, start, size):
        return self.data[start:start+size]

# ------------------------------------------------------------
# CLASE ClubDatabase: lee y proporciona nombres de clubes
# ------------------------------------------------------------
class ClubDatabase:
    def __init__(self, of):
        self.clubs = []
        for i in range(MAX_CLUBS):
            addr = CLUB_START + i * CLUB_SIZE
            name_bytes = of.data[addr:addr+48].split(b'\x00', 1)[0]
            name = name_bytes.decode('utf-8', errors='ignore')
            self.clubs.append(name)

    def get_name(self, idx):
        if 0 <= idx < len(self.clubs):
            return self.clubs[idx]
        return "Free Agent"

# ------------------------------------------------------------
# CLASE SquadDetector: encuentra las direcciones de las plantillas
# ------------------------------------------------------------
class SquadDetector:
    @staticmethod
    def find_slot23(data):
        """Retorna la dirección de inicio de las plantillas de 23 jugadores."""
        best_start = None
        best_cnt = 0
        limit = min(len(data), 1024*1024)
        for start in range(0, limit - 46, 2):
            cnt = 0
            for i in range(23):
                off = start + i*2
                pid = data[off] | (data[off+1] << 8)
                if 1 <= pid <= 5000:
                    cnt += 1
            if cnt > best_cnt:
                best_cnt = cnt
                best_start = start
                if cnt >= 20:   # ya es suficientemente bueno
                    break
        return best_start

    @staticmethod
    def find_slot32(data):
        """Retorna la dirección de inicio de las plantillas de 32 jugadores."""
        best_start = None
        best_cnt = 0
        limit = min(len(data), 1024*1024)
        for start in range(0, limit - 64, 2):
            cnt = 0
            for i in range(32):
                off = start + i*2
                pid = data[off] | (data[off+1] << 8)
                if 1 <= pid <= 5000:
                    cnt += 1
            if cnt > best_cnt:
                best_cnt = cnt
                best_start = start
                if cnt >= 20:
                    break
        return best_start

# ------------------------------------------------------------
# CLASE Player: representa un jugador
# ------------------------------------------------------------
class Player:
    def __init__(self, pid, name, nationality, club_idx):
        self.id = pid
        self.name = name
        self.nationality = nationality
        self.club_idx = club_idx

    def get_club(self, club_db):
        return club_db.get_name(self.club_idx)

# ------------------------------------------------------------
# CLASE PlayerDatabase: carga todos los jugadores desde el OF
# ------------------------------------------------------------
class PlayerDatabase:
    def __init__(self, of, club_db, slot23, slot32):
        self.players = []
        self._load_players(of, club_db, slot23, slot32)

    def _build_club_map(self, data, slot23, slot32):
        """Construye un diccionario {player_id: club_index} usando las plantillas."""
        player_club = {}
        # Clubes 0-63 (23 jugadores)
        for club in range(64):
            base = slot23 + club * 46
            for pos in range(23):
                off = base + pos*2
                pid = data[off] | (data[off+1] << 8)
                if pid and pid not in player_club:
                    player_club[pid] = club
        # Clubes 64-139 (32 jugadores)
        for club in range(64, MAX_CLUBS):
            base = slot32 + (club - 64) * 64
            for pos in range(32):
                off = base + pos*2
                pid = data[off] | (data[off+1] << 8)
                if pid and pid not in player_club:
                    player_club[pid] = club
        return player_club

    def _read_nations(self):
        # Lista por defecto (puedes externalizarla)
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
        for i in range(0, len(name_bytes), 2):
            if i+1 < len(name_bytes) and name_bytes[i] == 0 and name_bytes[i+1] == 0:
                name_bytes = name_bytes[:i]
                break
        try:
            return name_bytes.decode('utf-16le').strip()
        except:
            return name_bytes.decode('latin-1', errors='ignore').strip()

    def _load_players(self, of, club_db, slot23, slot32):
        data = of.data
        nations = self._read_nations()
        player_club_map = self._build_club_map(data, slot23, slot32)

        addr = PLAYER_START + PLAYER_SIZE   # saltar primer registro vacío
        max_end = min(len(data), PLAYER_START + OF_BLOCK_SIZE[4])
        pid = 1
        while addr + PLAYER_SIZE <= max_end:
            # Leer nombre
            name_bytes = data[addr+NAME_OFFSET:addr+NAME_OFFSET+NAME_LEN]
            name = self._decode_name(name_bytes)
            # Nacionalidad
            nation_byte = data[addr+NATION_OFFSET]
            nation = nations[nation_byte] if nation_byte < len(nations) else f"Unknown ({nation_byte})"
            # Club
            club_idx = player_club_map.get(pid)
            if club_idx is None:
                club_idx = -1   # Free Agent
            self.players.append(Player(pid, name, nation, club_idx))
            addr += PLAYER_SIZE
            pid += 1

    def filter(self, col, value):
        """Devuelve lista de jugadores que coinciden con el filtro."""
        value = value.lower()
        if col == "ID":
            return [p for p in self.players if value in str(p.id)]
        elif col == "Name":
            return [p for p in self.players if value in p.name.lower()]
        elif col == "Nationality":
            return [p for p in self.players if value in p.nationality.lower()]
        elif col == "Club":
            return [p for p in self.players if value in p.get_club(club_db).lower()]
        else:
            return self.players[:]

# ------------------------------------------------------------
# CLASE MainWindow: interfaz gráfica
# ------------------------------------------------------------
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PES 6 Option File Viewer")
        self.geometry("1000x700")
        self.club_db = None
        self.player_db = None
        self.filtered_players = []
        self._build_ui()

    def _build_ui(self):
        # Configurar grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Botón de carga
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        self.btn_load = tk.Button(btn_frame, text="Load Option File", command=self.load_file)
        self.btn_load.pack(side=tk.LEFT)

        # Filtros
        filter_frame = tk.Frame(self)
        filter_frame.grid(row=1, column=0, sticky="ew", pady=5, padx=10)
        tk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar()
        self.filter_entry = tk.Entry(filter_frame, textvariable=self.filter_var, width=30)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_entry.bind("<KeyRelease>", self.apply_filter)
        self.filter_col = tk.StringVar(value="Name")
        col_menu = ttk.Combobox(filter_frame, textvariable=self.filter_col, values=["ID", "Name", "Nationality", "Club"], width=12)
        col_menu.pack(side=tk.LEFT, padx=5)
        self.btn_clear = tk.Button(filter_frame, text="Clear", command=self.clear_filter)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        # Tabla
        columns = ("ID", "Name", "Nationality", "Club")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=25)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Nationality", text="Nationality")
        self.tree.heading("Club", text="Club")
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Name", width=250)
        self.tree.column("Nationality", width=180)
        self.tree.column("Club", width=250)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        vsb.grid(row=2, column=1, sticky="ns")
        hsb.grid(row=3, column=0, sticky="ew")

        self.status = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Select PES 6 Option File",
            initialdir=str(Path.home() / "Documents"),
            filetypes=[("Option files", "KONAMI-WIN32PES6OPT *.bin *.of *.OPT"), ("All files", "*.*")]
        )
        if not filename:
            return
        self.status.config(text="Loading and decrypting...")
        self.update()
        try:
            of = OptionFile()
            of.load(filename)
            self.club_db = ClubDatabase(of)
            slot23 = SquadDetector.find_slot23(of.data)
            slot32 = SquadDetector.find_slot32(of.data)
            if slot23 is None or slot32 is None:
                self.status.config(text="Error: no se encontraron las plantillas de clubes")
                return
            self.player_db = PlayerDatabase(of, self.club_db, slot23, slot32)
            self.filtered_players = self.player_db.players[:]
            self.update_table()
            self.status.config(text=f"Loaded {len(self.player_db.players)} players")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in self.filtered_players:
            club_name = p.get_club(self.club_db)
            self.tree.insert("", tk.END, values=(p.id, p.name, p.nationality, club_name))

    def apply_filter(self, event=None):
        if not self.player_db:
            return
        text = self.filter_var.get().lower()
        col = self.filter_col.get()
        if not text:
            self.filtered_players = self.player_db.players[:]
        else:
            self.filtered_players = self.player_db.filter(col, text)
        self.update_table()

    def clear_filter(self):
        self.filter_var.set("")
        if self.player_db:
            self.filtered_players = self.player_db.players[:]
            self.update_table()

# ------------------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------------------
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
