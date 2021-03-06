from tkinter import Menu, Entry, messagebox, ttk, Radiobutton, StringVar, IntVar, BooleanVar
from src.GUI.image_menu import load_image
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from border_detectors import prewit_detection, sobel_detection, \
    prewit_color_detection, sobel_color_detection
from filters import border_enhancement_filter
from border_detectors import laplacian_method, laplacian_method_with_slope_evaluation,\
    laplacian_gaussian_method, four_direction_border_detection, canny_method, susan_method, colored_canny_method, \
    compare_images, harris_method


def load_left_image(interface):
    loaded_image = load_image(0, 0)
    if loaded_image is not None:
        interface.left_image = loaded_image


def load_right_image(interface):
    loaded_image = load_image(0, 1)
    if loaded_image is not None:
        interface.right_image = loaded_image


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
        messagebox.showerror(title="Error", message="You must upload an image to apply laplacian")


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
        messagebox.showerror(title="Error", message="You must upload an image to apply laplacian gaussian")


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
        messagebox.showerror(title="Error", message="You must upload an image to apply laplacian with slope")


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


def generate_sift_method_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None or interface.image_to_copy is not None or interface.left_image is not None\
            or interface.right_image is not None:
        interface.reset_parameters()
    generate_sift_method_input(interface)


def generate_colored_sift_method_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None or interface.image_to_copy is not None or interface.left_image is not None\
            or interface.right_image is not None:
        interface.reset_parameters()
    generate_colored_sift_method_input(interface)


def generate_sift_method_input(interface):
    interface.delete_widgets(interface.buttons_frame)
    image_1_button = ttk.Button(interface.buttons_frame, text="Load Image 1",
                                    command=lambda: load_left_image(interface))
    image_2_button = ttk.Button(interface.buttons_frame, text="Load Image 2",
                                    command=lambda: load_right_image(interface))
    image_1_button.grid(row=0, column=2, padx=3, pady=3)
    image_2_button.grid(row=0, column=3, padx=3, pady=3)
    ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
    threshold = Entry(interface.buttons_frame)
    threshold.grid(row=0, column=1)
    ttk.Label(interface.buttons_frame, text="Acceptance percentage", background=constants.TOP_COLOR).grid(row=1,column=0)
    acceptance = Entry(interface.buttons_frame)
    acceptance.grid(row=1, column=1)
    add_button = ttk.Button(interface.buttons_frame, text="Compare",
                            command=lambda: call_sift_method(interface, threshold, acceptance))
    add_button.grid(row=2, column=0, padx=3, pady=3)


def call_sift_method(interface, threshold, acceptance):
    if interface.left_image is not None and interface.right_image is not None:
        are_equals = compare_images(interface.left_image, constants.HEIGHT,
                       constants.WIDTH, interface.right_image,
                       constants.HEIGHT, constants.WIDTH, int(threshold.get()), float(acceptance.get()), is_colored=False)
        ttk.Label(interface.buttons_frame, text="Are images equal?:",
                  background=constants.TOP_COLOR).grid(row=0, column=4)
        if are_equals is True:
            ttk.Label(interface.buttons_frame, text="Yes",
                      background=constants.TOP_COLOR).grid(row=0, column=5)
        else:
            ttk.Label(interface.buttons_frame, text="No",
                      background=constants.TOP_COLOR).grid(row=0, column=5)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload two images to apply sift method")


def generate_colored_sift_method_input(interface):
    interface.delete_widgets(interface.buttons_frame)
    image_1_button = ttk.Button(interface.buttons_frame, text="Load Image 1",
                                    command=lambda: load_left_image(interface))
    image_2_button = ttk.Button(interface.buttons_frame, text="Load Image 2",
                                    command=lambda: load_right_image(interface))
    image_1_button.grid(row=0, column=2, padx=3, pady=3)
    image_2_button.grid(row=0, column=3, padx=3, pady=3)
    ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
    threshold = Entry(interface.buttons_frame)
    threshold.grid(row=0, column=1)
    ttk.Label(interface.buttons_frame, text="Acceptance percentage", background=constants.TOP_COLOR).grid(row=1, column=0)
    acceptance = Entry(interface.buttons_frame)
    acceptance.grid(row=1, column=1)
    add_button = ttk.Button(interface.buttons_frame, text="Compare",
                            command=lambda: call_colored_sift_method(interface, threshold, acceptance))
    add_button.grid(row=2, column=0, padx=3, pady=3)


def call_colored_sift_method(interface, threshold, acceptance):
    if interface.left_image is not None and interface.right_image is not None:
        are_equals = compare_images(interface.left_image, constants.HEIGHT,
                       constants.WIDTH, interface.right_image,
                       constants.HEIGHT, constants.WIDTH, int(threshold.get()), float(acceptance.get()), is_colored=True)
        ttk.Label(interface.buttons_frame, text="Are images equal?:",
                  background=constants.TOP_COLOR).grid(row=0, column=4)
        if are_equals is True:
            ttk.Label(interface.buttons_frame, text="Yes",
                      background=constants.TOP_COLOR).grid(row=0, column=5)
        else:
            ttk.Label(interface.buttons_frame, text="No",
                      background=constants.TOP_COLOR).grid(row=0, column=5)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload two images to apply sift method")


def generate_colored_harris_method_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
        threshold = Entry(interface.buttons_frame)
        threshold.grid(row=0, column=1)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: harris_method(interface.current_image, constants.HEIGHT,
                                                                constants.WIDTH, float(threshold.get()), True))
        apply_filter.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply harris method")


def generate_harris_method_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Threshold", background=constants.TOP_COLOR).grid(row=0, column=0)
        threshold = Entry(interface.buttons_frame)
        threshold.grid(row=0, column=1)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: harris_method(interface.current_image, constants.HEIGHT,
                                                                constants.WIDTH, float(threshold.get()), False))
        apply_filter.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply harris method")


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
        sift_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Sift Comparison", menu=sift_menu)
        sift_menu.add_command(label="Grey", command=generate_sift_method_wrapper)
        sift_menu.add_command(label="Color", command=generate_colored_sift_method_wrapper)
        harris_menu = Menu(border_detection_menu, tearoff=0)
        border_detection_menu.add_cascade(label="Harris", menu=harris_menu)
        harris_menu.add_command(label="Grey", command=generate_harris_method_input)
        harris_menu.add_command(label="Color", command=generate_colored_harris_method_input)
