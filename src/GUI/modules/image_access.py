from tkinter import filedialog


def open_file_name():
    file_name = filedialog.askopenfilename(title='Choose Image', filetypes=[("ppm", "*.ppm"), ("pgm", "*.pgm"),
                                                                            ("jpg", "*.jpg"), ("png", "*.png"),
                                                                            ("jpeg", "*.jpeg"), ("raw", "*.RAW")])
    if file_name:
        return file_name
    else:
        return ""

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
