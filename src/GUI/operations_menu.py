from tkinter import Menu, messagebox, ttk, Entry
from src.GUI import gui_constants as constants
from src.GUI.image_menu import load_image
from src.GUI.interface_info import InterfaceInfo
from image_operations import add_grey_images
from image_operations import subtract_colored_images
from image_operations import subtract_grey_images
from image_operations import multiply_grey_images_with_scalar
from image_operations import multiply_grey_images
from image_operations import copy_pixels
from image_operations import grey_image_negative
from image_operations import colored_image_negative


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


def generate_multiply_by_scalar_input():
    interface = InterfaceInfo.get_instance()
    interface.reset_parameters()
    load_image_button = ttk.Button(interface.buttons_frame, text="Load Image",
                                   command=lambda: load_left_image(interface))
    load_image_button.grid(row=0, column=0)
    ttk.Label(interface.buttons_frame, text="Scalar", background=constants.TOP_COLOR).grid(row=1, column=0)
    scalar = Entry(interface.buttons_frame)
    scalar.grid(row=1, column=1)
    multiply_button = ttk.Button(interface.buttons_frame, text="Multiply",
                                 command=lambda: multiply_grey_images_with_scalar_wrapper(constants.WIDTH,
                                                                                          constants.HEIGHT,
                                                                                          interface.left_image,
                                                                                          scalar.get()))
    multiply_button.grid(row=2, column=0)


def multiply_grey_images_with_scalar_wrapper(width, height, image, scalar):
    error = False
    try:
        scalar_value = float(scalar)
    except ValueError:
        error = True
        messagebox.showerror(title="Error", message="You need to insert a valid scalar to multiply")
    if (not error) and image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to multiply")
    elif not error:
        multiply_grey_images_with_scalar(width, height, image, scalar_value)


def generate_multiply_images_operation_input():
    interface = InterfaceInfo.get_instance()
    generate_binary_operations_input(interface)
    multiply_button = ttk.Button(interface.buttons_frame, text="Multiply",
                                 command=lambda: multiply_grey_images_wrapper(constants.WIDTH, constants.HEIGHT,
                                                                              interface.left_image, constants.WIDTH,
                                                                              constants.HEIGHT, interface.right_image))
    multiply_button.grid(row=1, column=0)


def multiply_grey_images_wrapper(width_1, height_1, image_1, width_2, height_2, image_2):
    if binary_operation_validator(image_1, image_2):
        multiply_grey_images(width_1, height_1, image_1, width_2, height_2, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to multiply")


def generate_copy_sub_image_input():
    interface = InterfaceInfo.get_instance()
    generate_binary_operations_input(interface)
    ttk.Label(interface.buttons_frame, text="Original image", background=constants.TOP_COLOR).grid(row=1, column=0)
    ttk.Label(interface.buttons_frame, text="X", background=constants.TOP_COLOR).grid(row=2, column=0)
    ttk.Label(interface.buttons_frame, text="Y", background=constants.TOP_COLOR).grid(row=3, column=0)
    ttk.Label(interface.buttons_frame, text="Width", background=constants.TOP_COLOR).grid(row=2, column=2)
    ttk.Label(interface.buttons_frame, text="Height", background=constants.TOP_COLOR).grid(row=3, column=2)
    ttk.Label(interface.buttons_frame, text="Image to copy", background=constants.TOP_COLOR).grid(row=1, column=4)
    ttk.Label(interface.buttons_frame, text="X", background=constants.TOP_COLOR).grid(row=2, column=4)
    ttk.Label(interface.buttons_frame, text="Y", background=constants.TOP_COLOR).grid(row=3, column=4)
    x_original = Entry(interface.buttons_frame)
    y_original = Entry(interface.buttons_frame)
    width_original = Entry(interface.buttons_frame)
    height_original = Entry(interface.buttons_frame)
    x_copy = Entry(interface.buttons_frame)
    y_copy = Entry(interface.buttons_frame)
    x_original.grid(row=2, column=1)
    y_original.grid(row=3, column=1)
    width_original.grid(row=2, column=3)
    height_original.grid(row=3, column=3)
    x_copy.grid(row=2, column=5)
    y_copy.grid(row=3, column=5)
    modify_pixel_button = ttk.Button(interface.buttons_frame, text="Copy",
                                     command=lambda: copy_pixels_wrapper(int(x_original.get()),
                                                                 int(y_original.get()),int(width_original.get()),
                                                                 int(height_original.get()), int(x_copy.get()) - 1,
                                                                 int(y_copy.get()),interface.left_image,
                                                                 interface.right_image))
    #TODO validate cast
    modify_pixel_button.grid(row=4, column=0)


def copy_pixels_wrapper(x_original, y_original, width_original, height_original, x_copy, y_copy, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        copy_pixels(x_original, y_original, width_original, height_original, x_copy, y_copy, image_1, image_2,
                    constants.WIDTH, constants.HEIGHT)
    else:
        messagebox.showerror(title="Error", message="You must upload two images to copy one into another")


def grey_negative_wrapper(image, width, height):
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to get its negative")
    else:
        grey_image_negative(image, width, height)


def colored_negative_wrapper(image, width, height):
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to get its negative")
    else:
        colored_image_negative(image, width, height)


class OperationsMenu:
    def __init__(self, menubar):
        interface = InterfaceInfo.get_instance()
        operation_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Operations", menu=operation_menu)
        operation_menu.add_command(label="Add", command=generate_add_operation_input)
        subtract_menu = Menu(operation_menu, tearoff=0)
        operation_menu.add_cascade(label="Subtract", menu=subtract_menu)
        subtract_menu.add_command(label="Color", command=generate_subtract_colored_operation_input)
        subtract_menu.add_command(label="B&W", command=generate_subtract_grey_operation_input)
        multiply_menu = Menu(operation_menu, tearoff=0)
        operation_menu.add_cascade(label="Multiply", menu=multiply_menu)
        multiply_menu.add_command(label="By scalar", command=generate_multiply_by_scalar_input)
        multiply_menu.add_command(label="Two images", command=generate_multiply_images_operation_input)
        operation_menu.add_command(label="Copy", command=generate_copy_sub_image_input)
        negative_menu = Menu(operation_menu, tearoff=0)
        operation_menu.add_cascade(label="Negative", menu=negative_menu)
        negative_menu.add_command(label="Colored Negative", command=lambda:
                                  colored_negative_wrapper(interface.current_image, constants.WIDTH, constants.HEIGHT))
        negative_menu.add_command(label="Grey Negative", command=lambda:
                                  grey_negative_wrapper(interface.current_image, constants.WIDTH, constants.HEIGHT))
