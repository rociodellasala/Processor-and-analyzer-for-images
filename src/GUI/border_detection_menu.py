from tkinter import Menu, Entry, messagebox, ttk, Radiobutton, StringVar, IntVar
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from border_detectors import prewit_detection, sobel_detection, \
    prewit_color_detection, sobel_color_detection
from filters import border_enhancement_filter
from border_detectors import laplacian_method, laplacian_method_with_slope_evaluation,\
    laplacian_gaussian_method, four_direction_border_detection


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


def generate_four_direction_input():
    interface = InterfaceInfo.get_instance()
    interface.delete_widgets(interface.buttons_frame)
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to detect borders")
    else:
        radio_var = IntVar()
        radio_var.set(1)
        Radiobutton(interface.buttons_frame, text="Prewitt", value=2, variable=radio_var,
                    background=constants.TOP_COLOR).grid(row=1, column=0)
        Radiobutton(interface.buttons_frame, text="Sobel", value=1, variable=radio_var,
                    background=constants.TOP_COLOR).grid(row=1, column=1)
        Radiobutton(interface.buttons_frame, text="Kirsh", value=3, variable=radio_var,
                    background=constants.TOP_COLOR).grid(row=1, column=2)

        detect_borders_button = ttk.Button(interface.buttons_frame, text="Detect Borders",
                                           command=lambda:four_direction_border_detection(interface.current_image,
                                                                                          constants.HEIGHT,
                                                                                          constants.WIDTH,
                                                                                          radio_var.get()))
        detect_borders_button.grid(row=2, column=0)


def border_enhancement_filter_wrapper(image, width, height):
    interface = InterfaceInfo.get_instance()
    interface.delete_widgets(interface.buttons_frame)
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to get its negative")
    else:
        border_enhancement_filter(image, width, height)


def generate_laplacian_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        radio_var = StringVar()
        radio_var.set("or")
        Radiobutton(interface.buttons_frame, text="And", value="and",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=0)
        Radiobutton(interface.buttons_frame, text="Or", value="or",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=1)
        Radiobutton(interface.buttons_frame, text="Module", value="module",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=2)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: laplacian_method(interface.current_image,
                                                                             constants.WIDTH, constants.HEIGHT,
                                                                             radio_var.get()))
        apply_filter.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply isotropic diffusion filter")


def generate_laplacian_gaussian_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Sigma", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=2)
        sigma = Entry(interface.buttons_frame)
        threshold = Entry(interface.buttons_frame)
        sigma.grid(row=0, column=1)
        threshold.grid(row=0, column=3)
        radio_var = StringVar()
        radio_var.set("or")
        Radiobutton(interface.buttons_frame, text="And", value="and",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=0)
        Radiobutton(interface.buttons_frame, text="Or", value="or",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=1)
        Radiobutton(interface.buttons_frame, text="Module", value="module",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=2)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: laplacian_gaussian_method(interface.current_image,
                                                                            constants.HEIGHT, constants.WIDTH,
                                                                            float(sigma.get()), int(threshold.get()),
                                                                            radio_var.get()))
        apply_filter.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply isotropic diffusion filter")


def generate_laplacian_with_slope_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
        threshold = Entry(interface.buttons_frame)
        threshold.grid(row=0, column=1)
        radio_var = StringVar()
        radio_var.set("or")
        Radiobutton(interface.buttons_frame, text="And", value="and",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=0)
        Radiobutton(interface.buttons_frame, text="Or", value="or",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=1)
        Radiobutton(interface.buttons_frame, text="Module", value="module",
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=2)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: laplacian_method_with_slope_evaluation(interface.current_image,
                                                                            constants.WIDTH, constants.HEIGHT,
                                                                            int(threshold.get()),
                                                                            radio_var.get()))
        apply_filter.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply isotropic diffusion filter")


class BorderDetectionMenu:
    def __init__(self, menubar):
        interface = InterfaceInfo.get_instance()
        border_detection_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Border detection", menu=border_detection_menu)
        border_detection_menu.add_command(label="Border enhancement",
                                          command=lambda: border_enhancement_filter_wrapper(interface.current_image,
                                                                                            constants.WIDTH,
                                                                                            constants.HEIGHT))
        prewit_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Prewitt", menu=prewit_menu)
        prewit_menu.add_command(label="B&W", command=prewit_detection_wrapper)
        prewit_menu.add_command(label="Color", command=prewit_color_detection_wrapper)
        sobel_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Sobel", menu=sobel_menu)
        sobel_menu.add_command(label="B&W", command=sobel_detection_wrapper)
        sobel_menu.add_command(label="Color", command=sobel_color_detection_wrapper)
        border_detection_menu.add_command(label="Four directions", command=generate_four_direction_input)
        border_detection_menu.add_command(label="Laplacian", command=generate_laplacian_input)
        border_detection_menu.add_command(label="Laplacian with slope", command=generate_laplacian_with_slope_input)
        border_detection_menu.add_command(label="Laplacian Gaussian", command=generate_laplacian_gaussian_input)


