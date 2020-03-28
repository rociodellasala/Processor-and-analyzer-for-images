# TODO remove extras
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
import numpy as np
from read_raw_image import read_raw_image
from image_generator import generate_circle
from image_generator import gray_faded_image
from image_generator import color_faded_image
from image_operations import subtract_grey_images
from image_operations import subtract_colored_images
from image_operations import multiply_grey_images_with_scalar
from image_operations import multiply_grey_images
from image_operations import dynamic_range_compression
from image_operations import grey_image_negative
from image_operations import grey_level_histogram
from image_operations import colored_image_negative
from image_operations import gamma_pow_function
from image_operations import image_threshold
from image_operations import image_equalization
from noise_generators import gaussian_noise_generator
from noise_generators import rayleigh_noise_generator
from noise_generators import exponential_noise_generator
from noise_generators import salt_and_pepper_noise_generator
from filters import media_filter
from filters import weighted_median_filter
from filters import median_filter
from filters import gaussian_filter
from filters import border_enhancement_filter
from src.GUI import gui_constants as color
from tkinter import ttk

from src.GUI.draw_menu import DrawMenu
from src.GUI.image_menu import ImageMenu
from src.GUI.interface_info import InterfaceInfo
from src.GUI.operations_menu import OperationsMenu
from src.GUI.pixel_menu import PixelMenu

WIDTH = 512
HEIGHT = 512

# def load_image(row, column):
#     file_name = open_file_name()
#     if file_name:
#         if file_name.endswith(".RAW"):
#             raw_image = read_raw_image(file_name)
#             image = Image.frombytes('L', (int(raw_image[1][0]), int(raw_image[1][1])), raw_image[0])
#         else:
#             # opens the image
#             image = Image.open(file_name)
#         # resize the image and apply a high-quality down sampling filter
#         image = image.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
#         image_instance = image
#         # PhotoImage class is used to add image to widgets, icons etc
#         image = ImageTk.PhotoImage(image)
#         # create a label
#         panel = ttk.Label(image_frame, image=image)
#         # set the image as img
#         panel.image = image
#         panel.grid(row=row, column=column)
#         return image_instance


# def load_image_wrapper():
#     remove_images()
#     global current_image, image_to_copy
#     if current_image is None:
#         current_image = load_image(0, 0)
#     elif image_to_copy is None:
#         image_to_copy = load_image(0, 1)
#     else:
#         messagebox.showerror(title="Error", message="You can't upload more than two images. If you want to change"
#                                                     " one click on the \"Clean image\" button first")







def create_image_menu(menubar):
    image_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Image", menu=image_menu)

    image_menu.add_command(label="Open")
    image_menu.add_command(label="Save")
    image_menu.add_separator()
    image_menu.add_command(label="Exit")
    # image_menu.add_command(label="Open", command=load_image_wrapper)
    # image_menu.add_command(label="Save", command=save_image)
    # image_menu.add_separator()
    # image_menu.add_command(label="Exit", command=root.quit)


def create_gradient_menu(menubar):
    gradient_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Gradient", menu=gradient_menu)

    gradient_menu.add_command(label="Gray")
    gradient_menu.add_command(label="Color")
    # gradient_menu.add_command(label="Gray", command=generate_gray_fading_input)
    # gradient_menu.add_command(label="Color", command=generate_color_fading_input)


def create_function_menu(menubar):
    function_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Function", menu=function_menu)

    function_menu.add_command(label="Gamma")
    function_menu.add_command(label="Dynamic Range Compression")
    function_menu.add_command(label="Threshold")
    function_menu.add_command(label="Equalization")
    function_menu.add_command(label="Grey Histogram")
    # function_menu.add_command(label="Gamma", command=generate_gamma_input)
    # function_menu.add_command(label="Dynamic Range Compression", command=generate_range_compression_input)
    # function_menu.add_command(label="Threshold", command=generate_image_threshold_input)
    # function_menu.add_command(label="Equalization", command=lambda:
    #                         equalized_image_wrapper(current_image, WIDTH, HEIGHT))
    # function_menu.add_command(label="Grey Histogram", command=lambda:
    #                           grey_level_histogram_wrapper(current_image, WIDTH, HEIGHT))




