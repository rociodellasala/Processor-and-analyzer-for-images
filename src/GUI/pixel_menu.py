from tkinter import Menu, messagebox, ttk, Entry
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo


def generate_get_pixel_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="X", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Y", background=constants.TOP_COLOR).grid(row=1, column=0)
        x = Entry(interface.buttons_frame)
        y = Entry(interface.buttons_frame)
        x.grid(row=0, column=1)
        y.grid(row=1, column=1)
        get_pixel_button = ttk.Button(interface.buttons_frame,
                                      text="Get Value",
                                      command=lambda: get_pixel_value(interface, x.get(), y.get()))
        get_pixel_button.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image to get the value of a pixel")


def get_pixel_value(interface, x, y):
    px = interface.current_image.load()
    ttk.Label(interface.buttons_frame, text=px[int(y), int(x)], background=constants.TOP_COLOR).grid(row=2, column=1)


def generate_modify_pixel_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="X", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Y", background=constants.TOP_COLOR).grid(row=1, column=0)
        ttk.Label(interface.buttons_frame, text="Value", background=constants.TOP_COLOR).grid(row=0, column=2)
        x = Entry(interface.buttons_frame)
        y = Entry(interface.buttons_frame)
        value = Entry(interface.buttons_frame)
        x.grid(row=0, column=1)
        y.grid(row=1, column=1)
        value.grid(row=0, column=3)
        modify_pixel_button = ttk.Button(interface.buttons_frame, text="Set Value",
                                         command=lambda: modify_pixel_value(interface, int(x.get()),
                                                                            int(y.get()), int(value.get())))
        modify_pixel_button.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image to modify the value of a pixel")


def modify_pixel_value(interface, x, y, value):
    px = interface.current_image.load()
    px[int(x), int(y)] = value
    global save_path
    interface.current_image.save(save_path + "pixel_modification.png")
    interface.current_image.show()


class PixelMenu:
    def __init__(self, menubar):
        pixel_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pixel", menu=pixel_menu)
        pixel_menu.add_command(label="Get", command=generate_get_pixel_input)
        pixel_menu.add_command(label="Modify", command=generate_modify_pixel_input)


save_path = "../../draws/"
