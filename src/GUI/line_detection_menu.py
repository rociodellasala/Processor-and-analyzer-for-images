from tkinter import Menu, Entry, messagebox, ttk

from line_detectors import pixel_exchange, pixel_exchange_in_video, circular_hough_transform, hough_transform
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from src.GUI.region_selector import Region

def generate_hough_circle_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
        threshold = Entry(interface.buttons_frame)
        threshold.grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Epsilon", background=constants.TOP_COLOR).grid(row=1, column=0)
        epsilon = Entry(interface.buttons_frame)
        epsilon.grid(row=1, column=1)
        ttk.Label(interface.buttons_frame, text="Radius", background=constants.TOP_COLOR).grid(row=0, column=2)
        radius = Entry(interface.buttons_frame)
        radius.grid(row=0, column=3)
        apply_method = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: circular_hough_transform(interface.current_image, constants.HEIGHT,
                                                               constants.WIDTH, int(threshold.get()), float(epsilon.get()),
                                                                int(radius.get())))
        apply_method.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply hough")


def generate_line_circle_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
        threshold = Entry(interface.buttons_frame)
        threshold.grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Epsilon", background=constants.TOP_COLOR).grid(row=1, column=0)
        epsilon = Entry(interface.buttons_frame)
        epsilon.grid(row=1, column=1)
        apply_method = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: hough_transform(interface.current_image, constants.HEIGHT,
                                                                           constants.WIDTH, int(threshold.get()),
                                                                           float(epsilon.get())))
        apply_method.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply hough")


def pixel_exchange_grey_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to mark a region")
    else:
        interface.delete_widgets(interface.buttons_frame)
        region = Region()
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Epsilon", background=constants.TOP_COLOR).grid(row=0, column=0)
        epsilon = Entry(interface.buttons_frame)
        epsilon.grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Max iterations", background=constants.TOP_COLOR).grid(row=1, column=0)
        max_iterations = Entry(interface.buttons_frame)
        max_iterations.grid(row=1, column=1)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: generate_pixel_exchange_grey_input(interface, region,
                                                                                      float(epsilon.get()),
                                                                                     int(max_iterations.get())))
        apply_filter.grid(row=2, column=0)


def generate_pixel_exchange_grey_input(interface, region, epsilon, max_iterations):
    if region.start_x is None or region.start_y is None or region.end_x is None or region.end_y is None:
        messagebox.showerror(title="Error", message="You have to mark a region before")
    elif abs(region.start_x - region.end_x) == 0:
        messagebox.showerror(title="Error", message="You have to mark a bigger region")
    else:
        pixel_exchange(interface.current_image, constants.HEIGHT, constants.WIDTH, region.start_x, region.start_y,
                       region.end_x, region.end_y, epsilon, max_iterations, True)


def pixel_exchange_color_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to mark a region")
    else:
        interface.delete_widgets(interface.buttons_frame)
        region = Region()
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Epsilon", background=constants.TOP_COLOR).grid(row=0, column=0)
        epsilon = Entry(interface.buttons_frame)
        epsilon.grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Max iterations", background=constants.TOP_COLOR).grid(row=1, column=0)
        max_iterations = Entry(interface.buttons_frame)
        max_iterations.grid(row=1, column=1)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: generate_pixel_exchange_color_input(interface, region,
                                                                                      float(epsilon.get()),
                                                                                     int(max_iterations.get())))
        apply_filter.grid(row=2, column=0)


def generate_pixel_exchange_color_input(interface, region, epsilon, max_iterations):
    if region.start_x is None or region.start_y is None or region.end_x is None or region.end_y is None:
        messagebox.showerror(title="Error", message="You have to mark a region before")
    elif abs(region.start_x - region.end_x) == 0:
        messagebox.showerror(title="Error", message="You have to mark a bigger region")
    else:
        pixel_exchange(interface.current_image, constants.HEIGHT, constants.WIDTH, region.start_x, region.start_y,
                       region.end_x, region.end_y, epsilon, max_iterations, False)


def pixel_exchange_video_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to mark a region")
    else:
        interface.delete_widgets(interface.buttons_frame)
        region = Region()
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Epsilon", background=constants.TOP_COLOR).grid(row=0, column=0)
        epsilon = Entry(interface.buttons_frame)
        epsilon.grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Max iterations", background=constants.TOP_COLOR).grid(row=1, column=0)
        max_iterations = Entry(interface.buttons_frame)
        max_iterations.grid(row=1, column=1)
        ttk.Label(interface.buttons_frame, text="Quantity", background=constants.TOP_COLOR).grid(row=0, column=2)
        quantity = Entry(interface.buttons_frame)
        quantity.grid(row=0, column=3)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: generate_pixel_exchange_video_input(interface, region, float(epsilon.get()),
                                                                          int(max_iterations.get()),
                                                                          int(quantity.get())))
        apply_filter.grid(row=2, column=0)


def generate_pixel_exchange_video_input(interface, region, epsilon, max_iterations, quantity):
    if region.start_x is None or region.start_y is None or region.end_x is None or region.end_y is None:
        messagebox.showerror(title="Error", message="You have to mark a region before")
    elif abs(region.start_x - region.end_x) == 0:
        messagebox.showerror(title="Error", message="You have to mark a bigger region")
    else:
        pixel_exchange_in_video(interface.current_image, constants.HEIGHT,
                                constants.WIDTH, interface.current_image_name,
                                region.start_x, region.start_y, region.end_x,
                                region.end_y, epsilon,
                                max_iterations,
                                quantity,
                                False, False)


class LineDetectorMenu:
    def __init__(self, menubar):
        line_detection_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Line detection", menu=line_detection_menu)
        hough_menu = Menu(line_detection_menu, tearoff=0)
        line_detection_menu.add_cascade(label="Hough", menu=hough_menu)
        hough_menu.add_command(label="Circle", command=generate_hough_circle_input)
        hough_menu.add_command(label="Lines", command=generate_line_circle_input)
        pixel_exchange = Menu(line_detection_menu, tearoff=0)
        line_detection_menu.add_cascade(label="Pixel exchange", menu=pixel_exchange)
        photo_menu = Menu(pixel_exchange, tearoff=0)
        pixel_exchange.add_cascade(label="Photo", menu=photo_menu)
        photo_menu.add_command(label="Grey", command=pixel_exchange_grey_wrapper)
        photo_menu.add_command(label="Color", command=pixel_exchange_color_wrapper)
        pixel_exchange.add_command(label="Video", command=pixel_exchange_video_wrapper)


