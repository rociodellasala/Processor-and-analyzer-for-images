from tkinter import Menu, messagebox, ttk, Entry
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from image_operations import gamma_pow_function
from image_operations import dynamic_range_compression
from threshold_calculator import image_threshold
from image_operations import image_equalization
from image_operations import grey_level_histogram
from threshold_calculator import otsu_threshold, global_threshold, otsu_threshold_with_color


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
        dynamic_range_compression(interface.current_image, constants.WIDTH, constants.HEIGHT)
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


def global_threshold_wrapper(image, height, width, interface):
    if image is not None:
        interface.delete_widgets(interface.buttons_frame)
        threshold_value = global_threshold(image, height, width)
        ttk.Label(interface.buttons_frame, text="Threshold value:",
                  background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text=int(threshold_value),
                  background=constants.TOP_COLOR).grid(row=0, column=1)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply the global threshold")


def otsu_threshold_wrapper(image, height, width, interface):
    if image is not None:
        interface.delete_widgets(interface.buttons_frame)
        threshold_value = otsu_threshold(image, height, width)
        ttk.Label(interface.buttons_frame, text="Threshold value:",
                  background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text=int(threshold_value)
                  , background=constants.TOP_COLOR).grid(row=0, column=1)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply otsu's threshold")


def otsu_threshold_with_color_wrapper(image, height, width, interface):
    if image is not None:
        interface.delete_widgets(interface.buttons_frame)
        threshold_value = otsu_threshold_with_color(image, height, width)
        ttk.Label(interface.buttons_frame, text="Red threshold value:",
                  background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text=int(threshold_value[0]),
                  background=constants.TOP_COLOR).grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Green threshold value:",
                  background=constants.TOP_COLOR).grid(row=1, column=0)
        ttk.Label(interface.buttons_frame, text=int(threshold_value[1]),
                  background=constants.TOP_COLOR).grid(row=1, column=1)
        ttk.Label(interface.buttons_frame, text="Blue threshold value:",
                  background=constants.TOP_COLOR).grid(row=2, column=0)
        ttk.Label(interface.buttons_frame, text=int(threshold_value[2]),
                  background=constants.TOP_COLOR).grid(row=2, column=1)

    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply otsu's threshold")


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
        threshold_menu = Menu(function_menu, tearoff=0)
        function_menu.add_cascade(label="Threshold", menu=threshold_menu)
        threshold_menu.add_command(label="Custom", command=generate_image_threshold_input)
        threshold_menu.add_command(label="Global", command=lambda:
        global_threshold_wrapper(interface.current_image, constants.HEIGHT, constants.WIDTH, interface))
        otsu_menu = Menu(function_menu, tearoff=0)
        threshold_menu.add_cascade(label="Otsu", menu=otsu_menu)
        otsu_menu.add_command(label="B&W", command=lambda:
            otsu_threshold_wrapper(interface.current_image, constants.HEIGHT, constants.WIDTH, interface))
        otsu_menu.add_command(label="RGB", command=lambda:
            otsu_threshold_with_color_wrapper(interface.current_image, constants.HEIGHT, constants.WIDTH, interface))
        function_menu.add_command(label="Equalization", command=lambda:
            equalized_image_wrapper(interface.current_image, constants.WIDTH, constants.HEIGHT, interface))
        function_menu.add_command(label="Grey Histogram", command=lambda:
            grey_level_histogram_wrapper(interface.current_image, constants.WIDTH, constants.HEIGHT, interface))
