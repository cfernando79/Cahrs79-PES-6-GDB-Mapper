# gui.py
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
import os
import json
from optionfile import OptionFile
from club_db import ClubDatabase
from player_db import PlayerDatabase

class MainWindow(tk.Tk):
    CONFIG_FILE = "pes6_config.json"

    @staticmethod
    def save_config(of_path, gdb_path):
        config = {"of_path": of_path, "gdb_path": gdb_path}
        with open(MainWindow.CONFIG_FILE, "w") as f:
            json.dump(config, f)

    @staticmethod
    def load_config():
        if os.path.exists(MainWindow.CONFIG_FILE):
            try:
                with open(MainWindow.CONFIG_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        return {"of_path": "", "gdb_path": ""}

    def __init__(self):
        super().__init__()
        self.title("Cahrs79 PES6 Mapper")
        self.geometry("1000x700")
        self.club_db = None
        self.player_db = None
        self.filtered_players = []
        self.gdb_path = ""

        self.config = self.load_config()
        self._build_ui()

        if self.config.get("of_path"):
            self.status.config(text=f"OF: {self.config['of_path']}")
        if self.config.get("gdb_path"):
            self.gdb_path = self.config["gdb_path"]
            self.status_gdb.config(text=f"GDB: {self.gdb_path}")

    def _build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)

        self.btn_load = tk.Button(btn_frame, text="Cargar Option File", command=self.load_file)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_load_gdb = tk.Button(btn_frame, text="Cargar GDB", command=self.load_gdb)
        self.btn_load_gdb.pack(side=tk.LEFT, padx=5)

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

        self.status = tk.Label(self, text="OF: No cargado", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.status_gdb = tk.Label(self, text="GDB: No cargado", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_gdb.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    def load_file(self):
        last_of = self.config.get("of_path", "")
        if last_of and os.path.exists(os.path.dirname(last_of)):
            initial_dir = os.path.dirname(last_of)
        else:
            initial_dir = str(Path.home() / "Documents")

        filename = filedialog.askopenfilename(
            title="Select PES 6 Option File",
            initialdir=initial_dir,
            filetypes=[("Option files", "KONAMI-WIN32PES6OPT *.bin *.of *.OPT"), ("All files", "*.*")]
        )
        if not filename:
            return

        self.status.config(text="Loading and decrypting...")
        self.update_idletasks()

        try:
            of = OptionFile()
            of.load(filename)
            # Opcional: guardar versión descifrada para depuración (comentado)
            # with open("decrypted_OF.bin", "wb") as f:
            #     f.write(of.data)

            self.club_db = ClubDatabase(of)
            self.player_db = PlayerDatabase(of, self.club_db)
            self.filtered_players = self.player_db.players[:]
            self.update_table()

            self.save_config(filename, self.gdb_path)
            self.config["of_path"] = filename
            self.status.config(text=f"OF: {filename} ({len(self.player_db.players)} players)")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    def load_gdb(self):
        last_path = self.config.get("gdb_path", "")
        if not last_path or not os.path.exists(last_path):
            last_path = os.environ.get('SystemDrive', 'C:') + '\\'

        folder = filedialog.askdirectory(title="Seleccionar carpeta GDB", initialdir=last_path)
        if not folder:
            return

        self.gdb_path = folder
        self.status_gdb.config(text=f"GDB: {folder}")
        self.save_config(self.config.get("of_path", ""), folder)
        self.config["gdb_path"] = folder

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