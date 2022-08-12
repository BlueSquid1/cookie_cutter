import os
import glob

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar, filedialog, messagebox

from PIL import Image, ImageTk

import cookie_cutter

def main():

    cc = cookie_cutter.cookieCutter()
    img = cc.readImage('/Users/clinton/Desktop/mygit/cookie_cutter/input_images/A1.tif')

    # A root window for displaying objects
    root = tk.Tk()  

    # Convert the Image object into a TkPhoto object
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im) 

    # Put it in the display window
    ttk.Label(root, image=imgtk).pack() 

    root.mainloop() # Start the GUI

main()