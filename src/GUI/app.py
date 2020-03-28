# TODO remove extras
from tkinter import messagebox, ttk, Menu
from filters import media_filter
from filters import weighted_median_filter
from filters import median_filter
from filters import gaussian_filter
from filters import border_enhancement_filter

from src.GUI.draw_menu import DrawMenu
from src.GUI.function_menu import FunctionMenu
from src.GUI.gradient_menu import GradientMenu
from src.GUI.image_menu import ImageMenu
from src.GUI.interface_info import InterfaceInfo
from src.GUI.noise_menu import NoiseMenu
from src.GUI.operations_menu import OperationsMenu
from src.GUI.pixel_menu import PixelMenu

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
        GradientMenu(menubar)
        FunctionMenu(menubar)
        NoiseMenu(menubar)
        # create_filters_menu(menubar)


app = App()
root = InterfaceInfo.get_instance().get_root()
save_path = "../../draws/"
save_generated_path = "../../generated/"

# main loop
root.mainloop()


