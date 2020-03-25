from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from read_raw_image import read_raw_image
from image_generator import generate_rectangle
from image_generator import generate_circle
from image_generator import gray_faded_image
from image_generator import color_faded_image
from image_operations import add_grey_images
from image_operations import subtract_grey_images
from image_operations import subtract_colored_images
from image_operations import multiply_grey_images_with_scalar
from image_operations import multiply_grey_images
from image_operations import dynamic_range_compression
from image_operations import grey_image_negative
from image_operations import colored_image_negative
from image_operations import gamma_pow_function
from image_operations import grey_level_histogram
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
from src.GUI import gui_constants

WIDTH = 512
HEIGHT = 512


def load_image(row, column):
    file_name = open_file_name()
    if file_name:
        if file_name.endswith(".RAW"):
            raw_image = read_raw_image(file_name)
            image = Image.frombytes('L', (int(raw_image[1][0]), int(raw_image[1][1])), raw_image[0])
        else:
            # opens the image
            image = Image.open(file_name)
        # resize the image and apply a high-quality down sampling filter
        image = image.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        image_instance = image
        # PhotoImage class is used to add image to widgets, icons etc
        image = ImageTk.PhotoImage(image)
        # create a label
        panel = Label(image_frame, image=image)
        # set the image as img
        panel.image = image
        panel.grid(row=row, column=column)
        # dynamic_range_compression(image_instance, 512, 512)
        # salt_and_pepper_noise_generator(image_instance, 512, 512, 0.01)
        # media_filter(image_instance, 512, 512, 5)
        # median_filter(image_instance, 512, 512, 5)
        # weighted_median_filter(image_instance, 512, 512, 3)
        # median_filter(image_instance, 512, 512, 5)
        # gaussian_filter(image_instance, 512, 512, 3)
        # border_enhancement_filter(image_instance, 512, 512)
        return image_instance


def load_image_wrapper():
    remove_images()
    global current_image, image_to_copy
    if current_image is None:
        current_image = load_image(0, 0)
    elif image_to_copy is None:
        image_to_copy = load_image(0, 1)
    else:
        messagebox.showerror(title="Error", message="You can't upload more than two images. If you want to change"
                                                    " one click on the \"Clean image\" button first")


def load_left_image():
    global left_image
    left_image = load_image(0, 0)


def load_right_image():
    global right_image
    right_image = load_image(0, 1)


def save_image():
    image = Image.open('../../images/Lenaclor.ppm')
    image_info = image.filename = asksaveasfilename(initialdir="/", title="Select file", filetypes=(
        ('jpg', '*.jpg'), ('jpeg', '*.jpeg'), ('png', '*.png'), ('ppm', '*.ppm'), ("pgm", "*.pgm")))
    image.save(image_info)


def create_image_menu(menubar):
    image_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Image", menu=image_menu)
    image_menu.add_command(label="Open", command=load_image_wrapper)
    image_menu.add_command(label="Save", command=save_image)
    image_menu.add_separator()
    image_menu.add_command(label="Exit", command=root.quit)


def create_pixel_menu(menubar):
    pixel_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Pixel", menu=pixel_menu)
    pixel_menu.add_command(label="Get", command=load_pixel_input)
    pixel_menu.add_command(label="Modify", command=modify_pixel_input)


def create_draw_menu(menubar):
    draw_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Draw", menu=draw_menu)
    draw_menu.add_command(label="Rectangle", command=generate_rectangle_input)
    draw_menu.add_command(label="Circle", command=generate_circle_input)


def create_gradient_menu(menubar):
    gradient_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Gradient", menu=gradient_menu)
    gradient_menu.add_command(label="Gray", command=generate_gray_fading_input)
    gradient_menu.add_command(label="Color", command=generate_color_fading_input)


def create_function_menu(menubar):
    function_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Function", menu=function_menu)
    function_menu.add_command(label="Gamma", command=generate_gamma_input)
    function_menu.add_command(label="Dynamic Range Compression", command=generate_range_compression_input)
    function_menu.add_command(label="Threshold", command=generate_image_threshold_input)  # add command
    function_menu.add_command(label="Equalization", command=generate_equalized_image)  # add command
    function_menu.add_command(label="Grey Histogram")  # add command


