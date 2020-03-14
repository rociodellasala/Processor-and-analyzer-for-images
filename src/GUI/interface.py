from read_raw_image import *
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image

root = Tk()
# label
label = Label(root, text="Hello RO!")
label.pack()


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
            image = Image.frombytes('L', (int(raw_image[1][0]), int(raw_image[1][1])), raw_image[0])
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
