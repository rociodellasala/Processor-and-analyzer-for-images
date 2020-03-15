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
        px = image.load()
        print(px[4, 4])
        print(px)
        # PhotoImage class is used to add image to widgets, icons etc
        image = ImageTk.PhotoImage(image)
        # create a label
        panel = Label(root, image=image)
        # set the image as img
        panel.image = image
        panel.grid(row=3, column=0, columnspan=4, rowspan=4)
        load_pixel_input()


def save_image():
    image = Image.open('../../images/Lenaclor.ppm')
    image_info = image.filename = asksaveasfilename(initialdir="/", title="Select file", filetypes=(
        ('jpg', '*.jpg'), ('jpeg', '*.jpeg') ('png', '*.png'), ('ppm', '*.ppm'), ("pgm", "*.pgm")))
    image.save(image_info)


def load_menu():
    menubar = Menu(root)
    root.config(menu=menubar)
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Image", menu=file_menu)
    file_menu.add_command(label="Open", command=load_image)
    file_menu.add_command(label="Save", command=save_image)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)


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
    height = Entry(root)
    width = Entry(root)
    height.grid(row=0, column=1)
    width.grid(row=1, column=1)
    Button(root, text="Get Value").grid(row=2, column=0)


root = Tk()
root.state('zoomed')
load_menu()


# main loop
root.mainloop()
