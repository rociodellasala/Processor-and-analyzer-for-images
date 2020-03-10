from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image

root = Tk()
# label
label = Label(root, text="Hello RO!")
label.pack()

def openFileName():
    filename = filedialog.askopenfilename(title='"pen')
    return filename

def loadImage():
    fileName = openFileName()
    # opens the image
    image = Image.open(fileName)

    # resize the image and apply a high-quality down sampling filter
    image = image.resize((512, 512), Image.ANTIALIAS)

    # PhotoImage class is used to add image to widgets, icons etc
    image = ImageTk.PhotoImage(image)

    # create a label
    panel = Label(root, image=image)

    # set the image as img
    panel.image = image
    panel.pack()

addImageButton = Button(root, text="Load Image", fg="blue", command=loadImage).pack()

# #image
# image = ImageTk.PhotoImage(Image.open('../../images/Lenaclor.ppm'))
# imageLabel = Label(image=image)
# imageLabel.pack()

#main loop
root.mainloop()