def create_filters_menu(menubar):
    filters_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Filters", menu=filters_menu)

    filters_menu.add_command(label="Media")
    filters_menu.add_command(label="Median")
    filters_menu.add_command(label="Weighted median")
    filters_menu.add_command(label="Gaussian")
    filters_menu.add_command(label="Border enhancement")
    # filters_menu.add_command(label="Media", command=generate_media_filter_input)
    # filters_menu.add_command(label="Median", command=generate_median_filter_input)
    # filters_menu.add_command(label="Weighted median", command=lambda:
    #                          weighted_median_wrapper(current_image, WIDTH, HEIGHT))
    # filters_menu.add_command(label="Gaussian", command=generate_gaussian_filter_input)
    # filters_menu.add_command(label="Border enhancement", command=lambda:
    #                          border_enhancement_filter_wrapper(current_image, WIDTH, HEIGHT))


def create_noise_menu(menubar):
    noise_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Noise", menu=noise_menu)

    noise_menu.add_command(label="Gaussian")
    noise_menu.add_command(label="Rayleigh")
    noise_menu.add_command(label="Exponential")
    noise_menu.add_command(label="Salt and Pepper")
    # noise_menu.add_command(label="Gaussian", command=generate_gaussian_noise_input)
    # noise_menu.add_command(label="Rayleigh", command=generate_rayleigh_noise_input)
    # noise_menu.add_command(label="Exponential", command=generate_exponential_noise_input)
    # noise_menu.add_command(label="Salt and Pepper", command=generate_salt_and_pepper_noise_input)


# def generate_gray_fading_input():
#     clean_images()
#     delete_widgets(buttons_frame)
#     delete_widgets(image_frame)
#     ttk.Label(buttons_frame, text="Image width", background=color.TOP_COLOR).grid(row=0, column=0)
#     ttk.Label(buttons_frame, text="Image height", background=color.TOP_COLOR).grid(row=1, column=0)
#     image_width = Entry(buttons_frame)
#     image_height = Entry(buttons_frame)
#     image_width.grid(row=0, column=1)
#     image_height.grid(row=1, column=1)
#     generate_gray_fading_button = ttk.Button(buttons_frame, text="Show", command=lambda:
#     gray_faded_image(int(image_width.get()), int(image_height.get())))
#     generate_gray_fading_button.grid(row=3, column=0)


# def generate_color_fading_input():
#     clean_images()
#     delete_widgets(buttons_frame)
#     delete_widgets(image_frame)
#     ttk.Label(buttons_frame, text="Image width", background=color.TOP_COLOR).grid(row=0, column=0)
#     ttk.Label(buttons_frame, text="Image height", background=color.TOP_COLOR).grid(row=1, column=0)
#     red = BooleanVar()
#     green = BooleanVar()
#     blue = BooleanVar()
#     Checkbutton(buttons_frame, text="Red", variable=red, background=color.TOP_COLOR).grid(row=2, column=0)
#     Checkbutton(buttons_frame, text="Green", variable=green, background=color.TOP_COLOR).grid(row=2, column=1)
#     Checkbutton(buttons_frame, text="Blue", variable=blue, background=color.TOP_COLOR).grid(row=2, column=2)
#     image_width = Entry(buttons_frame)
#     image_height = Entry(buttons_frame)
#     image_width.grid(row=0, column=1)
#     image_height.grid(row=1, column=1)
#     generate_gray_fading_button = ttk.Button(buttons_frame, text="Show",
#                                          command=lambda: color_faded_image(int(image_width.get()),
#                                                                            int(image_height.get()),
#                                                                            red.get(), green.get(),
#                                                                            blue.get()))
#     generate_gray_fading_button.grid(row=3, column=0)


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


