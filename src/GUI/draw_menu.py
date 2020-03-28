from tkinter import Menu, ttk, Entry, Radiobutton, BooleanVar
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from image_generator import generate_rectangle
from image_generator import generate_circle


def generate_rectangle_input():
    interface = InterfaceInfo.get_instance()
    interface.clean_images()
    interface.delete_widgets(interface.buttons_frame)
    interface.delete_widgets(interface.image_frame)
    ttk.Label(interface.buttons_frame, text="Rectangle width", background=constants.TOP_COLOR).grid(row=0, column=0)
    ttk.Label(interface.buttons_frame, text="Rectangle height", background=constants.TOP_COLOR).grid(row=1, column=0)
    ttk.Label(interface.buttons_frame, text="Image width", background=constants.TOP_COLOR).grid(row=0, column=2)
    ttk.Label(interface.buttons_frame, text="Image height", background=constants.TOP_COLOR).grid(row=1, column=2)
    width = Entry(interface.buttons_frame)
    height = Entry(interface.buttons_frame)
    image_width = Entry(interface.buttons_frame)
    image_height = Entry(interface.buttons_frame)
    radio_var = BooleanVar()
    radio_var.set(True)
    Radiobutton(interface.buttons_frame, text="Empty", value=False, variable=radio_var,
                background=constants.TOP_COLOR).grid(row=1, column=4)
    Radiobutton(interface.buttons_frame, text="Filled", value=True, variable=radio_var,
                background=constants.TOP_COLOR).grid(row=0, column=4)
    width.grid(row=0, column=1)
    height.grid(row=1, column=1)
    image_width.grid(row=0, column=3)
    image_height.grid(row=1, column=3)
    draw_pixel_button = ttk.Button(interface.buttons_frame, text="Draw",
                                   command=lambda: generate_rectangle("rectangle.png", int(image_width.get()),
                                                                      int(image_height.get()), int(width.get()),
                                                                      int(height.get()), radio_var.get()))
    # TODO validate params
    draw_pixel_button.grid(row=3, column=0)


def generate_circle_input():
    interface = InterfaceInfo.get_instance()
    interface.clean_images()
    interface.delete_widgets(interface.buttons_frame)
    interface.delete_widgets(interface.image_frame)
    ttk.Label(interface.buttons_frame, text="Radius", background=constants.TOP_COLOR).grid(row=0, column=2)
    ttk.Label(interface.buttons_frame, text="Image width", background=constants.TOP_COLOR).grid(row=0, column=0)
    ttk.Label(interface.buttons_frame, text="Image height", background=constants.TOP_COLOR).grid(row=1, column=0)
    radius = Entry(interface.buttons_frame)
    image_width = Entry(interface.buttons_frame)
    image_height = Entry(interface.buttons_frame)
    radio_var = BooleanVar()
    radio_var.set(True)
    Radiobutton(interface.buttons_frame, text="Filled", value=True,
                variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=4)
    Radiobutton(interface.buttons_frame, text="Empty", value=False,
                variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=4)
    radius.grid(row=0, column=3)
    image_width.grid(row=0, column=1)
    image_height.grid(row=1, column=1)
    draw_pixel_button = ttk.Button(interface.buttons_frame, text="Draw",
                                   command=lambda:generate_circle("circle.png", int(image_width.get()),
                                                                  int(image_height.get()), int(radius.get()),
                                                                  radio_var.get()))
    # Todo validate params
    draw_pixel_button.grid(row=3, column=0)


class DrawMenu:
    def __init__(self, menubar):
        draw_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Draw", menu=draw_menu)
        draw_menu.add_command(label="Rectangle", command=generate_rectangle_input)
        draw_menu.add_command(label="Circle", command=generate_circle_input)
