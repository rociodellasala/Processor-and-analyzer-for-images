from tkinter import *
from PIL import ImageTk,Image

root = Tk()
# label
label = Label(root, text="Hello RO!")
label.pack()

#button
def loadImage():
    print("loading image")

addImageButton = Button(root, text="Load Image", fg="blue", command=loadImage).pack()

#image
image = ImageTk.PhotoImage(Image.open('../../images/Lenaclor.ppm'))
imageLabel = Label(image=image)
imageLabel.pack();
#main loop
root.mainloop()