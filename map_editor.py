# -*- coding: utf-8 -*-
"""Map editor

Please note that this file is a bit of a mess. It's not intended for 
readability, modularity or any such fancy concepts.
(Sarcasm very much intended)

This is just a tool to help me build the game, so it's built under
Murphy's law:  
If it's stupid but it works, it isn't stupid.

Please note that the class MapEditor is extremely messy ☹
On the positive side, code formatting is OK.
"""


import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from ode.map import Map, MapTile, Room, list_next
from ode.constants import *
from ode.util import timer
from pprint import pprint
import gc
import json


class MenuBar(tk.Menu):
    def __init__(self, parent):
        super(MenuBar, self).__init__(parent)
        filemenu = tk.Menu(self)
        filemenu.add_command(label="Open Map", command=parent.load_blosc)
        filemenu.add_command(label="Save Map", command=parent.save_blosc)
        filemenu.add_separator()
        filemenu.add_command(label="Open JSON", command=parent.load_json)
        filemenu.add_command(label="Save JSON", command=parent.save_json)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_program)
        self.add_cascade(label="File", menu=filemenu)

    def exit_program(self):
        exit()


class MapEditor(tk.Frame):
    def __init__(self, parent):
        super(MapEditor, self).__init__(parent)
        self.menubar = MenuBar(self)
        parent.config(menu=self.menubar)
        self.map_width = 20
        self.map_height = 20
        self.canvas_padding = 5
        self.x = 0
        self.y = 0
        self.copy = MapTile()
        self.copy_changed = True
        self.hover_color = "red"
        self.hover_boundary = 2
        self.hover_delay = 50
        self.hover_delay_room = 500
        self.hover_delay_waiting = False
        self.fix_edges = True
        self.hover_room = Room
        self.line_settings = {"fill": "yellow"}  # , "dash": (2, 2)
        self.room_text_dict = {"font": ("Consolas 6"), "fill": "yellow", "anchor": "nw"}
        self.rooms = []
        self.gc_counter = 0

        self.text_dict = {"font": ("Consolas 8"), "fill": "black", "anchor": "nw"}
        self.label_dict = {"font": ("Consolas 8"), "anchor": "nw", "bg": "white"}
        self.key_list = [
            {"w": "Cycle North"},
            {"a": "Cycle West"},
            {"s": "Cycle South"},
            {"d": "Cycle East"},
            {"f": "Cycle floor"},
            {"c": "Copy"},
            {"v": "Paste"},
            {"x": "Clear tile"},
            {"n": "Clear map"},
            {"h": "Randomize map"},
            {"z": "Adjust surrounding"},
        ]
        self.key_list_x = self.canvas_padding * 2
        self.key_list_y = (
            (self.map_height * TILESIZE)
            - ((1 + len(self.key_list)) * 10)
            - self.canvas_padding
        )

        self.auto_adjust = tk.BooleanVar()
        self.auto_adjust_cb = tk.Checkbutton(
            parent,
            text="Autoadjust surrounding",
            **self.label_dict,
            variable=self.auto_adjust,
            onvalue=True,
            offvalue=False,
        )
        self.auto_adjust_cb.select()
        self.auto_adjust_cb.place(
            x=((self.map_width * TILESIZE) + (self.canvas_padding * 2)),
            y=self.key_list_y - 20,
        )

        self.draw_room_bool = tk.BooleanVar()
        self.draw_room_cb = tk.Checkbutton(
            parent,
            text="Draw room outline",
            **self.label_dict,
            variable=self.draw_room_bool,
            onvalue=True,
            offvalue=False,
        )
        self.draw_room_cb.place(
            x=((self.map_width * TILESIZE) + (self.canvas_padding * 2)),
            y=self.key_list_y - 40,
        )

        self.canvas = tk.Canvas(
            self,
            width=self.map_width * TILESIZE,
            height=self.map_height * TILESIZE,
            highlightthickness=0,
            background="grey",
        )
        self.canvas.grid(row=0, column=0)
        # self.canvas.pack(padx=self.canvas_padding,pady=self.canvas_padding)

        self.infoblock = tk.Canvas(
            self,
            width=200,
            height=self.map_height * TILESIZE,
            highlightthickness=0,
            background="white",
        )
        self.label_copied = tk.Label(
            self.infoblock, text="Copied tile:", **self.label_dict
        )
        self.label_copied.place(x=0, y=0)
        self.label_hover = tk.Label(
            self.infoblock, text="Hovered tile:", **self.label_dict
        )
        self.label_hover.place(x=0, y=70)
        self.label_hover_details_text = tk.StringVar()
        self.label_hover_details = tk.Label(
            self.infoblock,
            textvariable=self.label_hover_details_text,
            **self.label_dict,
        )
        self.label_hover_details.place(x=0, y=140)

        self.infoblock.create_rectangle(
            0,
            0,
            self.canvas_padding,
            self.map_height * TILESIZE,
            outline=parent["bg"],
            fill=parent["bg"],
        )
        self.infoblock.grid(row=0, column=1)
        # self.infoblock.pack(padx=self.canvas_padding,pady=self.canvas_padding)

        # BINDINGS
        self.canvas.bind("<Button-1>", self.canvas_click_event)
        self.canvas.bind("<Button-2>", self.canvas_click_middle_event)
        self.canvas.bind("<Button-3>", self.canvas_click_right_event)
        self.canvas.bind_all("<w>", self.cycle_north)
        self.canvas.bind_all("<a>", self.cycle_west)
        self.canvas.bind_all("<s>", self.cycle_south)
        self.canvas.bind_all("<d>", self.cycle_east)
        self.canvas.bind_all("<W>", self.sepa_inv_north)
        self.canvas.bind_all("<A>", self.sepa_inv_west)
        self.canvas.bind_all("<S>", self.sepa_inv_south)
        self.canvas.bind_all("<D>", self.sepa_inv_east)
        self.canvas.bind_all("<f>", self.cycle_floor)
        self.canvas.bind_all("<c>", self.copy_tile)
        self.canvas.bind_all("<v>", self.paste_tile)
        self.canvas.bind_all("<x>", self.clear_tile)
        self.canvas.bind_all("<n>", self.clear_map)
        self.canvas.bind_all("<z>", self.fix_surrounding)
        self.canvas.bind_all("<h>", self.randomize)
        self.canvas.bind("<Motion>", self.canvas_motion_event)

        self.map = Map(self.map_width, self.map_height, dev_mode=True)
        # self.map.randomize()
        self.map = Map.load_blosc("C:/###VS Projects/ode_to_crawlers/data/maps/1.map")
        self.init_map()
        self.update()
        self.draw_keybindings()

    def xy_from_event(self, event):
        return event.x // TILESIZE, event.y // TILESIZE

    def save_blosc(self):
        filetypes = (("Map files", "*.map"),)
        filename = fd.asksaveasfilename(
            title="Save map", filetypes=filetypes, defaultextension=".map"
        )  # , initialdir="/"
        if filename:
            if filename.endswith(".map"):
                self.map.save_blosc(filename)
            else:
                mb.showerror(title="Error", message="Only .map files are allowed...")
        else:
            print("No file selected")

    def save_json(self):
        filetypes = (("JSON files", "*.json"),)
        filename = fd.asksaveasfilename(
            title="Save JSON", filetypes=filetypes, defaultextension=".json"
        )  # , initialdir="/"
        if filename:
            if filename.endswith(".json"):
                with open(filename, "w") as outfile:
                    outfile.write(self.map.dumps())
            else:
                mb.showerror(title="Error", message="Only .json files are allowed...")
        else:
            print("No file selected")

    def load_blosc(self):
        filetypes = (("Map files", "*.map"),)
        filename = fd.askopenfilename(
            title="Open map", filetypes=filetypes, defaultextension=".map"
        )
        if filename:
            if filename.endswith(".map"):
                self.map = Map.load_blosc(filename)
                self.update()
            else:
                mb.showerror(title="Error", message="Only .map files are allowed...")
        else:
            print("No file selected")

    def load_json(self):
        filetypes = (("Map files", "*.json"),)
        filename = fd.askopenfilename(
            title="Open JSON", filetypes=filetypes, defaultextension=".json"
        )
        if filename:
            if filename.endswith(".json"):
                with open(filename) as infile:
                    self.map = Map.from_json(**json.load(infile))
                self.update()
            else:
                mb.showerror(title="Error", message="Only .json files are allowed...")
        else:
            print("No file selected")

    def randomize(self, _):
        self.map.randomize()
        self.update(adjust=False)

    def canvas_click_event(self, _):
        self.map.tiles[self.x][self.y] = MapTile.random(dev_mode=True)
        self.update()

    def canvas_click_middle_event(self, _):
        pass

    def canvas_click_right_event(self, _):
        # self.rooms = self.map.get_rooms_all()
        if self.hover_room not in self.rooms:
            self.rooms.append(self.hover_room)
            self.update()

    def canvas_motion_event(self, event):
        """Sets the coordinates for drawing the hover indicator.
        These coordinates are also used for the other event functions dealing with the map.
        There was a mismatch between the hover and the tile where the action was executed on.
        Delay added to increase responsiveness.
        """
        self.x, self.y = self.xy_from_event(event)
        if self.hover_delay_waiting:
            return
        self.after(self.hover_delay, self.execute_hover)
        self.hover_delay_waiting = True

    def execute_hover(self):
        self.hover_delay_waiting = False
        self.update(adjust=False)

    def clear_map(self, _):
        """Clear map"""
        self.map.clear()
        self.update(adjust=False)

    def fix_surrounding(self, _):
        """Makes the surrounding tiles' edges match the current tile"""
        self.map.adjust_surrounding(self.x, self.y)
        self.update(adjust=False)

    def copy_tile(self, _):
        """Copy current tile"""
        self.copy = MapTile(dev_mode=True, **self.map.tiles[self.x][self.y].dump)
        self.copy_changed = True
        self.update(adjust=False)

    def paste_tile(self, _):
        """Paste previously copied tile. (defaults to ode.ode_constants.EMPTY_TILE)"""
        self.map.tiles[self.x][self.y] = MapTile(dev_mode=True, **self.copy.dump)
        self.update()

    def clear_tile(self, _):
        """Paste ode.ode_constants.EMPTY_TILE (in other words, delete)"""
        self.map.tiles[self.x][self.y] = MapTile(dev_mode=True)
        self.update()

    def cycle_north(self, _):
        """Cycle north edge"""
        self.map.tiles[self.x][self.y].n.style = list_next(
            self.map.tiles[self.x][self.y].n.style, EDGE_LIST_SIMPLE
        )
        self.update()

    def cycle_west(self, _):
        """Cycle west edge"""
        self.map.tiles[self.x][self.y].w.style = list_next(
            self.map.tiles[self.x][self.y].w.style, EDGE_LIST_SIMPLE
        )
        self.update()

    def cycle_south(self, _):
        """Cycle south edge"""
        self.map.tiles[self.x][self.y].s.style = list_next(
            self.map.tiles[self.x][self.y].s.style, EDGE_LIST_SIMPLE
        )
        self.update()

    def cycle_east(self, _):
        """Cycle east edge"""
        self.map.tiles[self.x][self.y].e.style = list_next(
            self.map.tiles[self.x][self.y].e.style, EDGE_LIST_SIMPLE
        )
        self.update()

    def sepa_inv_north(self, _):
        self.map.tiles[self.x][self.y].n.style = SEPA_INV
        self.update()

    def sepa_inv_west(self, _):
        self.map.tiles[self.x][self.y].w.style = SEPA_INV
        self.update()

    def sepa_inv_south(self, _):
        self.map.tiles[self.x][self.y].s.style = SEPA_INV
        self.update()

    def sepa_inv_east(self, _):
        self.map.tiles[self.x][self.y].e.style = SEPA_INV
        self.update()

    def cycle_floor(self, _):
        """Cycle floor"""
        self.map.tiles[self.x][self.y].f.style = list_next(
            self.map.tiles[self.x][self.y].f.style, FLOOR_LIST_SIMPLE
        )
        self.update()

    def init_map(self):
        self.imggrid_tk = [
            [None for _ in range(self.map_width)] for _ in range(self.map_height)
        ]

    def draw_keybindings(self):
        self.infoblock.create_text(
            self.key_list_x, self.key_list_y, text="Keybindings:", **self.text_dict
        )
        for index, item in enumerate(self.key_list):
            key, value = next(iter(item.items()))
            self.infoblock.create_text(
                self.key_list_x + 4,
                self.key_list_y + (index + 1) * 10,
                text=f"{key}: {value}",
                **self.text_dict,
            )

    def draw_tile(self, x, y):
        self.imggrid_tk[x][y] = ImageTk.PhotoImage(self.map.tiles[x][y].image)
        self.canvas.create_image(
            x * TILESIZE,
            y * TILESIZE,
            image=self.imggrid_tk[x][y],
            anchor="nw",
        )

    # @timer
    def draw_room_outline(self, room: Room, text=""):
        # self.gc_counter += 1
        # if self.gc_counter == 100:
        #     print("collect")
        #     self.gc_counter = 0
        #     gc.collect(2)
        if not self.draw_room_bool.get():
            return
        # room = self.map.get_room((self.x, self.y), [])

        for coord in room.coords:
            x, y = coord
            if self.map.tiles[x][y]._n != "none":
                self.canvas.create_line(
                    x * TILESIZE - 2,
                    y * TILESIZE - 2,
                    (x + 1) * TILESIZE + 2,
                    y * TILESIZE - 2,
                    **self.line_settings,
                )
            if self.map.tiles[x][y]._s != "none":
                self.canvas.create_line(
                    x * TILESIZE - 2,
                    (y + 1) * TILESIZE + 2,
                    (x + 1) * TILESIZE + 2,
                    (y + 1) * TILESIZE + 2,
                    **self.line_settings,
                )
            if self.map.tiles[x][y]._e != "none":
                self.canvas.create_line(
                    (x + 1) * TILESIZE + 2,
                    y * TILESIZE - 2,
                    (x + 1) * TILESIZE + 2,
                    (y + 1) * TILESIZE + 2,
                    **self.line_settings,
                )
            if self.map.tiles[x][y]._w != "none":
                self.canvas.create_line(
                    x * TILESIZE - 2,
                    y * TILESIZE - 2,
                    x * TILESIZE - 2,
                    (y + 1) * TILESIZE + 2,
                    **self.line_settings,
                )
        for coord in room.coords:
            self.draw_tile(*coord)
        self.label_room(room, text)

    def label_room(self, room: Room, text=""):
        text = f"{text}\n{room.size}"
        x, y = room.first
        x = x * TILESIZE +2
        y = y * TILESIZE +2
        # print(x,y)
        self.canvas.create_text(x, y, **self.room_text_dict, text=text)

    def update(self, adjust=True):
        # self.label_hover_details_text.set(self.map.tiles[self.x][self.y].pretty_text)
        if self.fix_edges:
            self.map.fix_edges()
        if adjust and self.auto_adjust.get():
            self.map.adjust_surrounding(self.x, self.y)
        for w in range(self.map.width):
            for h in range(self.map.height):
                self.draw_tile(w, h)
        if self.copy_changed:
            if hasattr(self, "info_copied"):
                del self.info_copied
            self.info_copied = ImageTk.PhotoImage(
                self.copy.image.resize(
                    (TILESIZE * 2, TILESIZE * 2), Image.BILINEAR
                )
            )
            self.copy_changed = False
        del self.hover_room
        self.hover_room = Room(coords=self.map.get_room((self.x, self.y), []))
        self.draw_room_outline(self.hover_room)
        
        x0 = (self.x * TILESIZE) - self.hover_boundary - 1
        y0 = (self.y * TILESIZE) - self.hover_boundary - 1
        x1 = (self.x * TILESIZE) + TILESIZE + self.hover_boundary + 1
        y1 = (self.y * TILESIZE) + TILESIZE + self.hover_boundary + 1
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=self.hover_color)
        self.hover_delay = 0
        self.hover_delay_waiting = False

        for room in self.rooms:
            self.label_room(room, "___")

        self.infoblock.create_image(20, 20, image=self.info_copied, anchor="nw")
        self.info_hover = ImageTk.PhotoImage(
            self.map.tiles[self.x][self.y].image.resize(
                (TILESIZE * 2, TILESIZE * 2), Image.BILINEAR
            )
        )
        self.infoblock.create_image(20, 90, image=self.info_hover, anchor="nw")


if __name__ == "__main__":
    root = tk.Tk(className=" ODE Map Editor")
    root.option_add("*tearOff", False)
    root.config(bg="white")
    main = MapEditor(root)

    main.pack(
        fill="both", expand=True, pady=main.canvas_padding, padx=main.canvas_padding
    )

    root.mainloop()
