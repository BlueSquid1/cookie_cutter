import os
import glob

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar, filedialog, messagebox

from PIL import Image, ImageTk

import cookie_cutter

class gui:
    window = None
    inputImgSv = None
    outputImgSv = None

    splashFrame = None
    imageTotalSv = None
    imageNumSb = None
    imageNumSv = None
    containerFrame = None

    cookieCutter = None
    imageFiles = []


    def __init__(self):
        self.cookieCutter = cookie_cutter.cookieCutter()

        self.window = tk.Tk()
        self.window.geometry("900x500")
        self.window.title('Cookie Cutter')

    def generateSplashForm(self):
        defaultInputPath = os.getcwd() + "/input_images"
        defaultOutputPath = os.getcwd()
        splashFrame = ttk.Frame(self.containerFrame)
        splashFrame.grid_columnconfigure(0, weight=1)
        splashFrame.grid_rowconfigure(0, weight=1)

        labelFrame = ttk.LabelFrame(splashFrame, text="Image Folders")
        labelFrame.grid(row=0, column=0)
        inputImgLb = ttk.Label(labelFrame, text="Input Folder:")
        inputImgLb.grid(column=0, row=0, padx=5, pady=5)
        self.inputImgSv = tk.StringVar(labelFrame, value=defaultInputPath)
        inputImgEn = ttk.Entry(labelFrame, textvariable=self.inputImgSv, width=40)
        inputImgEn.grid(column=1, row=0, padx=5, pady=5)
        inputBrowseBtn = ttk.Button(labelFrame, text="browse")
        inputBrowseBtn.grid(column=2, row=0, padx=5, pady=5)
        inputBrowseBtn.bind("<Button-1>", self.inputFolderEvent)

        outputImgLb = ttk.Label(labelFrame, text="Output Folder:")
        outputImgLb.grid(column=0, row=1, padx=5, pady=5)
        self.outputImgSv = tk.StringVar(labelFrame, value=defaultOutputPath)
        outputImgEn = ttk.Entry(labelFrame, textvariable=self.outputImgSv, width=40)
        outputImgEn.grid(column=1, row=1, padx=5, pady=5)
        outputBrowseBtn = ttk.Button(labelFrame, text="browse")
        outputBrowseBtn.grid(column=2, row=1, padx=5, pady=5)
        outputBrowseBtn.bind("<Button-1>", self.outputFolderEvent)

        nextBtn = ttk.Button(labelFrame, text="next")
        nextBtn.grid(column=2, row=2, padx=5, pady=5)
        nextBtn.bind("<Button-1>", self.splashNextEvent)

        return splashFrame

    def generateMainFrame(self):
        mainFrame = ttk.Frame(self.containerFrame)
        displayFrame = ttk.LabelFrame(mainFrame, text="Input Image")
        displayFrame.grid(row=0, column=0, padx=5, pady=5)
        imageArray = self.cookieCutter.readImage("/Users/clinton/Desktop/mygit/cookie_cutter/input_images/A1.tif")
        inputImage = Image.fromarray(imageArray)
        inputPhotoImage = ImageTk.PhotoImage(image=inputImage)
        inputImageLb = ttk.Label(displayFrame, image=inputPhotoImage)
        inputImageLb.pack()
        #inputImageLb.grid(row=0, column=0, padx=5, pady=5)

        previewFrame = ttk.LabelFrame(mainFrame, text="Preview Image")
        previewFrame.grid(row=0, column=1, padx=5, pady=5)
        
        settingsFrame = ttk.LabelFrame(mainFrame, text="Settings")
        settingsFrame.grid(row=0, column=2, padx=5, pady=5)
        imageLb = ttk.Label(settingsFrame, text="Image: ")
        imageLb.grid(column=0, row=0, padx=5, pady=5)
        self.imageNumSv = tk.StringVar(settingsFrame, value="0")
        self.imageNumSb = ttk.Spinbox(settingsFrame, textvariable=self.imageNumSv, width=3)
        self.imageNumSv.trace('w', lambda a, b, c: self.UpdateView())
        self.imageNumSb.grid(row=0, column=1, padx=5, pady=5)

        self.imageTotalSv = tk.StringVar(settingsFrame, value=" of 0")
        totalLb = ttk.Label(settingsFrame, textvariable=self.imageTotalSv)
        totalLb.grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)

        return mainFrame


    def inputFolderEvent(self, event):
        curentPath = self.inputImgSv.get()
        path = filedialog.askdirectory(initialdir=curentPath, title="input folder")
        if len(path) > 0:
            self.inputImgSv.set(path)

    def outputFolderEvent(self, event):
        curentPath = self.outputImgSv.get()
        path = filedialog.askdirectory(initialdir=curentPath, title="output folder")
        if len(path) > 0:
            self.outputImgSv.set(path)

    def splashNextEvent(self, event):
        # Validate splash form
        inputPath = self.inputImgSv.get()
        outputPath = self.outputImgSv.get()
        if inputPath == outputPath:
            messagebox.showerror(title="invalid file paths", message="The input folder can not be the same as the output folder")
            return

        if not os.path.isdir(inputPath):
            messagebox.showerror(title="invalid file paths", message="The input folder needs to point to an existing folder")
            return

        fileTypes = ('*.tif', '*.png', '*.jpg', '*.bmp', '*.jpeg')
        self.imageFiles = []
        for type in fileTypes:
            self.imageFiles.extend(glob.glob(inputPath + "/" + type))

        if len(self.imageFiles) <= 0:
            messagebox.showerror(title="invalid file paths", message="Not images found in input folder")
            return
        
        self.UpdateView()
        self.mainFrame.tkraise()

    def UpdateView(self):
        # Update view
        numOfImages = len(self.imageFiles)
        self.imageNumSb.config(from_= 0, to=numOfImages-1)
        self.imageTotalSv.set(" of " + str(numOfImages-1))

        curImageStr = self.imageNumSb.get()
        if not curImageStr.isdigit() or int(curImageStr) < 0 or int(curImageStr) >= numOfImages:
            # Invalid state ignoring
            print("invalid image index")
            return
        

    def launch(self):
        # img = self.cookieCutter.readImage('/Users/clinton/Desktop/mygit/cookie_cutter/input_images/A1.tif')
        # im = Image.fromarray(img)
        # imgtk = ImageTk.PhotoImage(image=im) 
        # ttk.Label(self.window, image=imgtk).pack()

        self.containerFrame = ttk.Frame(self.window)
        self.containerFrame.pack(side="top", fill="both", expand=True)
        self.containerFrame.grid_rowconfigure(0, weight=1)
        self.containerFrame.grid_columnconfigure(0, weight=1)

        self.splashFrame = self.generateSplashForm()
        self.splashFrame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        self.mainFrame = self.generateMainFrame()
        self.mainFrame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        self.splashFrame.tkraise()

        self.window.mainloop()
        pass
