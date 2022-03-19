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
        # self.mapcanvas.place(x=0, y=0)
        self.mapcanvas.grid(row=1,column=0)
        self.create_bindings()

        # self.map_label = tk.Label(self, image = self.map_image, bg=TKINTER_TRANSPARENT_COLOR)
        # self.map_label.place(x=0, y=0)

        # self.party_label = tk.Label(self, image = self.party_img, bg=TKINTER_TRANSPARENT_COLOR)
        # self.party_label.place(x=0, y=0)

    def custom_update(self):
        # print(map.tiles[self.party.x][self.party.y].dump)
        self.mapcanvas.custom_move(**self.party.dump_map_paint)

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
        x,y = self.party.forward_coords()
        if self.map.tiles[x][y].passable[self.party.facing]:
            print("y")
        else:
            print("n")
        self.party.forward
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
