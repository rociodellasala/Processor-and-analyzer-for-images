from tkinter import Menu, messagebox, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from image_access import open_file_name
from image_access import read_raw_image
from src.GUI import gui_constants as constants
from src.GUI.image_menu import load_image
from src.GUI.interface_info import InterfaceInfo
from image_operations import add_grey_images
from image_operations import subtract_colored_images
from image_operations import subtract_grey_images


def load_left_image(interface):
    loaded_image = load_image(0, 0)
    if loaded_image is not None:
        interface.left_image = loaded_image


def load_right_image(interface):
    loaded_image = load_image(0, 1)
    if loaded_image is not None:
        interface.right_image = loaded_image


def generate_binary_operations_input(interface):
    if interface.current_image is not None or interface.image_to_copy is not None:
        interface.reset_parameters()
    else:
        interface.delete_widgets(interface.buttons_frame)
    image_1_button = ttk.Button(interface.buttons_frame, text="Load Image 1",
                                command=lambda: load_left_image(interface))
    image_2_button = ttk.Button(interface.buttons_frame, text="Load Image 2",
                                command=lambda: load_right_image(interface))
    image_1_button.grid(row=0, column=0)
    image_2_button.grid(row=0, column=1)


def binary_operation_validator(image_1, image_2):
    if image_1 is None or image_2 is None:
        return False
    else:
        return True


def generate_add_operation_input():
    interface = InterfaceInfo.get_instance()
    generate_binary_operations_input(interface)
    add_button = ttk.Button(interface.buttons_frame, text="Add",
                            command=lambda: add_grey_image_wrapper(constants.WIDTH, constants.HEIGHT,
                                                                   interface.left_image, constants.WIDTH,
                                                                   constants.HEIGHT, interface.right_image))
    add_button.grid(row=1, column=0)


def add_grey_image_wrapper(width_1, height_1, image_1, width_2, height_2, image_2):
    if binary_operation_validator(image_1, image_2):
        add_grey_images(width_1, height_1, image_1, width_2, height_2, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to add")


def generate_subtract_colored_operation_input():
    interface = InterfaceInfo.get_instance()
    generate_binary_operations_input(interface)
    subtract_button = ttk.Button(interface.buttons_frame, text="Subtract",
                                 command=lambda: subtract_colored_image_wrapper(constants.WIDTH, constants.HEIGHT,
                                                                                interface.left_image,
                                                                                interface.right_image))
    subtract_button.grid(row=1, column=0)


def subtract_colored_image_wrapper(width, height, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        subtract_colored_images(width, height, image_1, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to subtract")


def generate_subtract_grey_operation_input():
    interface = InterfaceInfo.get_instance()
    generate_binary_operations_input(interface)
    subtract_button = ttk.Button(interface.buttons_frame, text="Subtract",
                                 command=lambda: subtract_grey_image_wrapper(constants.WIDTH, constants.HEIGHT,
                                                                             interface.left_image,
                                                                             interface.right_image))
    subtract_button.grid(row=1, column=0)


def subtract_grey_image_wrapper(width, height, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        subtract_grey_images(width, height, image_1, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to subtract")


class OperationsMenu:
    def __init__(self, menubar):
        operation_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Operations", menu=operation_menu)
        operation_menu.add_command(label="Add", command=generate_add_operation_input)
        subtract_menu = Menu(operation_menu, tearoff=0)
        operation_menu.add_cascade(label="Subtract", menu=subtract_menu)
        subtract_menu.add_command(label="Color", command=generate_subtract_colored_operation_input)
        subtract_menu.add_command(label="B&W", command=generate_subtract_grey_operation_input)
        # multiply_menu = Menu(operation_menu, tearoff=0)
        # operation_menu.add_cascade(label="Multiply", menu=multiply_menu)
        # multiply_menu.add_command(label="By scalar", command=generate_multiply_by_scalar_input)
        # multiply_menu.add_command(label="Two images", command=generate_multiply_images_operation_input)
        # operation_menu.add_command(label="Copy", command=generate_copy_sub_image_input)
        # negative_menu = Menu(operation_menu, tearoff=0)
        # operation_menu.add_cascade(label="Negative", menu=negative_menu)
        # negative_menu.add_command(label="Colored Negative", command=lambda:
        #                           colored_negative_wrapper(current_image, WIDTH, HEIGHT))
        # negative_menu.add_command(label="Grey Negative", command=lambda:
        #                           grey_negative_wrapper(current_image, WIDTH, HEIGHT))
