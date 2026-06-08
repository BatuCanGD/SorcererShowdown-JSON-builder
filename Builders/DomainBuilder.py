import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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


class DomainBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Domain Builder")
        f = ttk.Frame(root, padding=15)
        f.pack(fill="both", expand=True)

        self.vars = {}
        row = 0

        def add_entry(key, label, default):
            nonlocal row
            ttk.Label(f, text=label).grid(row=row, column=0, sticky="w")
            var = tk.StringVar(value=default)
            ttk.Entry(f, textvariable=var).grid(row=row, column=1, pady=4)
            self.vars[key] = var
            row += 1

        def add_combo(key, label, values, default):
            nonlocal row
            ttk.Label(f, text=label).grid(row=row, column=0, sticky="w")
            cb = ttk.Combobox(f, values=values, state="readonly")
            cb.set(default)
            cb.grid(row=row, column=1, pady=4)
            self.vars[key] = cb
            row += 1

        def add_spin(key, label, default):
            nonlocal row
            ttk.Label(f, text=label).grid(row=row, column=0, sticky="w")
            spin = ttk.Spinbox(f, from_=0, to=99999, increment=1)
            spin.set(default)
            self.vars[key] = spin
            spin.grid(row=row, column=1, pady=4)
            row += 1

        def add_check(key, label):
            nonlocal row
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(f, text=label, variable=var).grid(row=row, columnspan=2, sticky="w", pady=4)
            self.vars[key] = var
            row += 1

        add_entry("name", "Name:", "Custom Domain")

        ttk.Label(f, text="Color:").grid(row=row, column=0, sticky="w")
        self.color_cb = ttk.Combobox(f, values=[c.name for c in ColorMap], state="readonly")
        self.color_cb.set("Red")
        self.color_cb.grid(row=row, column=1, pady=4)
        row += 1

        add_combo("domain_type", "Domain Type:", ["Hits Curse User", "Hits Everyone", "Hits Soul"], "Hits Curse User")
        add_combo("refinement", "Refinement:", ["Unstable", "Crude", "Refined", "Absolute"], "Refined")
        add_check("is_neutralizer", "Is Neutralizer (Simple Domain/HWB)")
        add_spin("health", "Health:", 500.0)
        add_spin("strength", "Strength:", 100.0)
        add_spin("range", "Range:", 15)
        add_spin("cost", "Cost (CE):", 1500.0)
        add_check("can_stun", "Can Stun")
        add_spin("surehit_damage", "Sure-hit Damage:", 100.0)

        ttk.Button(f, text="Export JSON", command=self.export).grid(row=row, columnspan=2, pady=12)

    def export(self):
        is_neutralizer = self.vars["is_neutralizer"].get()

        data = {
            "identity": {
                "name": self.vars["name"].get(),
                "color": ColorMap[self.color_cb.get()].value
            },
            "config": {
                "domain_type": self.vars["domain_type"].get(),
                "refinement": self.vars["refinement"].get(),
                "is_neutralizer": is_neutralizer,
                "cost": float(self.vars["cost"].get()),
                "can_stun": self.vars["can_stun"].get(),
                "surehit_damage": float(self.vars["surehit_damage"].get())
            }
        }

        if not is_neutralizer:
            data["stats"] = {
                "health": float(self.vars["health"].get()),
                "strength": float(self.vars["strength"].get()),
                "range": int(self.vars["range"].get())
            }

        path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="domains.json")
        if path:
            with open(path, "w") as fh:
                json.dump({"domains": [data]}, fh, indent=2)
            messagebox.showinfo("Saved", "Domain exported successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    DomainBuilderApp(root)
    root.mainloop()