# def generate_gamma_input():
#     delete_widgets(buttons_frame)
#     if current_image is not None:
#         ttk.Label(buttons_frame, text="Gamma", background=color.TOP_COLOR).grid(row=0, column=0)
#         gamma = Entry(buttons_frame)
#         gamma.grid(row=0, column=1)
#         apply_button = ttk.Button(buttons_frame, text="Apply",
#                               command=lambda: gamma_pow_function_wrapper(current_image, WIDTH, HEIGHT, gamma.get()))
#         apply_button.grid(row=1, column=0)
#     else:
#         messagebox.showerror(title="Error", message="You must upload an image to apply gamma")


# def generate_range_compression_input():
#     delete_widgets(buttons_frame)
#     if current_image is not None:
#         dynamic_range_compression(current_image, WIDTH, HEIGHT)
#     else:
#         messagebox.showerror(title="Error", message="You must upload an image to generate range compression")


# def generate_copy_sub_image_input():
#     generate_binary_operations_input()
#     ttk.Label(buttons_frame, text="Original image", background=color.TOP_COLOR).grid(row=1, column=0)
#     ttk.Label(buttons_frame, text="X", background=color.TOP_COLOR).grid(row=2, column=0)
#     ttk.Label(buttons_frame, text="Y", background=color.TOP_COLOR).grid(row=3, column=0)
#     ttk.Label(buttons_frame, text="Width", background=color.TOP_COLOR).grid(row=2, column=2)
#     ttk.Label(buttons_frame, text="Height", background=color.TOP_COLOR).grid(row=3, column=2)
#     ttk.Label(buttons_frame, text="Image to copy", background=color.TOP_COLOR).grid(row=1, column=4)
#     ttk.Label(buttons_frame, text="X", background=color.TOP_COLOR).grid(row=2, column=4)
#     ttk.Label(buttons_frame, text="Y", background=color.TOP_COLOR).grid(row=3, column=4)
#     x_original = Entry(buttons_frame)
#     y_original = Entry(buttons_frame)
#     width_original = Entry(buttons_frame)
#     height_original = Entry(buttons_frame)
#     x_copy = Entry(buttons_frame)
#     y_copy = Entry(buttons_frame)
#     x_original.grid(row=2, column=1)
#     y_original.grid(row=3, column=1)
#     width_original.grid(row=2, column=3)
#     height_original.grid(row=3, column=3)
#     x_copy.grid(row=2, column=5)
#     y_copy.grid(row=3, column=5)
#     modify_pixel_button = ttk.Button(buttons_frame, text="Copy",
#                                  command=lambda: copy_pixels(int(x_original.get()),
#                                                              int(y_original.get()),
#                                                              int(width_original.get()), int(height_original.get()),
#                                                              int(x_copy.get()) - 1, int(y_copy.get()),
#                                                              left_image, right_image))
#     #TODO validate cast
#     modify_pixel_button.grid(row=4, column=0)


