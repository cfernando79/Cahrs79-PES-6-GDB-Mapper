# gui.py
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
from optionfile import OptionFile
from club_db import ClubDatabase
from squad_detector import SquadDetector
from player_db import PlayerDatabase

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
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        self.btn_load = tk.Button(btn_frame, text="Load Option File", command=self.load_file)
        self.btn_load.pack(side=tk.LEFT)

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
            if col == "ID":
                self.filtered_players = [p for p in self.player_db.players if text in str(p.id)]
            elif col == "Name":
                self.filtered_players = [p for p in self.player_db.players if text in p.name.lower()]
            elif col == "Nationality":
                self.filtered_players = [p for p in self.player_db.players if text in p.nationality.lower()]
            elif col == "Club":
                self.filtered_players = [p for p in self.player_db.players if text in p.get_club(self.club_db).lower()]
        self.update_table()

    def clear_filter(self):
        self.filter_var.set("")
        if self.player_db:
            self.filtered_players = self.player_db.players[:]
            self.update_table()