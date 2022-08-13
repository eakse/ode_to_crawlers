# -*- coding: utf-8 -*-

import tkinter as tk
from ode.constants import *


class MenuBarCharacterEditor(tk.Menu):
    def __init__(self, parent):
        super(MenuBarCharacterEditor, self).__init__(parent)
        filemenu = tk.Menu(self)
        # filemenu.add_command(label="Open Map", command=parent.load_blosc)
        # filemenu.add_command(label="Save Map", command=parent.save_blosc)
        filemenu.add_separator()
        # filemenu.add_command(label="Open JSON", command=parent.load_json)
        # filemenu.add_command(label="Save JSON", command=parent.save_json)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_program)
        self.add_cascade(label="File", menu=filemenu)

    def exit_program(self):
        exit()


class CharacterDetails(tk.Frame):
    def __init__(self, parent, character) -> None:
        super(CharacterDetails, self).__init__(parent)
        


class CharacterEditor(tk.Frame):
    def __init__(self, parent):
        super(CharacterEditor, self).__init__(parent)
        self.menubar = MenuBarCharacterEditor(self)
        parent.config(menu=self.menubar)






if __name__ == "__main__":
    root = tk.Tk(className="oDE Character Editor")
    root.option_add("*tearOff", False)
    root.config(bg="white")
    main = CharacterEditor(root)

    main.pack(
        fill="both", expand=True, pady=main.canvas_padding, padx=main.canvas_padding
    )

    root.mainloop()
