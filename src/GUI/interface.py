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
from src.GUI import gui_constants



def load_image(row, column, image_instance):
    file_name = open_file_name()
    if file_name:
        if file_name.endswith(".RAW"):
            raw_image = read_raw_image(file_name)
            image = Image.frombytes('L', (int(raw_image[1][0]), int(raw_image[1][1])), raw_image[0])
        else:
            # opens the image
            image = Image.open(file_name)
        # resize the image and apply a high-quality down sampling filter
        image = image.resize((512, 512), Image.ANTIALIAS)
        image_instance = image
        # PhotoImage class is used to add image to widgets, icons etc
        image = ImageTk.PhotoImage(image)
        # create a label
        panel = Label(image_frame, image=image)
        # set the image as img
        panel.image = image
        panel.grid(row=row, column=column)
        return image_instance

def load_image_wrapper():
    global current_image, converted_image
    if current_image is None:
        current_image = load_image(0, 0, current_image)
    else:
        converted_image = load_image(0, 1, converted_image)


def save_image():
    image = Image.open('../../images/Lenaclor.ppm')
    image_info = image.filename = asksaveasfilename(initialdir="/", title="Select file", filetypes=(
        ('jpg', '*.jpg'), ('jpeg', '*.jpeg'), ('png', '*.png'), ('ppm', '*.ppm'), ("pgm", "*.pgm")))
    image.save(image_info)


def load_menu():
    menubar = Menu(root)
    root.config(menu=menubar)
    image_menu = Menu(menubar, tearoff=0)
    pixel_menu = Menu(menubar, tearoff=0)
    draw_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Image", menu=image_menu)
    image_menu.add_command(label="Open", command=load_image_wrapper)
    image_menu.add_command(label="Save", command=save_image)
    image_menu.add_separator()
    image_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Pixel", menu=pixel_menu)
    pixel_menu.add_command(label="Get", command=load_pixel_input)
    pixel_menu.add_command(label="Modify", command=modify_pixel_input)
    pixel_menu.add_command(label="Copy", command=copy_subimage_input)
    menubar.add_cascade(label="Draw", menu=draw_menu)
    draw_menu.add_command(label="Rectangle", command=generate_rectangle_input)
    draw_menu.add_command(label="Circle", command=generate_circle_input)


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
        modify_pixel_button = Button(buttons_frame, text="Set Value", command=lambda: modify_pixel_value(x.get(), y.get()))
        modify_pixel_button.grid(row=2, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload an image")


def modify_pixel_value(x, y):
    global converted_image
    converted_image = current_image
    px = converted_image.load()
    px[int(x), int(y)] = 255
    image = ImageTk.PhotoImage(converted_image)
    # create a label
    new_panel = Label(image_frame, image=image)
    # set the image as img
    new_panel.image = image
    new_panel.grid(row=0, column=2)


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


def copy_subimage_input():
    if current_image is not None and converted_image is not None:
        delete_widgets(buttons_frame)
        Label(buttons_frame, text="Original image").grid(row=0, column=0)
        Label(buttons_frame, text="X").grid(row=1, column=0)
        Label(buttons_frame, text="Y").grid(row=2, column=0)
        Label(buttons_frame, text="width").grid(row=1, column=2)
        Label(buttons_frame, text="height").grid(row=2, column=2)
        Label(buttons_frame, text="Image to copy").grid(row=0, column=4)
        Label(buttons_frame, text="X").grid(row=1, column=4)
        Label(buttons_frame, text="Y").grid(row=2, column=4)
        x_original = Entry(buttons_frame)
        y_original = Entry(buttons_frame)
        width_original = Entry(buttons_frame)
        height_original = Entry(buttons_frame)
        x_copy = Entry(buttons_frame)
        y_copy = Entry(buttons_frame)
        x_original.grid(row=1, column=1)
        y_original.grid(row=2, column=1)
        width_original.grid(row=1, column=3)
        height_original.grid(row=2, column=3)
        x_copy.grid(row=1, column=5)
        y_copy.grid(row=2, column=5)
        modify_pixel_button = Button(buttons_frame, text="Copy",
                                     command=lambda: copy_pixels(int(x_original.get()),
                                                                 int(y_original.get()),
                                                                 int(width_original.get()), int(height_original.get()),
                                                                 int(x_copy.get())-1, int(y_copy.get())))
        modify_pixel_button.grid(row=3, column=0)
    else:
        messagebox.showerror(title="Error", message="You must upload two images")


def copy_pixels(x_original, y_original, width_original, height_original, x_copy, y_copy):
    pixels = current_image.load()
    converted = converted_image.load()
    y_copy_aux = y_copy

    for x in range(x_original, x_original + width_original):
        x_copy += 1
        y_copy = y_copy_aux
        for y in range(y_original, y_original + height_original):
            if x < 512 and y < 512 and x_copy < 512 and y_copy < 512:
                pixels[x, y] = converted[x_copy, y_copy]
                y_copy += 1

    image = ImageTk.PhotoImage(current_image)
    # create a label
    new_panel = Label(image_frame, image=image)
    # set the image as img
    new_panel.image = image
    new_panel.grid(row=0, column=1)



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
    global converted_image, current_image
    converted_image = None
    current_image = None


root = Tk()
root.title('ATI interface')
root.state('zoomed')
current_image = None
converted_image = None
buttons_frame = None
image_frame = None
footer_frame = None
load_frames()
load_menu()

# main loop
root.mainloop()