def create_operations_menu(menubar):
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
    operation_menu.add_command(label="Copy", command=copy_sub_image_input)
    negative_menu = Menu(operation_menu, tearoff=0)
    operation_menu.add_cascade(label="Negative", menu=negative_menu)
    negative_menu.add_command(label="Colored Negative",
                              command=lambda: colored_negative_wrapper(current_image, 512, 512))
    negative_menu.add_command(label="Grey Negative",
                              command=lambda: grey_negative_wrapper(current_image, 512, 512))


def create_filters_menu(menubar):
    filters_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Filters", menu=filters_menu)
    filters_menu.add_command(label="Media")  # add command
    filters_menu.add_command(label="Median")  # add command
    filters_menu.add_command(label="Weighted median")  # add command
    filters_menu.add_command(label="Gaussian")  # add command
    filters_menu.add_command(label="Border enhancement")  # add command


def create_noise_menu(menubar):
    noise_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Noise", menu=noise_menu)
    noise_menu.add_command(label="Gaussian", command=generate_gaussian_noise_input)  # add command
    noise_menu.add_command(label="Rayleigh", command=generate_rayleigh_noise_input)  # add command
    noise_menu.add_command(label="Exponential", command=generate_exponential_noise_input)  # add command


def load_menu():
    menubar = Menu(root)
    root.config(menu=menubar)
    create_image_menu(menubar)
    create_pixel_menu(menubar)
    create_operations_menu(menubar)
    create_draw_menu(menubar)
    create_gradient_menu(menubar)
    create_function_menu(menubar)
    create_noise_menu(menubar)
    create_filters_menu(menubar)


def open_file_name():
    file_name = filedialog.askopenfilename(title='Choose Image', filetypes=[("ppm", "*.ppm"), ("pgm", "*.pgm"),
                                                                            ("jpg", "*.jpg"), ("png", "*.png"),
                                                                            ("jpeg", "*.jpeg"), ("raw", "*.RAW")])
    if file_name:
        return file_name
    else:
        return ""


def load_pixel_input():
    if current_image is not None:
        delete_widgets(buttons_frame)
        Label(buttons_frame, text="x", ).grid(row=0, column=0)
        Label(buttons_frame, text="y").grid(row=1, column=0)
        x = Entry(buttons_frame)
        y = Entry(buttons_frame)
        x.grid(row=0, column=1)
        y.grid(row=1, column=1)
        get_pixel_button = Button(buttons_frame, text="Get Value", command=lambda: get_pixel_value(x.get(), y.get()))
        get_pixel_button.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def get_pixel_value(x, y):
    px = current_image.load()
    Label(buttons_frame, text=px[int(y), int(x)]).grid(row=2, column=1)


def modify_pixel_input():
    if current_image is not None:
        delete_widgets(buttons_frame)
        Label(buttons_frame, text="x").grid(row=0, column=0)
        Label(buttons_frame, text="y").grid(row=1, column=0)
        x = Entry(buttons_frame)
        y = Entry(buttons_frame)
        x.grid(row=0, column=1)
        y.grid(row=1, column=1)
        modify_pixel_button = Button(buttons_frame, text="Set Value",
                                     command=lambda: modify_pixel_value(x.get(), y.get()))
        modify_pixel_button.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def modify_pixel_value(x, y):
    px = current_image.load()
    px[int(x), int(y)] = 255
    global save_path
    current_image.save(save_path + "pixel_modification.png")
    current_image.show()


