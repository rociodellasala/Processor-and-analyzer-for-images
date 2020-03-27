# TODO remove extras
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
import numpy as np
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

WIDTH = 512
HEIGHT = 512


class InterfaceInfo:
    __instance = None

    def __init__(self):
        if InterfaceInfo.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.root = Tk()
            self.current_image = None
            self.image_to_copy = None
            self.left_image = None
            self.right_image = None
            self.buttons_frame = None
            self.image_frame = None
            self.footer_frame = None
            InterfaceInfo.__instance = self

    @staticmethod
    def get_instance():
        if InterfaceInfo.__instance is None:
            InterfaceInfo()
        return InterfaceInfo.__instance

    def get_root(self):
        return self.root

    def configure(self):
        # can only resize height
        self.root.style = ttk.Style()
        # ('clam', 'alt', 'default', 'classic')
        self.root.style.theme_use("clam")
        ttk.Style().configure("Label", background=color.TOP_COLOR)
        self.root.resizable(False, True)
        self.root.title('ATI interface')
        self.root.state('zoomed')

    def load_frames(self):
        self.buttons_frame = Frame(self.root, bg=color.TOP_COLOR, bd=2,
                                   height=self.root.winfo_screenheight() / 8,
                                   width=self.root.winfo_screenwidth())
        self.buttons_frame.pack(side=TOP, expand=True, fill=BOTH)
        self.image_frame = Frame(self.root, bg=color.MIDDLE_COLOR, bd=2,
                                 height=self.root.winfo_screenheight() / 1.5,
                                 width=self.root.winfo_screenwidth())
        self.image_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.footer_frame = Frame(self.root, bg=color.BOTTOM_COLOR,
                                  bd=2, height=self.root.winfo_screenheight() / 10,
                                  width=self.root.winfo_screenwidth())
        self.footer_frame.pack(side=BOTTOM, expand=True, fill=BOTH)

    def clean_images(self):
        self.current_image = None
        self.left_image = None
        self.right_image = None

    def delete_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        if frame is self.image_frame:
            self.clean_images()

    def remove_images(self):
        self.clean_images()
        self.delete_widgets(self.image_frame)