def copy_pixels(x_original, y_original, width_original, height_original, x_copy, y_copy, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        pixels = image_1.load()
        copy = image_2.load()
        new_image = np.zeros((WIDTH, HEIGHT))
        for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                new_image[y, x] = pixels[x, y]
        y_copy_aux = y_copy
        for x in range(x_original, x_original + width_original):
            x_copy += 1
            y_copy = y_copy_aux
            for y in range(y_original, y_original + height_original):
                if x < 512 and y < 512 and x_copy < 512 and y_copy < 512:
                    new_image[y, x] = copy[x_copy, y_copy]
                    y_copy += 1
        save_grey_image(new_image, save_generated_path + "copy_image.ppm")
        img = Image.fromarray(new_image)
        img.show()
    else:
        messagebox.showerror(title="Error", message="You must upload two images to copy one into another")


def save_grey_image(image, file_path):
    img = Image.fromarray(image)
    img = img.convert("I")
    img.save(file_path)


def subtract_grey_image_wrapper(width, height, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        subtract_grey_images(width, height, image_1, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to subtract")


# def generate_subtract_grey_operation_input():
#     generate_binary_operations_input()
#     subtract_button = ttk.Button(buttons_frame, text="Subtract",
#                                  command=lambda: subtract_grey_image_wrapper(WIDTH, HEIGHT, left_image, right_image))
#     subtract_button.grid(row=1, column=0)


def subtract_colored_image_wrapper(width, height, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        subtract_colored_images(width, height, image_1, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to subtract")


def generate_subtract_colored_operation_input():
    generate_binary_operations_input()
    subtract_button = ttk.Button(buttons_frame, text="Subtract",
                             command=lambda: subtract_colored_image_wrapper(WIDTH, HEIGHT, left_image, right_image))
    subtract_button.grid(row=1, column=0)


def multiply_grey_images_wrapper(width_1, height_1, image_1, width_2, height_2, image_2):
    if binary_operation_validator(image_1, image_2):
        multiply_grey_images(width_1, height_1, image_1, width_2, height_2, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to multiply")


# def generate_multiply_images_operation_input():
#     generate_binary_operations_input()
#     multiply_button = ttk.Button(buttons_frame, text="Multiply",
#                              command=lambda: multiply_grey_images_wrapper(WIDTH, HEIGHT, left_image, WIDTH, HEIGHT, right_image))
#     multiply_button.grid(row=1, column=0)


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


# def generate_multiply_by_scalar_input():
#     reset_parameters()
#     load_image_button = ttk.Button(buttons_frame, text="Load Image",
#                                    command=load_left_image).grid(row=0, column=0)
#     ttk.Label(buttons_frame, text="Scalar", background=color.TOP_COLOR).grid(row=1, column=0)
#     scalar = Entry(buttons_frame)
#     scalar.grid(row=1, column=1)
#     multiply_button = ttk.Button(buttons_frame, text="Multiply",
#                              command=lambda: multiply_grey_images_with_scalar_wrapper(WIDTH, HEIGHT, left_image,
#                                                                                       scalar.get()))
#     multiply_button.grid(row=2, column=0)


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


# def generate_image_threshold_input():
#     delete_widgets(buttons_frame)
#     if current_image is not None:
#         ttk.Label(buttons_frame, text="Threshold", background=color.TOP_COLOR).grid(row=0, column=0)
#         threshold = Entry(buttons_frame)
#         threshold.grid(row=0, column=1)
#         apply_threshold = ttk.Button(buttons_frame, text="Apply",
#                                  command=lambda: image_threshold(current_image, WIDTH, HEIGHT, float(threshold.get())))
#         apply_threshold.grid(row=1, column=0)
#     else:
#         messagebox.showerror(title="Error", message="You must upload an image to apply a threshold")


# def equalized_image_wrapper(image, width, height):
#     if image is not None:
#         delete_widgets(buttons_frame)
#         image_equalization(image, width, height)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to get the equalized histogram")


def grey_level_histogram_wrapper(image, width, height):
    if image is not None:
        delete_widgets(buttons_frame)
        grey_level_histogram(image, width, height)
    else:
        reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to get the equalized histogram")


# def generate_gaussian_noise_input():
#     if current_image is not None:
#         delete_widgets(buttons_frame)
#         ttk.Label(buttons_frame, text="Percentage", background=color.TOP_COLOR).grid(row=0, column=3)
#         ttk.Label(buttons_frame, text="Mu", background=color.TOP_COLOR).grid(row=0, column=0)
#         ttk.Label(buttons_frame, text="Sigma", background=color.TOP_COLOR).grid(row=1, column=0)
#         percentage = Entry(buttons_frame)
#         mu = Entry(buttons_frame)
#         sigma = Entry(buttons_frame)
#         percentage.grid(row=0, column=4)
#         mu.grid(row=0, column=2)
#         sigma.grid(row=1, column=2)
#         radio_var = BooleanVar()
#         radio_var.set(True)
#         Radiobutton(buttons_frame, text="Additive", value=True,
#                     variable=radio_var, background=color.TOP_COLOR).grid(row=0, column=5)
#         Radiobutton(buttons_frame, text="Multiplicative", value=False,
#                     variable=radio_var, background=color.TOP_COLOR).grid(row=1, column=5)
#         generate_noise = ttk.Button(buttons_frame, text="Generate",
#                                 command=lambda: gaussian_noise_generator(float(percentage.get()), radio_var.get(),
#                                                                          current_image, WIDTH, HEIGHT, int(mu.get()),
#                                                                          float(sigma.get())))
#         generate_noise.grid(row=2, column=0)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to generate gaussian noise")


# def generate_rayleigh_noise_input():
#     if current_image is not None:
#         delete_widgets(buttons_frame)
#         ttk.Label(buttons_frame, text="Percentage", background=color.TOP_COLOR).grid(row=0, column=0)
#         ttk.Label(buttons_frame, text="Xi", background=color.TOP_COLOR).grid(row=1, column=0)
#         percentage = Entry(buttons_frame)
#         xi = Entry(buttons_frame)
#         percentage.grid(row=0, column=1)
#         xi.grid(row=1, column=1)
#         radio_var = BooleanVar()
#         radio_var.set(True)
#         Radiobutton(buttons_frame, text="Additive", value=True,
#                     variable=radio_var, background=color.TOP_COLOR).grid(row=0, column=2)
#         Radiobutton(buttons_frame, text="Multiplicative", value=False,
#                     variable=radio_var, background=color.TOP_COLOR).grid(row=1, column=2)
#         generate_noise = ttk.Button(buttons_frame, text="Generate",
#                                 command=lambda: rayleigh_noise_generator(float(percentage.get()), radio_var.get(),
#                                                                          current_image, WIDTH, HEIGHT, float(xi.get())))
#         generate_noise.grid(row=2, column=0)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to generate rayleigh noise")


# def generate_exponential_noise_input():
#     if current_image is not None:
#         delete_widgets(buttons_frame)
#         ttk.Label(buttons_frame, text="Percentage", background=color.TOP_COLOR).grid(row=0, column=0)
#         ttk.Label(buttons_frame, text="Lambda", background=color.TOP_COLOR).grid(row=1, column=0)
#         percentage = Entry(buttons_frame)
#         lambda_value = Entry(buttons_frame)
#         percentage.grid(row=0, column=1)
#         lambda_value.grid(row=1, column=1)
#         radio_var = BooleanVar()
#         radio_var.set(True)
#         Radiobutton(buttons_frame, text="Additive",
#                     value=True, variable=radio_var, background=color.TOP_COLOR).grid(row=0, column=2)
#         Radiobutton(buttons_frame, text="Multiplicative",
#                     value=False, variable=radio_var, background=color.TOP_COLOR).grid(row=1, column=2)
#         generate_noise = ttk.Button(buttons_frame, text="Generate",
#                                 command=lambda: exponential_noise_generator(float(percentage.get()), radio_var.get(),
#                                                                             current_image, WIDTH, HEIGHT,
#                                                                             float(lambda_value.get())))
#         generate_noise.grid(row=2, column=0)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to generate exponential noise")


# def generate_salt_and_pepper_noise_input():
#     if current_image is not None:
#         delete_widgets(buttons_frame)
#         ttk.Label(buttons_frame, text="Density", background=color.TOP_COLOR).grid(row=0, column=0)
#         density = Entry(buttons_frame)
#         density.grid(row=0, column=1)
#         generate_salt_and_pepper = ttk.Button(buttons_frame, text="Generate",
#                                           command=lambda: salt_and_pepper_noise_generator(current_image, WIDTH, HEIGHT,
#                                                                                           float(density.get())))
#         generate_salt_and_pepper.grid(row=1, column=0)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to generate salt and pepper noise")


# def generate_media_filter_input():
#     if current_image is not None:
#         delete_widgets(buttons_frame)
#         ttk.Label(buttons_frame, text="Windows size", background=color.TOP_COLOR).grid(row=0, column=0)
#         windows_size = Entry(buttons_frame)
#         windows_size.grid(row=0, column=1)
#         generate_noise = ttk.Button(buttons_frame, text="Apply",
#                                 command=lambda: media_filter(current_image, WIDTH, HEIGHT, int(windows_size.get())))
#         generate_noise.grid(row=1, column=0)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to apply media filter")


# def generate_median_filter_input():
#     if current_image is not None:
#         delete_widgets(buttons_frame)
#         ttk.Label(buttons_frame, text="Windows size", background=color.TOP_COLOR).grid(row=0, column=0)
#         windows_size = Entry(buttons_frame)
#         windows_size.grid(row=0, column=1)
#         generate_noise = ttk.Button(buttons_frame, text="Apply",
#                                 command=lambda: median_filter(current_image, WIDTH, HEIGHT, int(windows_size.get())))
#         generate_noise.grid(row=1, column=0)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to apply median filter ")


def weighted_median_wrapper(image, width, height):
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to apply weighted median filter ")
    else:
        weighted_median_filter(image, width, height, 3)


# def generate_gaussian_filter_input():
#     if current_image is not None:
#         delete_widgets(buttons_frame)
#         ttk.Label(buttons_frame, text="Sigma", background=color.TOP_COLOR).grid(row=0, column=0)
#         sigma = Entry(buttons_frame)
#         sigma.grid(row=0, column=1)
#         generate_noise = ttk.Button(buttons_frame, text="Apply",
#                                 command=lambda: gaussian_filter(current_image, WIDTH, HEIGHT, int(sigma.get())))
#         generate_noise.grid(row=1, column=0)
#     else:
#         reset_parameters()
#         messagebox.showerror(title="Error", message="You must upload an image to apply gaussian filter ")


def border_enhancement_filter_wrapper(image, width, height):
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to get its negative")
    else:
        border_enhancement_filter(image, width, height)





# root = Tk()
# # can only resize height
# root.style = ttk.Style()
# #('clam', 'alt', 'default', 'classic')
# root.style.theme_use("clam")
# ttk.Style().configure("Label", background=color.TOP_COLOR)
#
# root.resizable(False, True)
# root.title('ATI interface')
# root.state('zoomed')
#
# current_image = None
# image_to_copy = None
# left_image = None
# right_image = None
#
# buttons_frame = None
# image_frame = None
# footer_frame = None
#
# load_frames()
# load_menu()
#########################################################################################################################
class App:
    def __init__(self):
        interface = InterfaceInfo.get_instance()
        root = interface.get_root()
        interface.configure()
        interface.load_frames()
        self.load_footer_buttons(interface)
        self.load_menu(root)

    def load_footer_buttons(self, interface):
        exit_program_btn = ttk.Button(interface.footer_frame, text="Exit Program",
                                      command= lambda: self.ask_quit(root))
        exit_program_btn.grid(column=0, row=0)
        clean_window_btn = ttk.Button(interface.footer_frame, text="Clean buttons",
                                      command=lambda: interface.delete_widgets(interface.buttons_frame))
        clean_window_btn.grid(column=1, row=0)
        clean_window_btn = ttk.Button(interface.footer_frame, text="Clean image",
                                      command=lambda: interface.delete_widgets(interface.image_frame))
        clean_window_btn.grid(column=2, row=0)

    def ask_quit(self, root):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            root.destroy()

    def load_menu(self, root):
        menubar = Menu(root)
        root.config(menu=menubar)
        ImageMenu(menubar)
        PixelMenu(menubar)
        DrawMenu(menubar)
        OperationsMenu(menubar)
        # create_operations_menu(menubar)
        # create_gradient_menu(menubar)
        # create_function_menu(menubar)
        # create_noise_menu(menubar)
        # create_filters_menu(menubar)


app = App()
root = InterfaceInfo.get_instance().get_root()
save_path = "../../draws/"
save_generated_path = "../../generated/"

# main loop
root.mainloop()


