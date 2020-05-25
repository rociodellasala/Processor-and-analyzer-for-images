from tkinter import Menu, messagebox, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image
from image_access import open_file_name
from image_access import read_raw_image
from src.GUI import gui_constants as constants
from src.GUI.interface_info import InterfaceInfo
from src.GUI.region_selector import Region
from src.GUI.modules.line_detectors import pixel_exchange, pixel_exchange_in_video


def region_information():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to mark a region")
    else:
        region = Region()


def pixel_exchange_wrapper():
    interface = InterfaceInfo.get_instance()
    if interface.current_image is None:
        messagebox.showerror(title="Error", message="You must upload an image to mark a region")
    else:
        region = Region()
        ttk.Label(interface.buttons_frame, text="Press Apply when selection is ready",
                  background=constants.TOP_COLOR).grid(row=0, column=0)
        apply_filter = ttk.Button(interface.buttons_frame, text="Apply",
                                  # command=lambda: pixel_exchange(interface.current_image,
                                  #                               constants.HEIGHT, constants.WIDTH,
                                  #                               region.start_x, region.start_y, region.end_x,
                                  #                                region.end_y, 40, 400, False))
                                  #
                                  command=lambda: pixel_exchange_in_video(interface.current_image,
                                                                          constants.HEIGHT, constants.WIDTH,
                                                                          interface.current_image_name, region.start_x,
                                                                          region.start_y, region.end_x, region.end_y, 40
                                                                          , 400, 2, False, False))
        apply_filter.grid(row=1, column=0)


class RegionMenu:
    def __init__(self, menubar):
        image_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Region", menu=image_menu)
        image_menu.add_command(label="Information", command=region_information)
        image_menu.add_command(label="Pixel exchange", command=pixel_exchange_wrapper)


