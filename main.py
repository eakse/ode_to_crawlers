from tkinter import *
from PIL import Image, ImageTk
 


















exit(0)
# Create Tkinter Object
root = Tk()
 
# Read the Image
image = Image.open("data/images/wall_texture.png")

width = 200
height = 200
# Resize the image using resize() method
resize_image = image.resize((width, height))
 
img = ImageTk.PhotoImage(resize_image)
 
# create label and add resize image
label1 = Label(image=img)
label1.image = img
label1.pack()
 
# Execute Tkinter
root.mainloop()