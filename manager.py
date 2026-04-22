mport tkinter as tk
from tkinter import filedialog, ttk
import struct
from pathlib import Path

# ------------------------------------------------------------
# CONSTANTES (rellena con tus claves)
# ------------------------------------------------------------
OF_BLOCK = [12, 5144, 9544, 14288, 37116, 657956, 751472, 763804, 911144, 1170520]
OF_BLOCK_SIZE = [4844, 1268, 4730, 22816, 620000, 93501, 12320, 147328, 259364, 21032]
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

PLAYER_START = 37116
PLAYER_SIZE = 124
NAME_OFFSET = 0
NAME_LEN = 32
NATION_OFFSET = 112
CLUB_START = 751472
CLUB_SIZE = 88
MAX_CLUBS = 140

# ------------------------------------------------------------
# DESCIFRADO RÁPIDO
# ------------------------------------------------------------
def decrypt_of(data):
    k = 0
    for i in range(len(data)):
        data[i] ^= OF_KEY_PC[k] & 0xFF
        k = (k + 1) % 256
    for blk in range(1, 10):
        start = OF_BLOCK[blk]
        end = start + OF_BLOCK_SIZE[blk]
        k = 0
        for a in range(start, end - 3, 4):
            c = struct.unpack_from('<I', data, a)[0]
            p = ((c - OF_KEY[k]) + 0x7AB3684C) ^ 0x7AB3684C
            struct.pack_into('<I', data, a, p & 0xFFFFFFFF)
            k = (k + 1) % 446

# ------------------------------------------------------------
# DETECCIÓN DE PLANTILLAS (rápida)
# ------------------------------------------------------------
def find_squads(data):
    # Usar memoryview para acelerar acceso
    mv = memoryview(data)
    best23 = best32 = None
    best23_cnt = best32_cnt = 0
    # Escanear solo hasta 1M (las plantillas están temprano)
    limit = min(len(data), 1024*1024)
    for start in range(0, limit - 64, 2):
        # Probar bloque de 23 (46 bytes)
        cnt23 = 0
        for i in range(23):
            off = start + i*2
            pid = mv[off] | (mv[off+1] << 8)
            if 1 <= pid <= 5000:
                cnt23 += 1
        if cnt23 > best23_cnt:
            best23_cnt = cnt23
            best23 = start
            if cnt23 >= 20:
                # Ya es muy bueno, pero seguimos buscando secuencias
                pass
        # Probar bloque de 32 (64 bytes)
        cnt32 = 0
        for i in range(32):
            off = start + i*2
            pid = mv[off] | (mv[off+1] << 8)
            if 1 <= pid <= 5000:
                cnt32 += 1
        if cnt32 > best32_cnt:
            best32_cnt = cnt32
            best32 = start
    # Verificar que sean inicios de secuencias consecutivas (opcional)
    # Aquí simplificamos: devolvemos los mejores encontrados
    return best23, best32

# ------------------------------------------------------------
# CONSTRUIR MAPA JUGADOR->CLUB
# ------------------------------------------------------------
def build_map(data, slot23, slot32):
    mv = memoryview(data)
    player_club = {}
    # Clubes 0-63 (23 jugadores)
    for club in range(64):
        base = slot23 + club * 46
        for pos in range(23):
            off = base + pos*2
            pid = mv[off] | (mv[off+1] << 8)
            if pid and pid not in player_club:
                player_club[pid] = club
    # Clubes 64-139 (32 jugadores)
    for club in range(64, MAX_CLUBS):
        base = slot32 + (club - 64) * 64
        for pos in range(32):
            off = base + pos*2
            pid = mv[off] | (mv[off+1] << 8)
            if pid and pid not in player_club:
                player_club[pid] = club
    return player_club

