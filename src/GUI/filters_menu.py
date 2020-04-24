from tkinter import Menu, messagebox, ttk, Entry
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from filters import media_filter, median_filter, weighted_median_filter, \
    gaussian_filter, bilateral_filter, anisotropic_diffusion_filter, isotropic_diffusion_filter


def generate_media_filter_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Windows size", background=constants.TOP_COLOR).grid(row=0, column=0)
        windows_size = Entry(interface.buttons_frame)
        windows_size.grid(row=0, column=1)
        generate_noise = ttk.Button(interface.buttons_frame, text="Apply",
                                    command=lambda: media_filter(interface.current_image, constants.WIDTH,
                                                                 constants.HEIGHT, int(windows_size.get())))
        generate_noise.grid(row=1, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply media filter")


def generate_median_filter_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Windows size", background=constants.TOP_COLOR).grid(row=0, column=0)
        windows_size = Entry(interface.buttons_frame)
        windows_size.grid(row=0, column=1)
        generate_noise = ttk.Button(interface.buttons_frame, text="Apply",
                                    command=lambda: median_filter(interface.current_image, constants.WIDTH,
                                                                  constants.HEIGHT, int(windows_size.get())))
        generate_noise.grid(row=1, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply median filter ")


def weighted_median_wrapper(image, width, height):
    if image is None:
        messagebox.showerror(title="Error", message="You need to upload an image to apply weighted median filter ")
    else:
        weighted_median_filter(image, width, height, 3)


def generate_gaussian_filter_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Sigma", background=constants.TOP_COLOR).grid(row=0, column=0)
        sigma = Entry(interface.buttons_frame)
        sigma.grid(row=0, column=1)
        generate_noise = ttk.Button(interface.buttons_frame, text="Apply",
                                    command=lambda: gaussian_filter(interface.current_image, constants.WIDTH,
                                                                    constants.HEIGHT, int(sigma.get())))
        generate_noise.grid(row=1, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply gaussian filter ")


def generate_bilateral_filter_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="Sigma r", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Sigma s", background=constants.TOP_COLOR).grid(row=1, column=0)
        ttk.Label(interface.buttons_frame, text="Windows size", background=constants.TOP_COLOR).grid(row=0, column=2)
        sigma_r = Entry(interface.buttons_frame)
        sigma_s = Entry(interface.buttons_frame)
        windows_size = Entry(interface.buttons_frame)
        sigma_r.grid(row=0, column=1)
        sigma_s.grid(row=1, column=1)
        windows_size.grid(row=0, column=3)
        generate_noise = ttk.Button(interface.buttons_frame, text="Apply",
                                    command=lambda: bilateral_filter(interface.current_image, constants.WIDTH,
                                                                     constants.HEIGHT, int(sigma_r.get()),
                                                                     int(sigma_s.get()), int(windows_size.get())))
        generate_noise.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply gaussian filter")


def generate_anisotropic_diffusion_filter_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="T max", background=constants.TOP_COLOR).grid(row=0, column=0)
        ttk.Label(interface.buttons_frame, text="Sigma", background=constants.TOP_COLOR).grid(row=1, column=0)
        t_max = Entry(interface.buttons_frame)
        sigma = Entry(interface.buttons_frame)
        t_max.grid(row=0, column=1)
        sigma.grid(row=1, column=1)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: anisotropic_diffusion_filter(interface.current_image,
                                                                               constants.WIDTH, constants.HEIGHT,
                                                                               int(t_max.get()), int(sigma.get())))
        apply_filter.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply anisotropic diffusion filter")


def generate_isotropic_diffusion_filter_input():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is not None:
        interface.delete_widgets(interface.buttons_frame)
        ttk.Label(interface.buttons_frame, text="T max", background=constants.TOP_COLOR).grid(row=0, column=0)
        t_max = Entry(interface.buttons_frame)
        t_max.grid(row=0, column=1)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  command=lambda: isotropic_diffusion_filter(interface.current_image,
                                                                               constants.WIDTH, constants.HEIGHT,
                                                                               int(t_max.get())))
        apply_filter.grid(row=2, column=0)
    else:
        interface.reset_parameters()
        messagebox.showerror(title="Error", message="You must upload an image to apply isotropic diffusion filter")


class FiltersMenu:
    def __init__(self, menubar):
        interface = InterfaceInfo.get_instance()
        filters_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Filters", menu=filters_menu)
        filters_menu.add_command(label="Media", command=generate_media_filter_input)
        filters_menu.add_command(label="Median", command=generate_median_filter_input)
        filters_menu.add_command(label="Weighted median",
                                 command=lambda: weighted_median_wrapper(interface.current_image, constants.WIDTH,
                                                                         constants.HEIGHT))
        filters_menu.add_command(label="Gaussian", command=generate_gaussian_filter_input)
        filters_menu.add_command(label="Bilateral", command=generate_bilateral_filter_input)
        filters_menu.add_command(label="Isotropic diffusion", command=generate_isotropic_diffusion_filter_input)
        filters_menu.add_command(label="Anisotropic diffusion", command=generate_anisotropic_diffusion_filter_input)
