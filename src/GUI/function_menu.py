from tkinter import Menu, messagebox, ttk, Entry
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from image_operations import gamma_pow_function
from image_operations import dynamic_range_compression
from threshold_calculator import image_threshold
from image_operations import image_equalization
from image_operations import grey_level_histogram


def generate_gamma_input():
    interface = InterfaceInfo.get_instance()
    interface.delete_widgets(interface.buttons_frame)
    if interface.current_image is not None:
        ttk.Label(interface.buttons_frame, text="Gamma", background=constants.TOP_COLOR).grid(row=0, column=0)
        gamma = Entry(interface.buttons_frame)
        gamma.grid(row=0, column=1)
        apply_button = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: gamma_pow_function_wrapper(interface.current_image, constants.WIDTH,
                                                                             constants.HEIGHT, gamma.get()))
        apply_button.grid(row=1, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image to apply gamma")


def gamma_pow_function_wrapper(image, width, height, gamma):
    error = False
    try:
        gamma_value = float(gamma)
    except ValueError:
        error = True
        messagebox.showerror(title="Error", message="You need to insert a valid gamma")
    if (not error) and image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to apply gamma")
    elif not error:
        gamma_pow_function(image, width, height, gamma_value)


def generate_range_compression_input():
    interface = InterfaceInfo.get_instance()
    interface.delete_widgets(interface.buttons_frame)
    if interface.current_image is not None:
        dynamic_range_compression(interface.current_image, constants.WIDTH,constants.HEIGHT)
    else:
        messagebox.showerror(title="Error", message="You must upload an image to generate range compression")


def generate_image_threshold_input():
    interface = InterfaceInfo.get_instance()
    interface.delete_widgets(interface.buttons_frame)
    if interface.current_image is not None:
        ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
        threshold = Entry(interface.buttons_frame)
        threshold.grid(row=0, column=1)
        apply_threshold = ttk.Button(interface.buttons_frame, text="Apply",
                                     command=lambda: image_threshold(interface.current_image, constants.WIDTH,
                                                                     constants.HEIGHT, float(threshold.get())))
        apply_threshold.grid(row=1, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image to apply a threshold")


def equalized_image_wrapper(image, width, height, interface):
    if image is not None:
        interface.delete_widgets(interface.buttons_frame)
        image_equalization(image, width, height)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to get the equalized histogram")


def grey_level_histogram_wrapper(image, width, height, interface):
    if image is not None:
        interface.delete_widgets(interface.buttons_frame)
        grey_level_histogram(image, width, height)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to get the equalized histogram")


class FunctionMenu:
    def __init__(self, menubar):
        interface = InterfaceInfo.get_instance()
        function_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Function", menu=function_menu)
        function_menu.add_command(label="Gamma", command=generate_gamma_input)
        function_menu.add_command(label="Dynamic Range Compression", command=generate_range_compression_input)
        function_menu.add_command(label="Threshold", command=generate_image_threshold_input)
        function_menu.add_command(label="Equalization",
                                  command=lambda: equalized_image_wrapper(interface.current_image, constants.WIDTH,
                                                                          constants.HEIGHT, interface))
        function_menu.add_command(label="Grey Histogram",
                                  command=lambda: grey_level_histogram_wrapper(interface.current_image, constants.WIDTH,
                                                                               constants.HEIGHT, interface))
