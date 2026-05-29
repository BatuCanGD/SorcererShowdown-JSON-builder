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

class ToolBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cursed Tool Builder")
        f = ttk.Frame(root, padding=15)
        f.pack(fill="both", expand=True)

        ttk.Label(f, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar(value="Playful Cloud")
        ttk.Entry(f, textvariable=self.name_var).grid(row=0, column=1, pady=4)

        ttk.Label(f, text="Color:").grid(row=1, column=0, sticky="w")
        self.color_cb = ttk.Combobox(f, values=[c.name for c in ColorMap], state="readonly")
        self.color_cb.set("Red")
        self.color_cb.grid(row=1, column=1, pady=4)

        ttk.Label(f, text="Type:").grid(row=2, column=0, sticky="w")
        self.type_cb = ttk.Combobox(f, values=["Normal", "Bypass Techniques", "Bypass Reinforcement", "Bypass Everything"], state="readonly")
        self.type_cb.set("Normal")
        self.type_cb.grid(row=2, column=1, pady=4)

        ttk.Label(f, text="Damage:").grid(row=3, column=0, sticky="w")
        self.dmg_spin = ttk.Spinbox(f, from_=0, to=9999, increment=1)
        self.dmg_spin.set(150.0)
        self.dmg_spin.grid(row=3, column=1, pady=4)

        ttk.Button(f, text="Export JSON", command=self.export).grid(row=4, columnspan=2, pady=12)

    def export(self):
        data = {
            "name": self.name_var.get(),
            "color": ColorMap[self.color_cb.get()].value,
            "type": self.type_cb.get(),
            "damage": float(self.dmg_spin.get() or 0)
        }
        path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="cursedtools.json")
        if path:
            with open(path, "w") as fh:
                json.dump({"cursedtools": [data]}, fh, indent=2)
            messagebox.showinfo("Saved", "Tool exported successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    ToolBuilderApp(root)
    root.mainloop()