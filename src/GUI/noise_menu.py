from tkinter import Menu, messagebox, ttk, Entry, BooleanVar, Radiobutton
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from noise_generators import gaussian_noise_generator
from noise_generators import rayleigh_noise_generator
from noise_generators import exponential_noise_generator
from noise_generators import salt_and_pepper_noise_generator


def generate_gaussian_noise_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Percentage", background=constants.TOP_COLOR).grid(row=0, column=3)
        ttk.Label(interface.buttons_frame, text="Mu", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Sigma", background=constants.TOP_COLOR).grid(row=1, column=0)
        percentage = Entry(interface.buttons_frame)
        mu = Entry(interface.buttons_frame)
        sigma = Entry(interface.buttons_frame)
        percentage.grid(row=0, column=4)
        mu.grid(row=0, column=2)
        sigma.grid(row=1, column=2)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(interface.buttons_frame, text="Additive", value=True,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=5)
        Radiobutton(interface.buttons_frame, text="Multiplicative", value=False,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=5)
        generate_noise = ttk.Button(interface.buttons_frame, text="Generate",
                                    command=lambda: gaussian_noise_generator(float(percentage.get()), radio_var.get(),
                                                                             interface.current_image, constants.WIDTH,
                                                                             constants.HEIGHT, int(mu.get()),
                                                                             float(sigma.get())))
        generate_noise.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to generate gaussian noise")


def generate_rayleigh_noise_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Percentage", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Xi", background=constants.TOP_COLOR).grid(row=1, column=0)
        percentage = Entry(interface.buttons_frame)
        xi = Entry(interface.buttons_frame)
        percentage.grid(row=0, column=1)
        xi.grid(row=1, column=1)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(interface.buttons_frame, text="Additive", value=True,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=2)
        Radiobutton(interface.buttons_frame, text="Multiplicative", value=False,
                    variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=2)
        generate_noise = ttk.Button(interface.buttons_frame, text="Generate",
                                    command=lambda: rayleigh_noise_generator(float(percentage.get()), radio_var.get(),
                                                                             interface.current_image, constants.WIDTH,
                                                                             constants.HEIGHT, float(xi.get())))
        generate_noise.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to generate rayleigh noise")


def generate_exponential_noise_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Percentage", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Lambda", background=constants.TOP_COLOR).grid(row=1, column=0)
        percentage = Entry(interface.buttons_frame)
        lambda_value = Entry(interface.buttons_frame)
        percentage.grid(row=0, column=1)
        lambda_value.grid(row=1, column=1)
        radio_var = BooleanVar()
        radio_var.set(True)
        Radiobutton(interface.buttons_frame, text="Additive",
                    value=True, variable=radio_var, background=constants.TOP_COLOR).grid(row=0, column=2)
        Radiobutton(interface.buttons_frame, text="Multiplicative",
                    value=False, variable=radio_var, background=constants.TOP_COLOR).grid(row=1, column=2)
        generate_noise = ttk.Button(interface.buttons_frame, text="Generate",
                                    command=lambda: exponential_noise_generator(float(percentage.get()),
                                                                                radio_var.get(),
                                                                                interface.current_image,
                                                                                constants.WIDTH, constants.HEIGHT,
                                                                                float(lambda_value.get())))
        generate_noise.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to generate exponential noise")


def generate_salt_and_pepper_noise_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Density", background=constants.TOP_COLOR).grid(row=0, column=0)
        density = Entry(interface.buttons_frame)
        density.grid(row=0, column=1)
        generate_salt_and_pepper = ttk.Button(interface.buttons_frame, text="Generate",
                                              command=lambda: salt_and_pepper_noise_generator(interface.current_image,
                                                                                              constants.WIDTH,
                                                                                              constants.HEIGHT,
                                                                                              float(density.get())))
        generate_salt_and_pepper.grid(row=1, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to generate salt and pepper noise")


class NoiseMenu:
    def __init__(self, menubar):
        noise_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Noise", menu=noise_menu)
        noise_menu.add_command(label="Gaussian", command=generate_gaussian_noise_input)
        noise_menu.add_command(label="Rayleigh", command=generate_rayleigh_noise_input)
        noise_menu.add_command(label="Exponential", command=generate_exponential_noise_input)
        noise_menu.add_command(label="Salt and Pepper", command=generate_salt_and_pepper_noise_input)
