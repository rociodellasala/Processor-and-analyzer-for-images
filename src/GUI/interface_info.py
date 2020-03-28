from src.GUI import gui_constants as color
from tkinter import Frame, ttk, TOP, BOTH, BOTTOM, Tk


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

    def reset_parameters(self):
        self.remove_images()
        self.delete_widgets(self.buttons_frame)

