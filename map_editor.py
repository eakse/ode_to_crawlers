import tkinter as tk
from PIL import Image, ImageTk
from ode.map import Map, TileFloor, MapTile, TileEdge
from ode.ode_constants import *
import os


print(os.getcwd())


class MapEditor(tk.Frame):
    def __init__(self, parent):
        super(MapEditor, self).__init__(parent)
        self.copy = EMPTY_TILE
        self.map_width = 20
        self.map_height = 20
        self.canvas_padding = 5
        self.tilesize = TILESIZE
        self.hover_x = 0
        self.hover_y = 0
        self.hover_color = "red"
        self.hover_boundary = 2
        self.hover_delay = 0
        self.hover_delay_max = 5
        self.fix_edges = True

        self.canvas = tk.Canvas(
            self,
            width=self.map_width * self.tilesize,
            height=self.map_height * self.tilesize,
            highlightthickness=0,
            background="grey",
        )
        self.canvas.grid(row=0, column=0)
        # self.canvas.pack(padx=self.canvas_padding,pady=self.canvas_padding)

        self.infoblock = tk.Canvas(
            self,
            width=100,
            height=self.map_height * self.tilesize,
            highlightthickness=0,
            background="white",
        )
        self.infoblock.create_rectangle(
            0,
            0,
            self.canvas_padding,
            self.map_height * self.tilesize,
            outline=parent["bg"],
            fill=parent["bg"],
        )
        self.infoblock.grid(row=0, column=1)
        # self.infoblock.pack(padx=self.canvas_padding,pady=self.canvas_padding)

        # BINDINGS
        self.canvas.bind("<Button-1>", self.canvas_click_event)
        self.canvas.bind_all("<w>", self.canvas_w_event)
        self.canvas.bind_all("<a>", self.canvas_a_event)
        self.canvas.bind_all("<s>", self.canvas_s_event)
        self.canvas.bind_all("<d>", self.canvas_d_event)
        self.canvas.bind_all("<f>", self.canvas_f_event)
        self.canvas.bind_all("<c>", self.canvas_c_event)
        self.canvas.bind_all("<v>", self.canvas_v_event)
        self.canvas.bind_all("<x>", self.canvas_x_event)
        self.canvas.bind("<Motion>", self.canvas_motion_event)

        self.map = Map(self.map_width, self.map_height)
        self.map.randomize()
        self.init_map()
        self.update()

    def xy_from_event(self, event):
        return event.x // self.tilesize, event.y // self.tilesize

    def canvas_click_event(self, event):
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y] = MapTile(self.map.randomtile)
        self.update()

    def canvas_motion_event(self, event):
        """Sets the coordinates for drawing the hover indicator.
        Delay added to increase responsiveness.
        """
        self.hover_x, self.hover_y = self.xy_from_event(event)
        self.hover_delay += 1
        if self.hover_delay == self.hover_delay_max:
            self.update()

    def canvas_c_event(self, event):
        """Copy current tile"""
        x, y = self.xy_from_event(event)
        self.copy = self.map.tiles[x][y].to_json
        self.update()

    def canvas_v_event(self, event):
        """Paste previously copied tile. (defaults to ode.ode_constants.EMPTY_TILE)"""
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y] = MapTile(self.copy)
        self.update()

    def canvas_x_event(self, event):
        """Paste ode.ode_constants.EMPTY_TILE (in other words, delete)"""
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y] = MapTile(EMPTY_TILE)
        self.update()

    def canvas_w_event(self, event):
        """Cycle north edge"""
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y].n = TileEdge(
            start_type=self.map.tiles[x][y].n).next
        self.update()

    def canvas_a_event(self, event):
        """Cycle west edge"""
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y].w = TileEdge(
            start_type=self.map.tiles[x][y].w).next
        self.update()

    def canvas_s_event(self, event):
        """Cycle south edge"""
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y].s = TileEdge(
            start_type=self.map.tiles[x][y].s).next
        self.update()

    def canvas_d_event(self, event):
        """Cycle east edge"""
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y].e = TileEdge(
            start_type=self.map.tiles[x][y].e).next
        self.update()

    def canvas_f_event(self, event):
        """Cycle floor"""
        x, y = self.xy_from_event(event)
        self.map.tiles[x][y].f = TileFloor(
            start_type=self.map.tiles[x][y].f).next
        self.update()

    def init_map(self):
        self.imggrid_tk = [
            [None for _ in range(self.map_width)] for _ in range(self.map_height)
        ]

    def update(self):
        if self.fix_edges:
            self.map.fix_edges()
        for w in range(self.map.width):
            for h in range(self.map.height):
                self.imggrid_tk[w][h] = ImageTk.PhotoImage(
                    self.map.tiles[w][h].tile_img
                )
                self.canvas.create_image(
                    w * self.tilesize,
                    h * self.tilesize,
                    image=self.imggrid_tk[w][h],
                    anchor="nw",
                )
        x0 = (self.hover_x * self.tilesize) - self.hover_boundary - 1
        y0 = (self.hover_y * self.tilesize) - self.hover_boundary - 1
        x1 = (self.hover_x * self.tilesize) + \
            self.tilesize + self.hover_boundary
        y1 = (self.hover_y * self.tilesize) + \
            self.tilesize + self.hover_boundary
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=self.hover_color)
        self.hover_delay = 0

        self.info_copied = ImageTk.PhotoImage(
            MapTile(self.copy).tile_img.resize(
                (self.tilesize * 2, self.tilesize * 2), Image.BILINEAR
            )
        )
        self.infoblock.create_image(
            20, 20, image=self.info_copied, anchor="nw")
        self.info_hover = ImageTk.PhotoImage(
            self.map.tiles[self.hover_x][self.hover_y].tile_img.resize(
                (self.tilesize * 2, self.tilesize * 2), Image.BILINEAR
            )
        )
        self.infoblock.create_image(20, 80, image=self.info_hover, anchor="nw")


if __name__ == "__main__":
    root = tk.Tk(className=" ODE Map Editor")
    main = MapEditor(root)
    main.pack(
        fill="both", expand=True, pady=main.canvas_padding, padx=main.canvas_padding
    )

    root.mainloop()
