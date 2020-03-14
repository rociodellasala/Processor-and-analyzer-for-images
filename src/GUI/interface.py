from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image

root = Tk()
# label
label = Label(root, text="Hello RO!")
label.pack()


def read_raw_image(path):
    read_lines('info.txt')
    with open(path, "rb") as binary_file:
        # Read the whole file at once
        raw_image = binary_file.read()
        return raw_image


def read_lines(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()
    images = {}
    count = 0
    for line in lines:
        count = count + 1
        if count > 2:

            imageInfo = get_image_info(line)
            print(line)


def get_image_info(line):
    info = line.replace('\n', '').split(' ')
    print(info)
    count = 0
    for value in info:
        if len(value) > 0:
            count = count + 1;
            print(value)
    return [389, 164]


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
