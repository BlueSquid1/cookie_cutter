import os
import glob

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar, filedialog, messagebox

from PIL import Image, ImageTk

import cookie_cutter

class gui:
    window = None

    #Splash screen variables
    inputImgSv = None
    outputImgSv = None
    splashFrame = None

    inputPhotoImage = None
    outputPhotoImage = None
    outputImageLb = None
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

    def generateSplashForm(self, parentFrame):
        defaultInputPath = os.getcwd() + "/input_images"
        defaultOutputPath = os.getcwd()
        splashFrame = ttk.Frame(parentFrame)
        splashFrame.grid_columnconfigure(0, weight=1)
        splashFrame.grid_rowconfigure(0, weight=1)
        splashFrame.grid(column=0, row=0)

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

    def generateMainFrame(self, parentFrame):
        mainFrame = ttk.Frame(parentFrame)

        mainFrame.grid_columnconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(1, weight=1)
        mainFrame.grid_rowconfigure(0, weight=1)

        previewFrame = ttk.LabelFrame(mainFrame, text="Preview")
        previewFrame.grid(row=0, column=0, padx=5, pady=5)
        pilImg = Image.new('RGB', (600, 600))
        pilImgResized = pilImg.resize((600, 600))
        self.outputPhotoImage = ImageTk.PhotoImage(image=pilImgResized) 
        self.outputImageLb = ttk.Label(previewFrame, image=self.outputPhotoImage)
        self.outputImageLb.grid(column=0, row=0, padx=5, pady=5)
        
        settingsFrame = ttk.Frame(mainFrame)
        settingsFrame.grid(row=0, column=1, padx=5, pady=5)
        settingsLabelFrame = ttk.LabelFrame(settingsFrame, text="Settings")
        settingsLabelFrame.grid(row=0, column=0, padx=5, pady=5)
        imageLb = ttk.Label(settingsLabelFrame, text="Image: ")
        imageLb.grid(column=0, row=0, padx=5, pady=5)

        # Image selector
        self.imageNumSv = tk.StringVar(settingsLabelFrame, value="0")
        self.imageNumSb = ttk.Spinbox(settingsLabelFrame, textvariable=self.imageNumSv, width=3)
        self.imageNumSv.trace('w', lambda a, b, c: self.updateView())
        self.imageNumSb.grid(row=0, column=1, padx=5, pady=5)
        self.imageTotalSv = tk.StringVar(settingsLabelFrame, value=" of 0")
        totalLb = ttk.Label(settingsLabelFrame, textvariable=self.imageTotalSv)
        totalLb.grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)

        # other config

        # Export button
        exportBtn = ttk.Button(settingsFrame, text="Export Image")
        exportBtn.grid(column=0, row=1, padx=5, pady=5, sticky="E")
        exportBtn.bind("<Button-1>", self.exportImageEvent)

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
        
        self.updateView()
        self.mainFrame.tkraise()

    def updateView(self):
        # Update view
        numOfImages = len(self.imageFiles)
        self.imageNumSb.config(from_= 0, to=numOfImages-1)
        self.imageTotalSv.set(" of " + str(numOfImages-1))

        curImageStr = self.imageNumSb.get()
        if not curImageStr.isdigit() or int(curImageStr) < 0 or int(curImageStr) >= numOfImages:
            # Invalid state ignoring
            return

        imgRgb = self.cookieCutter.generatePreview(self.getCurrentImagePath())
        pilImg = Image.fromarray(imgRgb)
        pilImgResized = pilImg.resize((600, 600))
        self.outputPhotoImage = ImageTk.PhotoImage(image=pilImgResized)
        self.outputImageLb.config(image=self.outputPhotoImage)


    def exportImageEvent(self, event):
        inputFilePath = self.getCurrentImagePath()
        fileName = os.path.basename(inputFilePath)
        outputFolder = self.outputImgSv.get()
        outputPath = outputFolder + "/" + fileName
        print(outputPath)

        self.cookieCutter.generateAndSaveBinaryImage(inputFilePath, outputPath)        

    def getCurrentImagePath(self):
        curIndex = int(self.imageNumSb.get())
        return self.imageFiles[curIndex]

    def launch(self):
        self.containerFrame = ttk.Frame(self.window)
        self.containerFrame.pack(side="top", fill="both", expand=True)
        self.containerFrame.grid_rowconfigure(0, weight=1)
        self.containerFrame.grid_columnconfigure(0, weight=1)

        self.splashFrame = self.generateSplashForm(self.containerFrame)   
        self.splashFrame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        self.mainFrame = self.generateMainFrame(self.containerFrame)
        self.mainFrame.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

        self.splashFrame.tkraise()

        self.window.mainloop()
        pass
