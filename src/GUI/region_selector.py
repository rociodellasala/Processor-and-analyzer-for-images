import tkinter as tk
from PIL import Image, ImageTk
from src.GUI.interface_info import InterfaceInfo
from src.GUI import gui_constants as constants
from src.GUI import gui_constants as color
import numpy as np


class Region:
    __instance = None

    def __init__(self):
        if Region.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            interface = InterfaceInfo.get_instance()
            self.canvas = interface.canvas
            self.current_image = interface.current_image
            self.x = self.y = 0
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

            self.rect = None
            self.end_x = None
            self.end_y = None
            self.start_x = None
            self.start_y = None

    def on_button_press(self, event):
        self.reset_region_selector()
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        # if not self.rect:
        select_opts2 = dict(dash=(2, 2), fill='', outline='green')
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, **select_opts2)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.calculate_region()
        pass

    def reset_region_selector(self):
        self.canvas.delete(self.rect)
        self.rect = None
        self.end_x = None
        self.end_y = None
        self.start_x = None
        self.start_y = None

    def calculate_region(self):
        pixels = np.array(self.current_image)
        # self.end_x -= 2
        # self.end_y -= 2
        # self.start_x -= 2
        # self.start_y -= 2
        print("Top left")
        print(self.start_x)
        print(self.start_y)
        print("Bottom right")
        print(self.end_x)
        print(self.end_y)
        print("imprimiendo colores")
        # for i in range(self.start_x, self.end_x):
        #     for j in range(self.start_y, self.end_y):
        #         if pixels[j, i] != constants.MAX_COLOR_VALUE:
        #             print("negro")
        # print("----------------------")
        print(pixels[self.start_y, self.start_x])
        print(pixels[self.end_y, self.end_x])


