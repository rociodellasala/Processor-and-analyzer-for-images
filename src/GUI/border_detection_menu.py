from tkinter import Menu, messagebox
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from border_detectors import prewit_detection, sobel_detection, \
    prewit_color_detection, sobel_color_detection


def prewit_detection_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to detect borders")
    else:
        prewit_detection(interface.current_image, constants.HEIGHT, constants.WIDTH)


def prewit_color_detection_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to detect borders")
    else:
        prewit_color_detection(interface.current_image, constants.HEIGHT, constants.WIDTH)


def sobel_detection_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to detect borders")
    else:
        sobel_detection(interface.current_image, constants.HEIGHT, constants.WIDTH)


def sobel_color_detection_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to detect borders")
    else:
        sobel_color_detection(interface.current_image, constants.HEIGHT, constants.WIDTH)


class BorderDetectionMenu:
    def __init__(self, menubar):
        border_detection_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Border detection", menu=border_detection_menu)
        prewit_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Prewitt", menu=prewit_menu)
        prewit_menu.add_command(label="Color", command=prewit_color_detection_wrapper)
        prewit_menu.add_command(label="B&W", command=prewit_detection_wrapper)
        sobel_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Sobel", menu=sobel_menu)
        sobel_menu.add_command(label="Color", command=sobel_color_detection_wrapper)
        sobel_menu.add_command(label="B&W", command=sobel_detection_wrapper)

