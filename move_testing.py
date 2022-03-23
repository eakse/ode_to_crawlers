from turtle import width
from ode.constants import *
from ode.map import Map
from ode.party import Party
from PIL import Image, ImageTk
import tkinter as tk
from functools import wraps


fsize = lambda x: x * TILESIZE
# rotate = lambda x: x * 90


class MapCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        self.img_settings = {"anchor": "nw"}

        self.party_x = 0
        self.party_y = 0
        # yes I can set this directly to 0 but forwards compatability
        self.facing_index = FACING_LIST.index(NORTH)

        # clean the kwargs to pass on to the parent init

        super().__init__(parent, *args, self.custom_process_kwargs(**kwargs))

        self.party_images = [
            ImageTk.PhotoImage(Image.open(f"{PATH_IMAGES_PARTY}{facing}.png"))
            for facing in FACING_LIST
        ]
        self.map_image = ImageTk.PhotoImage(parent.map.get_image())
        self.custom_update()

    def custom_process_kwargs(self, **kwargs) -> dict:
        """parse kwards, and return leftover"""
        result = {}
        for key, value in kwargs.items():
            if key == K_PARTY_X:
                self.party_x = value
            elif key == K_PARTY_Y:
                self.party_y = value
            elif key == K_FACING_INDEX:
                self.facing_index = value
            else:
                result[key] = value
        return result

    def custom_move(self, **kwargs):
        self.custom_process_kwargs(**kwargs)
        self.custom_update()

    def custom_update(self):
        self.create_image(0, 0, image=self.map_image, **self.img_settings)
        self.create_image(
            fsize(self.party_x),
            fsize(self.party_y),
            image=self.party_images[self.facing_index],
            **self.img_settings,
        )


class InfoBlock(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.obj_defaults = {"anchor": "nw"}
        self.north = NONE
        self.east = NONE
        self.south = NONE
        self.west = NONE
        self.info_data = {}
        super().__init__(parent, *args, self.custom_process_kwargs(**kwargs))
        self.north_strvar = tk.StringVar()
        self.north_label = tk.Label(self, textvariable=self.north_strvar)
        self.north_label.grid(row=0, column=1)
        self.east_strvar = tk.StringVar()
        self.east_label = tk.Label(self, textvariable=self.east_strvar)
        self.east_label.grid(row=1, column=2)
        self.south_strvar = tk.StringVar()
        self.south_label = tk.Label(self, textvariable=self.south_strvar)
        self.south_label.grid(row=2, column=1)
        self.west_strvar = tk.StringVar()
        self.west_label = tk.Label(self, textvariable=self.west_strvar)
        self.west_label.grid(row=1, column=0)
        self.custom_update(data=self.info_data)

    def custom_update(self, data: dict = {}):
        if len(data) > 0:
            for key, value in data.items():
                if key in FACING_LIST:
                    # print(key, value.style)
                    setattr(self, key, value.style)
        for key in FACING_LIST:
            label = getattr(self, f"{key}_strvar")
            label.set(getattr(self, key))



    def custom_process_kwargs(self, **kwargs) -> dict:
        """parse kwards, and return leftover"""
        result = {}
        for key, value in kwargs.items():
            if key == K_INFO_BLOCK_DATA:
                setattr(self, K_INFO_BLOCK_DATA, value)
            else:
                result[key] = value
        return result


class Movement(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.map = Map.load_blosc("C:/###VS Projects/ode_to_crawlers/data/maps/1.map")
        self.map.dev_mode = False
        self.party = Party()
        self.party.facing = EAST
        self.party.x = 10
        self.party.y = 4
        self.mapcanvas = MapCanvas(
            self,
            width=fsize(self.map.width),
            height=fsize(self.map.height),
            **self.party.dump_map_paint,
        )
        self.mapgridinfo = InfoBlock(
            self, info_data=self.map.tiles[self.party.x][self.party.y].dump_long_dict, width=200
        )

        self.mapcanvas.grid(row=0, column=0)
        self.mapgridinfo.grid(row=0, column=1)
        self.create_bindings()

        # self.map_label = tk.Label(self, image = self.map_image, bg=TKINTER_TRANSPARENT_COLOR)
        # self.map_label.place(x=0, y=0)

        # self.party_label = tk.Label(self, image = self.party_img, bg=TKINTER_TRANSPARENT_COLOR)
        # self.party_label.place(x=0, y=0)

    def custom_update(self):
        # print(map.tiles[self.party.x][self.party.y].dump)
        self.mapcanvas.custom_move(**self.party.dump_map_paint)
        self.mapgridinfo.custom_update(self.map.tiles[self.party.x][self.party.y].dump_long_dict)

    def create_bindings(self):
        self.mapcanvas.bind_all("<w>", self.move_forward)
        self.mapcanvas.bind_all("<a>", self.move_turn_left)
        self.mapcanvas.bind_all("<s>", self.move_turn_around)
        self.mapcanvas.bind_all("<d>", self.move_turn_right)
        self.mapcanvas.bind_all("<Escape>", exit)

    # def update_decorator(func):
    #     def wrap(*args, **kwargs):
    #         result = func(*args, **kwargs)
    #         # custom_update()
    #         return result
    #     return wrap

    # @update_decorator
    def move_forward(self, _):
        if self.map.tiles[self.party.x][self.party.y].passable[self.party.facing]:
            print("y", self.party.facing, self.map.tiles[self.party.x][self.party.y].dump)
            self.party.forward
        else:
            print("n")
        self.custom_update()

    # @update_decorator
    def move_turn_left(self, _):
        self.party.left
        self.custom_update()

    # @update_decorator
    def move_turn_around(self, _):
        self.party.turn
        self.custom_update()

    # @update_decorator
    def move_turn_right(self, _):
        self.party.right
        self.custom_update()


if __name__ == "__main__":
    root = tk.Tk(className=" ODE Movement Tester")
    # root.geometry("1024x768")
    # root.wm_attributes("-transparentcolor", TKINTER_TRANSPARENT_COLOR)
    root.option_add("*tearOff", False)
    root.config(bg="white")
    main = Movement(root)

    main.pack(fill="both", expand=True)

    root.mainloop()
