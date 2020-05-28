from tkinter import Menu, Entry, messagebox, ttk, Radiobutton, StringVar, IntVar, BooleanVar

from line_detectors import pixel_exchange, pixel_exchange_in_video, circular_hough_transform, hough_transform
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from border_detectors import prewit_detection, sobel_detection, \
    prewit_color_detection, sobel_color_detection
from filters import border_enhancement_filter
from border_detectors import laplacian_method, laplacian_method_with_slope_evaluation,\
    laplacian_gaussian_method, four_direction_border_detection, canny_method, susan_method, colored_canny_method
from src.GUI.region_selector import Region


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


def generate_canny_method_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Sigma S", background=constants.TOP_COLOR).grid(row=0, column=0)
        sigma_s = Entry(interface.buttons_frame)
        sigma_s.grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Sigma R", background=constants.TOP_COLOR).grid(row=1, column=0)
        sigma_r = Entry(interface.buttons_frame)
        sigma_r.grid(row=1, column=1)
        ttk.Label(interface.buttons_frame, text="Windows size", background=constants.TOP_COLOR).grid(row=0, column=2)
        windows_size = Entry(interface.buttons_frame)
        windows_size.grid(row=0, column=3)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(interface.buttons_frame, text="Four neighbours", value=True,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=4)
        Radiobutton(interface.buttons_frame, text="Eight neighbours", value=False,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=4)
        apply_method = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: canny_method(interface.current_image, constants.HEIGHT,
                                                               constants.WIDTH, int(sigma_s.get()), int(sigma_r.get()),
                                                               int(windows_size.get()), radio_var.get()))
        apply_method.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply canny method")


def generate_canny_color_method_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Sigma S", background=constants.TOP_COLOR).grid(row=0, column=0)
        sigma_s = Entry(interface.buttons_frame)
        sigma_s.grid(row=0, column=1)
        ttk.Label(interface.buttons_frame, text="Sigma R", background=constants.TOP_COLOR).grid(row=1, column=0)
        sigma_r = Entry(interface.buttons_frame)
        sigma_r.grid(row=1, column=1)
        ttk.Label(interface.buttons_frame, text="Windows size", background=constants.TOP_COLOR).grid(row=0, column=2)
        windows_size = Entry(interface.buttons_frame)
        windows_size.grid(row=0, column=3)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(interface.buttons_frame, text="Four neighbours", value=True,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=4)
        Radiobutton(interface.buttons_frame, text="Eight neighbours", value=False,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=4)
        apply_method = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: colored_canny_method(interface.current_image, constants.HEIGHT,
                                                               constants.WIDTH, int(sigma_s.get()), int(sigma_r.get()),
                                                               int(windows_size.get()), radio_var.get()))
        apply_method.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply canny method")


def generate_susan_method_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="T difference", background=constants.TOP_COLOR).grid(row=0, column=0)
        t_difference = Entry(interface.buttons_frame)
        t_difference.grid(row=0, column=1)
        apply_method = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: susan_method(interface.current_image, constants.HEIGHT,
                                                               constants.WIDTH, int(t_difference.get())))
        apply_method.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply susan method")


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
        prewit_menu.add_command(label="Grey", command=prewit_detection_wrapper)
        prewit_menu.add_command(label="Color", command=prewit_color_detection_wrapper)
        sobel_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Sobel", menu=sobel_menu)
        sobel_menu.add_command(label="Grey", command=sobel_detection_wrapper)
        sobel_menu.add_command(label="Color", command=sobel_color_detection_wrapper)
        border_detection_menu.add_command(label="Four directions", command=generate_four_direction_input)
        border_detection_menu.add_command(label="Laplacian", command=generate_laplacian_input)
        border_detection_menu.add_command(label="Laplacian with slope", command=generate_laplacian_with_slope_input)
        border_detection_menu.add_command(label="Laplacian Gaussian", command=generate_laplacian_gaussian_input)
        canny_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Canny", menu=canny_menu)
        canny_menu.add_command(label="Grey", command=generate_canny_method_input)
        canny_menu.add_command(label="Color", command=generate_canny_color_method_input)
        border_detection_menu.add_command(label="Susan Detector", command=generate_susan_method_input)
        hough_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Hough", menu=hough_menu)
        hough_menu.add_command(label="Circle", command=generate_hough_circle_input)
        hough_menu.add_command(label="Lines", command=generate_line_circle_input)
        pixel_exchange = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Pixel exchange", menu=pixel_exchange)
        photo_menu = Menu(pixel_exchange, tearoff=0)
        pixel_exchange.add_cascade(label="Photo", menu=photo_menu)
        photo_menu.add_command(label="Grey", command=pixel_exchange_grey_wrapper)
        photo_menu.add_command(label="Color", command=pixel_exchange_color_wrapper)
        pixel_exchange.add_command(label="Video", command=pixel_exchange_video_wrapper)


