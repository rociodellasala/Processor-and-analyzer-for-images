from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image

root = Tk()
# label
label = Label(root, text="Hello RO!")
label.pack()

def read_raw_image(path):
    with open(path, "rb") as binary_file:
        # Read the whole file at once
        raw_image = binary_file.read()
        return raw_image


def open_file_name():
    file_name = filedialog.askopenfilename(title='Choose Image', filetypes=[("ppm", "*.ppm"), ("pgm", "*.pgm"),
                                                                            ("jpg", "*.jpg"), ("png", "*.png"),
                                                                            ("jpeg", "*.jpeg"),("raw", "*.RAW")])
    if file_name:
        return file_name
    else:
        return ""


def load_image():
    file_name = open_file_name()
    if file_name:
        if file_name.endswith(".RAW"):
            raw_image = read_raw_image(file_name)
            print(raw_image)
            # TODO if extension is RAW do this
            image = Image.frombytes('L', (290, 207), raw_image)
        else:
            # opens the image
            image = Image.open(file_name)
        # resize the image and apply a high-quality down sampling filter
        image = image.resize((512, 512), Image.ANTIALIAS)

        # PhotoImage class is used to add image to widgets, icons etc
        image = ImageTk.PhotoImage(image)

        # create a label
        panel = Label(root, image=image)

        # set the image as img
        panel.image = image
        panel.pack()

add_image_button = Button(root, text="Load Image", fg="blue", command=load_image).pack()

# main loop
root.mainloop()
