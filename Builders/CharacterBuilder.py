import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from enum import Enum

class ColorMap(Enum):
    Black = "\033[30;1m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"
    Pink = "\033[38;5;201m"
    Orange = "\033[38;5;208m"
    Purple = "\033[38;5;129m"
    Lime = "\033[38;5;157m"
    Gold = "\033[38;5;220m"
    Lavender = "\033[38;5;183m"

techniques = ["None", "Limitless", "Shrine", "Private Pure Love Train", "Idle Transfiguration", "Copy"]
domains = ["None", "Infinite Void", "Malevolent Shrine", "Authentic Mutual Love", "Idle Death Gamble", "Self Embodiment of Perfection"]
counter_domains = ["None", "Simple Domain", "Hollow Wicker Basket"]
specials = ["None", "Unlimited Purple", "World Cutting Slash"]
shikigami_list = ["Rika", "Mahoraga", "Agito"]
tools_list = ["The Inverted Spear of Heaven", "Playful Cloud", "Split Soul Katana", "Katana"]
ai_types = ["Aggressive", "Reactive", "Brawler", "Randomized"]
rct_levels = ["None", "Crude", "Adept", "Expert", "Absolute"]

def ResolveLabelColors(root):
    tmp = tk.Label(root)
    normal = tmp.cget("foreground") or "black"
    tmp.destroy()
    return normal, "gray"

label_normal = "black"
label_dim = "gray"

def MakeScrollableTab(notebook, title):
    outer = ttk.Frame(notebook)
    canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner = ttk.Frame(canvas, padding=(16, 10))

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    notebook.add(outer, text=title)
    return inner

def MakeLabel(parent, row, text):
    lbl = tk.Label(parent, text=text, anchor="w")
    lbl.grid(row=row, column=0, sticky="w", pady=4, padx=(0, 10))
    return lbl

def CreateSpinbox(parent, row, text, default, lo=0, hi=99999, width=12):
    lbl = MakeLabel(parent, row, text)
    s = ttk.Spinbox(parent, from_=lo, to=hi, width=width)
    s.delete(0, "end")
    s.insert(0, str(default))
    s.grid(row=row, column=1, sticky="w", pady=4)
    return lbl, s

def CreateCombobox(parent, row, text, values, default, width=22):
    lbl = MakeLabel(parent, row, text)
    c = ttk.Combobox(parent, values=values, state="readonly", width=width)
    c.set(default)
    c.grid(row=row, column=1, sticky="w", pady=4)
    return lbl, c

def SetGroup(enabled, *pairs):
    fg = label_normal if enabled else label_dim
    state = "normal" if enabled else "disabled"
    for lbl, widget in pairs:
        lbl.config(fg=fg)
        widget.config(state=state)

def SetComboGroup(enabled, *pairs):
    fg = label_normal if enabled else label_dim
    state = "readonly" if enabled else "disabled"
    for lbl, widget in pairs:
        lbl.config(fg=fg)
        widget.config(state=state)

class MultiSelect(tk.Frame):
    def __init__(self, parent, items, height=4, **kwargs):
        super().__init__(parent, **kwargs)
        lb_frame = ttk.Frame(self)
        lb_frame.pack(fill="both", expand=True)
        sb = ttk.Scrollbar(lb_frame, orient="vertical")
        self.listbox = tk.Listbox(lb_frame, selectmode="multiple", height=height,
                                  yscrollcommand=sb.set, exportselection=False,
                                  relief="flat", borderwidth=1)
        sb.config(command=self.listbox.yview)
        self.listbox.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for item in items:
            self.listbox.insert("end", item)

    def GetSelected(self):
        return [self.listbox.get(i) for i in self.listbox.curselection()]

class CharacterCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorcerer Showdown - Character Designer")
        self.root.geometry("520x600")
        self.root.resizable(False, False)
        self.BuildUi()

    def BuildUi(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=6, pady=6)

        self.TabBasics(notebook)
        self.TabCombat(notebook)
        self.TabTechniques(notebook)
        self.TabTools(notebook)
        self.TabAdvanced(notebook)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=(0, 8))
        ttk.Button(btn_frame, text="Export JSON", command=self.ExportJson).pack(side="right", ipadx=12, ipady=4)
        ttk.Button(btn_frame, text="Preview JSON", command=self.PreviewJson).pack(side="right", ipadx=12, ipady=4, padx=(0, 6))

        self.OnTypeChange()

    def TabBasics(self, nb):
        f = MakeScrollableTab(nb, "Basics")
        r = 0

        MakeLabel(f, r, "Character name:")
        self.name_entry = ttk.Entry(f, width=24)
        self.name_entry.grid(row=r, column=1, sticky="w", pady=4)
        r += 1

        _, self.type_combo = CreateCombobox(f, r, "Type:", ["Sorcerer", "Cursed Spirit", "Physically Gifted"], "Sorcerer")
        self.type_combo.bind("<<ComboboxSelected>>", self.OnTypeChange)
        r += 1

        _, self.ai_combo = CreateCombobox(f, r, "AI brain:", ai_types, "Aggressive")
        r += 1
        _, self.color_combo = CreateCombobox(f, r, "Name color:", [color.name for color in ColorMap], "Cyan")
        r += 1

        self.six_eyes_var = tk.BooleanVar()
        self.six_eyes_cb = ttk.Checkbutton(f, text="Possesses Six Eyes (Sorcerer only)", variable=self.six_eyes_var)
        self.six_eyes_cb.grid(row=r, column=0, columnspan=2, sticky="w", pady=4)
        r += 1

        ttk.Separator(f, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", pady=8)
        r += 1

        _, self.hp_spin = CreateSpinbox(f, r, "Max HP:", 600.0, 1)
        r += 1
        _, self.dmg_spin = CreateSpinbox(f, r, "Base attack DMG:", 45.0, 1, 9999)
        r += 1

    def TabCombat(self, nb):
        f = MakeScrollableTab(nb, "Combat")
        r = 0

        self.lbl_ce, self.ce_spin = CreateSpinbox(f, r, "Max cursed energy:", 3000.0)
        r += 1
        self.lbl_regen, self.regen_spin = CreateSpinbox(f, r, "CE regeneration per turn:", 50.0)
        r += 1
        self.lbl_pregen, self.passive_regen_spin = CreateSpinbox(f, r, "Passive HP regen (Cursed Spirit):", 20.0, 0, 9999)
        r += 1
        self.lbl_bf, self.bf_spin = CreateSpinbox(f, r, "Black Flash chance:", 15, 0, 100)
        r += 1
        self.lbl_bfm, self.bf_mult_spin = CreateSpinbox(f, r, "Black Flash damage multiplier:", 4.5, 1, 50)
        r += 1

        ttk.Separator(f, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", pady=8)
        r += 1

        self.lbl_rct, self.rct_combo = CreateCombobox(f, r, "RCT proficiency:", rct_levels, "None")
        r += 1

        ttk.Separator(f, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", pady=8)
        r += 1

        self.lbl_str, self.strength_spin = CreateSpinbox(f, r, "Strength (Physically Gifted):", 500, 1, 9999)
        r += 1

    def TabTechniques(self, nb):
        f = MakeScrollableTab(nb, "Techniques")
        r = 0

        self.lbl_tech, self.tech_combo = CreateCombobox(f, r, "Cursed technique:", techniques, "None")
        r += 1
        self.lbl_domain, self.domain_combo = CreateCombobox(f, r, "Domain expansion:", domains, "None")
        r += 1
        self.lbl_counter, self.counter_combo = CreateCombobox(f, r, "Counter domain:", counter_domains, "None")
        r += 1
        self.lbl_special, self.special_combo = CreateCombobox(f, r, "Special move:", specials, "None")
        r += 1

        ttk.Separator(f, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", pady=8)
        r += 1

        self.lbl_shiki = MakeLabel(f, r, "Shikigami (select multiple):")
        self.shiki_select = MultiSelect(f, shikigami_list, height=3)
        self.shiki_select.grid(row=r, column=1, sticky="w", pady=4)
        r += 1

    def TabTools(self, nb):
        f = MakeScrollableTab(nb, "Tools")
        r = 0

        _, self.equipped_combo = CreateCombobox(f, r, "Equipped tool:", ["None"] + tools_list, "None", width=26)
        r += 1

        ttk.Separator(f, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", pady=8)
        r += 1

        MakeLabel(f, r, "Inventory items\n(select multiple):")
        self.inv_select = MultiSelect(f, tools_list, height=4)
        self.inv_select.grid(row=r, column=1, sticky="w", pady=4)
        r += 1

    def TabAdvanced(self, nb):
        f = MakeScrollableTab(nb, "Advanced")
        r = 0

        self.lbl_reinf, self.max_reinf_spin = CreateSpinbox(f, r, "Max reinforcement:", 200, 0)
        r += 1
        self.lbl_rcost, self.reinf_cost_spin = CreateSpinbox(f, r, "Reinforcement cost multiplier:", 2, 0, 100)
        r += 1
        self.lbl_dlim, self.domain_lim_spin = CreateSpinbox(f, r, "Domain use limit:", 5, 1, 999)
        r += 1
        self.lbl_dtime, self.max_domain_spin = CreateSpinbox(f, r, "Max turn time on active domains:", 5, 1, 999)
        r += 1
        self.lbl_ztime, self.max_zone_spin = CreateSpinbox(f, r, "Max turn time in the Zone:", 3, 1, 999)
        r += 1
        self.lbl_btime, self.burnout_spin = CreateSpinbox(f, r, "Max turn amount in CT Burnout:", 4, 1, 999)
        r += 1

    def OnTypeChange(self, _event=None):
        t = self.type_combo.get()
        is_curse_user = t in ("Sorcerer", "Cursed Spirit")
        is_sorcerer = t == "Sorcerer"
        is_spirit = t == "Cursed Spirit"
        is_phys_gifted = t == "Physically Gifted"

        self.six_eyes_cb.config(state="normal" if is_sorcerer else "disabled")

        SetGroup(is_curse_user,
            (self.lbl_ce, self.ce_spin),
            (self.lbl_regen, self.regen_spin),
            (self.lbl_bf, self.bf_spin),
            (self.lbl_bfm, self.bf_mult_spin),
        )
        SetGroup(is_spirit, (self.lbl_pregen, self.passive_regen_spin))
        SetGroup(is_phys_gifted, (self.lbl_str, self.strength_spin))
        SetComboGroup(is_sorcerer, (self.lbl_rct, self.rct_combo))

        SetComboGroup(is_curse_user,
            (self.lbl_tech, self.tech_combo),
            (self.lbl_domain, self.domain_combo),
            (self.lbl_counter, self.counter_combo),
            (self.lbl_special, self.special_combo),
        )

        self.lbl_shiki.config(fg=label_normal if is_curse_user else label_dim)
        self.shiki_select.listbox.config(state="normal" if is_curse_user else "disabled")

        SetGroup(is_curse_user,
            (self.lbl_reinf, self.max_reinf_spin),
            (self.lbl_rcost, self.reinf_cost_spin),
            (self.lbl_dlim, self.domain_lim_spin),
            (self.lbl_dtime, self.max_domain_spin),
            (self.lbl_ztime, self.max_zone_spin),
            (self.lbl_btime, self.burnout_spin),
        )

    def BuildCharacter(self):
        char_type = self.type_combo.get()
        color_name = self.color_combo.get()
        color_code = ColorMap[color_name].value if color_name in ColorMap.__members__ else "\033[36m"

        data = {
            "type": char_type,
            "identity": {
                "name": self.name_entry.get().strip() or "Unnamed Sorcerer",
                "color": color_code
            },
            "stats": {
                "hp": float(self.hp_spin.get())
            },
            "config": {
                "ai_type": self.ai_combo.get(),
                "attack_damage": float(self.dmg_spin.get())
            }
        }

        if char_type == "Physically Gifted":
            data["stats"]["strength"] = float(self.strength_spin.get())
        else:
            data["stats"]["ce"] = float(self.ce_spin.get())
            data["stats"]["regen"] = float(self.regen_spin.get())

            data["sorcery"] = {
                "kit": {},
                "tuning": {
                    "blackflash_chance": int(self.bf_spin.get()),
                    "blackflash_multiplier": float(self.bf_mult_spin.get()),
                    "max_reinforcement": float(self.max_reinf_spin.get()),
                    "max_domain_time": int(self.max_domain_spin.get()),
                    "domain_limit": int(self.domain_lim_spin.get()),
                    "max_zone_time": int(self.max_zone_spin.get()),
                    "max_burnout_time": int(self.burnout_spin.get())
                }
            }

            if char_type == "Sorcerer":
                rct = self.rct_combo.get()
                if rct != "None":
                    data["config"]["can_use_rct"] = True
                    data["config"]["rct_proficiency"] = rct
                data["config"]["six_eyes"] = self.six_eyes_var.get()

            if char_type == "Cursed Spirit":
                data["config"]["passive_health_regen"] = float(self.passive_regen_spin.get())

            tech = self.tech_combo.get()
            if tech != "None": data["sorcery"]["kit"]["technique"] = tech

            domain = self.domain_combo.get()
            if domain != "None": data["sorcery"]["kit"]["domain"] = domain

            counter = self.counter_combo.get()
            if counter != "None": data["sorcery"]["kit"]["counter_domain"] = counter

            special = self.special_combo.get()
            if special != "None": data["sorcery"]["kit"]["special"] = special

            shiki = self.shiki_select.GetSelected()
            if shiki: data["sorcery"]["kit"]["shikigami"] = shiki

        equipped = self.equipped_combo.get()
        inv = self.inv_select.GetSelected()

        if equipped != "None" or inv:
            data["tools"] = {}
            if equipped != "None":
                data["tools"]["equipped_tool"] = equipped
            if inv:
                data["tools"]["inventory"] = inv

        return data

    def ExportJson(self):
        char = self.BuildCharacter()
        schema = {"characters": [char]}
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="characters.json",
        )
        if path:
            with open(path, "w") as fh:
                json.dump(schema, fh, indent=2)
            messagebox.showinfo("Saved", f"Character exported to:\n{path}")

    def PreviewJson(self):
        char = self.BuildCharacter()
        schema = {"characters": [char]}
        text = json.dumps(schema, indent=2)

        win = tk.Toplevel(self.root)
        win.title("JSON preview")
        win.geometry("480x500")
        win.resizable(True, True)

        frame = ttk.Frame(win, padding=8)
        frame.pack(fill="both", expand=True)

        sb = ttk.Scrollbar(frame)
        sb.pack(side="right", fill="y")

        txt = tk.Text(frame, wrap="none", yscrollcommand=sb.set, font=("Courier", 10))
        txt.pack(fill="both", expand=True)
        sb.config(command=txt.yview)
        txt.insert("1.0", text)
        txt.config(state="disabled")
        sb.config(command=txt.yview)

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 8))

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterCreatorApp(root)
    root.mainloop()