from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image

root = Tk()
# label
label = Label(root, text="Hello RO!")
label.pack()


def read_raw_image(path):
    last_slash_position = path.rfind('/')
    info_path = path[0:last_slash_position] + "/info.txt"
    image_map = read_lines(info_path)
    raw_image_info = []
    image_name = path[last_slash_position+1:].replace('.RAW', '')
    with open(path, "rb") as binary_file:
        # Read the whole file at once
        raw_image = binary_file.read()
        raw_image_info.append(raw_image)
    raw_image_info.append(image_map[image_name])
    return raw_image_info


def read_lines(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()
    images = {}
    count = 0
    for line in lines:
        count = count + 1
        if count > 2:
            image_info = get_image_info(line)
            images[image_info[0]] = [image_info[1], image_info[2]]
    return images


def get_image_info(line):
    info = line.replace('\n', '').replace('.RAW', '').split(' ')
    image_info = []
    count = 0
    for value in info:
        if len(value) > 0:
            image_info.append(value)
            count = count + 1
    return image_info


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