# ------------------------------------------------------------
# LECTURA DE JUGADORES (optimizada)
# ------------------------------------------------------------
def read_players(data, clubs, nations, player_club):
    mv = memoryview(data)
    players = []
    # Saltar primer registro vacío
    addr = PLAYER_START + PLAYER_SIZE
    max_end = min(len(data), PLAYER_START + OF_BLOCK_SIZE[4])
    idx = 1
    while addr + PLAYER_SIZE <= max_end:
        # Nombre UTF-16LE
        name_bytes = mv[addr:addr+NAME_LEN]
        # Buscar terminador
        for i in range(0, NAME_LEN, 2):
            if name_bytes[i] == 0 and name_bytes[i+1] == 0:
                name_bytes = name_bytes[:i]
                break
        name = name_bytes.tobytes().decode('utf-16le', errors='ignore').strip()
        # Nacionalidad
        nation_byte = mv[addr+NATION_OFFSET]
        nation = nations[nation_byte] if nation_byte < len(nations) else f"Unknown ({nation_byte})"
        # Club
        club_idx = player_club.get(idx)
        club_name = clubs[club_idx] if club_idx is not None and 0 <= club_idx < len(clubs) else "Free Agent"
        players.append((idx, name, nation, club_name))
        addr += PLAYER_SIZE
        idx += 1
    return players

# ------------------------------------------------------------
# INTERFAZ (Treeview virtual para rapidez)
# ------------------------------------------------------------
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PES 6 OF Reader")
        self.root.geometry("900x600")
        self.tree = ttk.Treeview(self.root, columns=("ID","Name","Nation","Club"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Nation", text="Nationality")
        self.tree.heading("Club", text="Club")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=200)
        self.tree.column("Nation", width=150)
        self.tree.column("Club", width=200)
        vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        btn = tk.Button(self.root, text="Load Option File", command=self.load)
        btn.grid(row=2, column=0, pady=5)
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.grid(row=3, column=0, sticky="ew", padx=5)
        self.players = []

    def load(self):
        fname = filedialog.askopenfilename(initialdir=str(Path.home()/"Documents"),
                                           filetypes=[("Option files", "KONAMI-WIN32PES6OPT *.bin *.of"), ("All","*.*")])
        if not fname: return
        self.status.config(text="Loading...")
        self.root.update()
        try:
            with open(fname, "rb") as f:
                raw = bytearray(f.read())
            decrypt_of(raw)
            # Leer nombres de clubes
            clubs = []
            for i in range(MAX_CLUBS):
                addr = CLUB_START + i * CLUB_SIZE
                name_bytes = raw[addr:addr+48].split(b'\x00',1)[0]
                clubs.append(name_bytes.decode('utf-8', errors='ignore'))
            # Nacionalidades (lista fija)
            nations = ["Austria","Belgium","Bulgaria","Croatia","Czech Republic","Denmark","England","Finland","France","Germany","Greece","Hungary","Ireland","Italy","Latvia","Netherlands","Northern Ireland","Norway","Poland","Portugal","Romania","Russia","Scotland","Serbia and Montenegro","Slovakia","Slovenia","Spain","Sweden","Switzerland","Turkey","Ukraine","Wales","Angola","Cameroon","Cote d'Ivoire","Ghana","Nigeria","South Africa","Togo","Tunisia","Costa Rica","Mexico","Trinidad and Tobago","United States","Argentina","Brazil","Chile","Colombia","Ecuador","Paraguay","Peru","Uruguay","Iran","Japan","Saudi Arabia","South Korea","Australia","Bosnia and Herzegovina","Estonia","Israel","Honduras","Jamaica","Panama","Bolivia","Venezuela","China","Uzbekistan","Albania","Cyprus","Iceland","Macedonia","Armenia","Belarus","Georgia","Liechtenstein","Lithuania","Algeria","Benin","Burkina Faso","Cape Verde","Congo","DR Congo","Egypt","Equatorial Guinea","Gabon","Gambia","Guinea","Guinea-Bissau","Kenya","Liberia","Libya","Mali","Morocco","Mozambique","Senegal","Sierra Leone","Zambia","Zimbabwe","Canada","Grenada","Guadeloupe","Martinique","Netherlands Antilles","Oman","New Zealand","Free Nationality"]
            # Detectar plantillas
            slot23, slot32 = find_squads(raw)
            if slot23 is None or slot32 is None:
                self.status.config(text="Error: no se encontraron plantillas")
                return
            player_map = build_map(raw, slot23, slot32)
            # Leer jugadores
            self.players = read_players(raw, clubs, nations, player_map)
            # Llenar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            for p in self.players:
                self.tree.insert("", tk.END, values=p)
            self.status.config(text=f"Cargados {len(self.players)} jugadores")
        except Exception as e:
            self.status.config(text=f"Error: {e}")
            import traceback
            traceback.print_exc()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()
