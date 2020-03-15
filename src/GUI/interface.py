from read_raw_image import read_raw_image
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from PIL import ImageTk, Image


def load_image():
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
        global current_image
        current_image = image
        # PhotoImage class is used to add image to widgets, icons etc
        image = ImageTk.PhotoImage(image)
        # create a label
        panel = Label(root, image=image)
        # set the image as img
        panel.image = image
        panel.grid(row=3, column=0, columnspan=4, rowspan=4)


def save_image():
    image = Image.open('../../images/Lenaclor.ppm')
    image_info = image.filename = asksaveasfilename(initialdir="/", title="Select file", filetypes=(
        ('jpg', '*.jpg'), ('jpeg', '*.jpeg') ('png', '*.png'), ('ppm', '*.ppm'), ("pgm", "*.pgm")))
    image.save(image_info)


def load_menu():
    menubar = Menu(root)
    root.config(menu=menubar)
    image_menu = Menu(menubar, tearoff=0)
    pixel_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Image", menu=image_menu)
    image_menu.add_command(label="Open", command=load_image)
    image_menu.add_command(label="Save", command=save_image)
    image_menu.add_separator()
    image_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Pixel", menu=pixel_menu)
    pixel_menu.add_command(label="Get", command=load_pixel_input)
    pixel_menu.add_command(label="Modify", command=modify_pixel_input)


def open_file_name():
    file_name = filedialog.askopenfilename(title='Choose Image', filetypes=[("ppm", "*.ppm"), ("pgm", "*.pgm"),
                                                                            ("jpg", "*.jpg"), ("png", "*.png"),
                                                                            ("jpeg", "*.jpeg"),("raw", "*.RAW")])
    if file_name:
        return file_name
    else:
        return ""


def load_pixel_input():
    Label(root, text="x").grid(row=0, column=0)
    Label(root, text="y").grid(row=1, column=0)
    x = Entry(root)
    y = Entry(root)
    x.grid(row=0, column=1)
    y.grid(row=1, column=1)
    # Button(root, text="Get Value", command=get_pixel_value(x.get(), y.get())).grid(row=2, column=0)
    get_pixel_button = Button(root, text="Get Value", command=lambda: get_pixel_value(x.get(), y.get()))
    # get_pixel_button['command'] = lambda arg1=x.get(), arg2=y.get(): print(arg1, arg2)
    get_pixel_button.grid(row=2, column=0)


def get_pixel_value(x, y):
    global current_image
    px = current_image.load()
    print(px[int(y), int(x)])
    Label(root, text=px[int(y), int(x)]).grid(row=2, column=1)


def modify_pixel_value(x, y):
    global current_image
    px = current_image.load()
    print(px[int(y), int(x)])
    Label(root, text=px[int(y), int(x)]).grid(row=2, column=1)


root = Tk()
root.state('zoomed')
current_image = None
converted_image = None
load_menu()


# main loop
root.mainloop()
