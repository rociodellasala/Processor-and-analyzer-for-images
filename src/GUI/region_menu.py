from tkinter import Menu, messagebox, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from image_access import open_file_name
from image_access import read_raw_image
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from src.GUI.region_selector import Region


def region_information():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to mark a region")
    else:
        region = Region()


def pixel_exchange():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to mark a region")
    else:
        region = Region()


class RegionMenu:
    def __init__(self, menubar):
        image_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Region", menu=image_menu)
        image_menu.add_command(label="Information", command=region_information)
        image_menu.add_command(label="Pixel exchange", command=pixel_exchange)