def generate_rectangle_input():
    clean_images()
    delete_widgets(buttons_frame)
    delete_widgets(image_frame)
    Label(buttons_frame, text="rectangle width").grid(row=0, column=0)
    Label(buttons_frame, text="rectangle height").grid(row=1, column=0)
    Label(buttons_frame, text="image width").grid(row=0, column=2)
    Label(buttons_frame, text="image height").grid(row=1, column=2)
    width = Entry(buttons_frame)
    height = Entry(buttons_frame)
    image_width = Entry(buttons_frame)
    image_height = Entry(buttons_frame)
    radio_var = BooleanVar()
    radio_var.set(True)
    Radiobutton(buttons_frame, text="Empty", value=False, variable=radio_var).grid(row=1, column=4)
    Radiobutton(buttons_frame, text="Filled", value=True, variable=radio_var).grid(row=0, column=4)
    width.grid(row=0, column=1)
    height.grid(row=1, column=1)
    image_width.grid(row=0, column=3)
    image_height.grid(row=1, column=3)
    modify_pixel_button = Button(buttons_frame, text="Draw", command=lambda:
    generate_rectangle("rectangle.png", int(image_width.get()), int(image_height.get()), int(width.get()),
                       int(height.get()), radio_var.get()))
    modify_pixel_button.grid(row=3, column=0)


def generate_circle_input():
    clean_images()
    delete_widgets(buttons_frame)
    delete_widgets(image_frame)
    Label(buttons_frame, text="radius").grid(row=0, column=0)
    Label(buttons_frame, text="image width").grid(row=0, column=2)
    Label(buttons_frame, text="image height").grid(row=1, column=2)
    radius = Entry(buttons_frame)
    image_width = Entry(buttons_frame)
    image_height = Entry(buttons_frame)
    radio_var = BooleanVar()
    radio_var.set(True)
    Radiobutton(buttons_frame, text="Filled", value=True, variable=radio_var).grid(row=0, column=4)
    Radiobutton(buttons_frame, text="Empty", value=False, variable=radio_var).grid(row=1, column=4)
    radius.grid(row=0, column=1)
    image_width.grid(row=0, column=3)
    image_height.grid(row=1, column=3)
    modify_pixel_button = Button(buttons_frame, text="Draw", command=lambda:
    generate_circle("circle.png", int(image_width.get()), int(image_height.get()),
                    int(radius.get()), radio_var.get()))
    modify_pixel_button.grid(row=3, column=0)


def generate_gray_fading_input():
    clean_images()
    delete_widgets(buttons_frame)
    delete_widgets(image_frame)
    Label(buttons_frame, text="image width").grid(row=0, column=2)
    Label(buttons_frame, text="image height").grid(row=1, column=2)
    image_width = Entry(buttons_frame)
    image_height = Entry(buttons_frame)
    image_width.grid(row=0, column=3)
    image_height.grid(row=1, column=3)
    generate_gray_fading_button = Button(buttons_frame, text="Show", command=lambda:
    gray_faded_image(int(image_width.get()), int(image_height.get())))
    generate_gray_fading_button.grid(row=3, column=0)


def generate_color_fading_input():
    clean_images()
    delete_widgets(buttons_frame)
    delete_widgets(image_frame)
    Label(buttons_frame, text="image width").grid(row=0, column=2)
    Label(buttons_frame, text="image height").grid(row=1, column=2)
    red = BooleanVar()
    green = BooleanVar()
    blue = BooleanVar()
    Checkbutton(buttons_frame, text="Red", variable=red).grid(row=2, column=1)
    Checkbutton(buttons_frame, text="Green", variable=green).grid(row=2, column=2)
    Checkbutton(buttons_frame, text="Blue", variable=blue).grid(row=2, column=3)
    image_width = Entry(buttons_frame)
    image_height = Entry(buttons_frame)
    image_width.grid(row=0, column=3)
    image_height.grid(row=1, column=3)
    generate_gray_fading_button = Button(buttons_frame, text="Show",
                                         command=lambda: color_faded_image(int(image_width.get()),
                                                                           int(image_height.get()),
                                                                           red.get(), green.get(),
                                                                           blue.get()))
    generate_gray_fading_button.grid(row=3, column=0)


def gamma_pow_function_wrapper(image, width, height, gamma):
    error = False
    try:
        gamma_value = float(gamma)
    except ValueError:
        error = True
        messagebox.showerror(title="Error", message="You need to insert a valid gamma.")
    if (not error) and image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to apply gamma.")
    elif not error:
        gamma_pow_function(image, width, height, gamma_value)


