from tkinter import *  
from PIL import ImageTk,Image  
root = Tk()  

frame = Frame(root)
canvas = Canvas(frame, width = 300, height = 300)  
canvas.pack()  
frame.pack()


img = ImageTk.PhotoImage(Image.open("images/no-camera.png"))  
canvas.create_image(20, 20, anchor="nw", image=img) 
root.mainloop() 