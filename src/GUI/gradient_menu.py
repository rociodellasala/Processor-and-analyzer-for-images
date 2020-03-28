from tkinter import Menu, ttk, Entry, BooleanVar, Checkbutton
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from image_generator import gray_faded_image
from image_generator import color_faded_image


def generate_gray_fading_input():
    interface = InterfaceInfo.get_instance()
    interface.reset_parameters()
    ttk.Label(interface.buttons_frame, text="Image width", background=constants.TOP_COLOR).grid(row=0, column=0)
    ttk.Label(interface.buttons_frame, text="Image height", background=constants.TOP_COLOR).grid(row=1, column=0)
    image_width = Entry(interface.buttons_frame)
    image_height = Entry(interface.buttons_frame)
    image_width.grid(row=0, column=1)
    image_height.grid(row=1, column=1)
    generate_gray_fading_button = ttk.Button(interface.buttons_frame, text="Show", command=lambda:
    gray_faded_image(int(image_width.get()), int(image_height.get())))
    generate_gray_fading_button.grid(row=3, column=0)


def generate_color_fading_input():
    interface = InterfaceInfo.get_instance()
    interface.reset_parameters()
    ttk.Label(interface.buttons_frame, text="Image width", background=constants.TOP_COLOR).grid(row=0, column=0)
    ttk.Label(interface.buttons_frame, text="Image height", background=constants.TOP_COLOR).grid(row=1, column=0)
    red = BooleanVar()
    green = BooleanVar()
    blue = BooleanVar()
    Checkbutton(interface.buttons_frame, text="Red", variable=red,
                background=constants.TOP_COLOR).grid(row=2, column=0)
    Checkbutton(interface.buttons_frame, text="Green", variable=green,
                background=constants.TOP_COLOR).grid(row=2, column=1)
    Checkbutton(interface.buttons_frame, text="Blue", variable=blue,
                background=constants.TOP_COLOR).grid(row=2, column=2)
    image_width = Entry(interface.buttons_frame)
    image_height = Entry(interface.buttons_frame)
    image_width.grid(row=0, column=1)
    image_height.grid(row=1, column=1)
    generate_gray_fading_button = ttk.Button(interface.buttons_frame, text="Show",
                                             command=lambda: color_faded_image(int(image_width.get()),
                                                                               int(image_height.get()),
                                                                               red.get(), green.get(),
                                                                               blue.get()))
    generate_gray_fading_button.grid(row=3, column=0)


class GradientMenu:
    def __init__(self, menubar):
        gradient_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gradient", menu=gradient_menu)
        gradient_menu.add_command(label="Gray", command=generate_gray_fading_input)
        gradient_menu.add_command(label="Color", command=generate_color_fading_input)