def generate_gamma_input():
    delete_widgets(buttons_frame)
    delete_widgets(image_frame)
    Label(buttons_frame, text="Gamma").grid(row=0, column=0)
    gamma = Entry(buttons_frame)
    gamma.grid(row=0, column=1)
    apply_button = Button(buttons_frame, text="Apply",
                          command=lambda: gamma_pow_function_wrapper(current_image, 512, 512, gamma.get()))
    apply_button.grid(row=1, column=0)


def generate_range_compression_input():
    delete_widgets(buttons_frame)
    if current_image is not None:
        dynamic_range_compression(current_image, 512, 512)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def copy_sub_image_input():
    generate_binary_operations_input()
    Label(buttons_frame, text="Original image").grid(row=1, column=0)
    Label(buttons_frame, text="X").grid(row=2, column=0)
    Label(buttons_frame, text="Y").grid(row=3, column=0)
    Label(buttons_frame, text="width").grid(row=2, column=2)
    Label(buttons_frame, text="height").grid(row=3, column=2)
    Label(buttons_frame, text="Image to copy").grid(row=1, column=4)
    Label(buttons_frame, text="X").grid(row=2, column=4)
    Label(buttons_frame, text="Y").grid(row=3, column=4)
    x_original = Entry(buttons_frame)
    y_original = Entry(buttons_frame)
    width_original = Entry(buttons_frame)
    height_original = Entry(buttons_frame)
    x_copy = Entry(buttons_frame)
    y_copy = Entry(buttons_frame)
    x_original.grid(row=2, column=1)
    y_original.grid(row=3, column=1)
    width_original.grid(row=2, column=3)
    height_original.grid(row=3, column=3)
    x_copy.grid(row=2, column=5)
    y_copy.grid(row=3, column=5)
    modify_pixel_button = Button(buttons_frame, text="Copy",
                                 command=lambda: copy_pixels(int(x_original.get()),
                                                             int(y_original.get()),
                                                             int(width_original.get()), int(height_original.get()),
                                                             int(x_copy.get()) - 1, int(y_copy.get()),
                                                             left_image, right_image))
    #TODO validate cast
    modify_pixel_button.grid(row=4, column=0)


