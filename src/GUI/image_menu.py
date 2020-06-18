from tkinter import Menu, messagebox, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from image_access import open_file_name
from image_access import read_raw_image
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
import numpy as np
from border_detectors import four_direction_border_detection, canny_method, susan_method, colored_canny_method, harris_method, sift_method, compare_images #TODO remove
from line_detectors import hough_transform, pixel_exchange, circular_hough_transform #TODO remove


def load_image(row, column):
    interface = InterfaceInfo.get_instance()
    file_name = open_file_name()
    if file_name:
        interface.current_image_name = file_name
        if file_name.endswith(".RAW"):
            raw_image = read_raw_image(file_name)
            image = Image.frombytes('L', (int(raw_image[1][0]), int(raw_image[1][1])), raw_image[0])
        else:
            # opens the image
            image = Image.open(file_name)
        # resize the image and apply a high-quality down sampling filter
        image = image.resize((constants.WIDTH, constants.HEIGHT), Image.ANTIALIAS)
        image_instance = image
        # PhotoImage class is used to add image to widgets, icons etc
        image = ImageTk.PhotoImage(image)
        # create a label
        # panel = ttk.Label(interface.image_frame, image=image)
        interface.generate_canvas()
        interface.canvas.create_image(0, 0, image=image, anchor="nw")
        # set the image as img
        interface.canvas.image = image
        return image_instance


def load_image_wrapper():
    interface = InterfaceInfo.get_instance()
    interface.remove_images()
    if interface.current_image is None:
        interface.current_image = load_image(0, 0)
        # harris_method(interface.current_image, constants.HEIGHT, constants.WIDTH, 0.8)
        sift_method(interface.current_image, constants.HEIGHT, constants.WIDTH)
        compare_images(interface.current_image, constants.HEIGHT, constants.WIDTH, interface.current_image, constants.HEIGHT, constants.WIDTH, 400)
    elif interface.image_to_copy is None:
        interface.image_to_copy = load_image(0, 1)
    else:
        messagebox.showerror(title="Error", message="You can't upload more than two images. If you want to change"
                                                    " one click on the \"Clean image\" button first")


def save_image():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to save it")
    else:
        image = interface.current_image
        image_info = image.filename = asksaveasfilename(initialdir="/", title="Select file", filetypes=(
            ('ppm', '*.ppm'), ('jpg', '*.jpg'), ('jpeg', '*.jpeg'), ('png', '*.png'),  ("pgm", "*.pgm")))
        image.convert("I")
        image.save(image_info)


class ImageMenu:
    def __init__(self, menubar):
        interface = InterfaceInfo.get_instance()
        image_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Image", menu=image_menu)
        image_menu.add_command(label="Open", command=load_image_wrapper)
        image_menu.add_command(label="Save", command=save_image)
        image_menu.add_separator()
        image_menu.add_command(label="Exit", command=interface.root.quit)


