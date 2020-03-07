from tkinter import *

root = Tk()
# label
label = Label(root, text="Hello RO!")
label.pack()

#button
def loadImage():
    print("loading image")

addImageButton = Button(root, text="Load Image", fg="blue", command=loadImage).pack();

#main loop
root.mainloop()