def copy_pixels(x_original, y_original, width_original, height_original, x_copy, y_copy, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        pixels = image_1.load()
        copy = image_2.load()
        y_copy_aux = y_copy
        for x in range(x_original, x_original + width_original):
            x_copy += 1
            y_copy = y_copy_aux
            for y in range(y_original, y_original + height_original):
                if x < 512 and y < 512 and x_copy < 512 and y_copy < 512:
                    pixels[x, y] = copy[x_copy, y_copy]
                    y_copy += 1

        global save_path
        image_1.save(save_path + "copy_image.png")
        image_1.show()
    else:
        messagebox.showerror(title="Error", message="You must upload two images")


def generate_binary_operations_input():
    reset_parameters()
    image_1_button = Button(buttons_frame, text="Load Image 1", command=load_left_image).grid(row=0, column=0)
    image_2_button = Button(buttons_frame, text="Load Image 2", command=load_right_image).grid(row=0, column=1)


def binary_operation_validator(image_1, image_2):
    if image_1 is None or image_2 is None:
        return False
    else:
        return True


def add_grey_image_wrapper(width_1, height_1, image_1, width_2, height_2, image_2):
    if binary_operation_validator(image_1, image_2):
        add_grey_images(width_1, height_1, image_1, width_2, height_2, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to add.")


def generate_add_operation_input():
    generate_binary_operations_input()
    add_button = Button(buttons_frame, text="Add",
                        command=lambda: add_grey_image_wrapper(512, 512, left_image, 512, 512, right_image))
    add_button.grid(row=1, column=0)


def subtract_grey_image_wrapper(width, height, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        subtract_grey_images(width, height, image_1, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to subtract.")


def generate_subtract_grey_operation_input():
    generate_binary_operations_input()
    subtract_button = Button(buttons_frame, text="Subtract",
                             command=lambda: subtract_grey_image_wrapper(512, 512, left_image, right_image))
    subtract_button.grid(row=1, column=0)


def subtract_colored_image_wrapper(width, height, image_1, image_2):
    if binary_operation_validator(image_1, image_2):
        subtract_colored_images(width, height, image_1, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to subtract.")


def generate_subtract_colored_operation_input():
    generate_binary_operations_input()
    subtract_button = Button(buttons_frame, text="Subtract",
                             command=lambda: subtract_colored_image_wrapper(512, 512, left_image, right_image))
    subtract_button.grid(row=1, column=0)


def multiply_grey_images_wrapper(width_1, height_1, image_1, width_2, height_2, image_2):
    if binary_operation_validator(image_1, image_2):
        multiply_grey_images(width_1, height_1, image_1, width_2, height_2, image_2)
    else:
        messagebox.showerror(title="Error", message="You need to upload image 1 and 2 to multiply.")


def generate_multiply_images_operation_input():
    generate_binary_operations_input()
    multiply_button = Button(buttons_frame, text="Multiply",
                             command=lambda: multiply_grey_images_wrapper(512, 512, left_image, 512, 512, right_image))
    multiply_button.grid(row=1, column=0)


def multiply_grey_images_with_scalar_wrapper(width, height, image, scalar):
    error = False
    try:
        scalar_value = float(scalar)
    except ValueError:
        error = True
        messagebox.showerror(title="Error", message="You need to insert a valid scalar to multiply.")
    if (not error) and image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to multiply.")
    elif not error:
        multiply_grey_images_with_scalar(width, height, image, scalar_value)


def generate_multiply_by_scalar_input():
    reset_parameters()
    load_image_button = Button(buttons_frame, text="Load Image", command=load_left_image).grid(row=0, column=0)
    Label(buttons_frame, text="Scalar").grid(row=1, column=0)
    scalar = Entry(buttons_frame)
    scalar.grid(row=1, column=1)
    multiply_button = Button(buttons_frame, text="Multiply",
                             command=lambda: multiply_grey_images_with_scalar_wrapper(512, 512, left_image,
                                                                                      scalar.get()))
    multiply_button.grid(row=2, column=0)


def grey_negative_wrapper(image, width, height):
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to get its negative.")
    else:
        grey_image_negative(image, width, height)


def colored_negative_wrapper(image, width, height):
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to get its negative.")
    else:
        colored_image_negative(image, width, height)


def generate_image_threshold_input():
    delete_widgets(buttons_frame)
    if current_image is not None:
        Label(buttons_frame, text="Threshold").grid(row=0, column=0)
        threshold = Entry(buttons_frame)
        threshold.grid(row=1, column=0)
        apply_threshold = Button(buttons_frame, text="Apply",
                                 command=lambda: image_threshold(current_image, WIDTH, HEIGHT, int(threshold.get())))
        apply_threshold.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def generate_equalized_image():
    if current_image is not None:
        image_equalization(current_image, WIDTH, HEIGHT)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def generate_gaussian_noise_input():
    if current_image is not None:
        Label(buttons_frame, text="Percentage").grid(row=0, column=0)
        Label(buttons_frame, text="Mu").grid(row=0, column=2)
        Label(buttons_frame, text="Sigma").grid(row=1, column=2)
        percentage = Entry(buttons_frame)
        mu = Entry(buttons_frame)
        sigma = Entry(buttons_frame)
        percentage.grid(row=0, column=1)
        mu.grid(row=0, column=3)
        sigma.grid(row=1, column=3)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(buttons_frame, text="Additive", value=True, variable=radio_var).grid(row=0, column=4)
        Radiobutton(buttons_frame, text="Multiplicative", value=False, variable=radio_var).grid(row=1, column=4)
        generate_noise = Button(buttons_frame, text="Generate",
                                command=lambda: gaussian_noise_generator(float(percentage.get()), radio_var.get(),
                                                                         current_image, WIDTH, HEIGHT, int(mu.get()),
                                                                         int(sigma.get())))
        generate_noise.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def generate_rayleigh_noise_input():
    if current_image is not None:
        Label(buttons_frame, text="Percentage").grid(row=0, column=0)
        Label(buttons_frame, text="Xi").grid(row=0, column=2)
        percentage = Entry(buttons_frame)
        xi = Entry(buttons_frame)
        percentage.grid(row=0, column=1)
        xi.grid(row=0, column=3)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(buttons_frame, text="Additive", value=True, variable=radio_var).grid(row=0, column=4)
        Radiobutton(buttons_frame, text="Multiplicative", value=False, variable=radio_var).grid(row=1, column=4)
        generate_noise = Button(buttons_frame, text="Generate",
                                command=lambda: rayleigh_noise_generator(float(percentage.get()), radio_var.get(),
                                                                         current_image, WIDTH, HEIGHT, int(xi.get())))
        generate_noise.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def generate_exponential_noise_input():
    if current_image is not None:
        Label(buttons_frame, text="Percentage").grid(row=0, column=0)
        Label(buttons_frame, text="Lambda").grid(row=0, column=2)
        percentage = Entry(buttons_frame)
        lambda_value = Entry(buttons_frame)
        percentage.grid(row=0, column=1)
        lambda_value.grid(row=0, column=3)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(buttons_frame, text="Additive", value=True, variable=radio_var).grid(row=0, column=4)
        Radiobutton(buttons_frame, text="Multiplicative", value=False, variable=radio_var).grid(row=1, column=4)
        generate_noise = Button(buttons_frame, text="Generate",
                                command=lambda: exponential_noise_generator(float(percentage.get()), radio_var.get(),
                                                                            current_image, WIDTH, HEIGHT,
                                                                            int(lambda_value.get())))
        generate_noise.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def delete_widgets(frame):
    print(frame)
    for widget in frame.winfo_children():
        widget.destroy()
    if frame is image_frame:
        clean_images()


def ask_quit():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        root.destroy()


def load_footer_buttons():
    global buttons_frame, image_frame
    exit_program_btn = Button(footer_frame, text="Exit Program", command=ask_quit)
    exit_program_btn.grid(column=0, row=0)
    clean_window_btn = Button(footer_frame, text="Clean buttons", command=lambda: delete_widgets(buttons_frame))
    clean_window_btn.grid(column=1, row=0)
    clean_window_btn = Button(footer_frame, text="Clean image", command=lambda: delete_widgets(image_frame))
    clean_window_btn.grid(column=2, row=0)


def load_frames():
    global buttons_frame, image_frame, footer_frame
    buttons_frame = Frame(root, bg=gui_constants.TOP_COLOR, bd=2,
                          height=root.winfo_screenheight() / 8, width=root.winfo_screenwidth())
    buttons_frame.pack(side=TOP, expand=True, fill=BOTH)
    image_frame = Frame(root, bg=gui_constants.MIDDLE_COLOR, bd=2,
                        height=root.winfo_screenheight() / 1.5, width=root.winfo_screenwidth())
    image_frame.pack(side=TOP, fill=BOTH, expand=True)
    footer_frame = Frame(root, bg=gui_constants.BOTTOM_COLOR,
                         bd=2, height=root.winfo_screenheight() / 10, width=root.winfo_screenwidth())
    footer_frame.pack(side=BOTTOM, expand=True, fill=BOTH)
    load_footer_buttons()


def clean_images():
    global current_image, image_to_copy, left_image, right_image
    image_to_copy = None
    current_image = None
    left_image = None
    right_image = None


def remove_images():
    clean_images()
    delete_widgets(image_frame)


def reset_parameters():
    remove_images()
    delete_widgets(buttons_frame)


root = Tk()
# can only resize height
root.resizable(False, True)
root.title('ATI interface')
root.state('zoomed')

current_image = None
image_to_copy = None
left_image = None
right_image = None

buttons_frame = None
image_frame = None
footer_frame = None

load_frames()
load_menu()

save_path = "../../draws/"

# main loop
root.mainloop()


