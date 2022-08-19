import os
import glob

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

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
    notificationSv = None
    
    highPassSigmaSv = None
    highPassSigmaSb = None
    highPassCheckVar = None

    thresholdOffsetSv = None
    thresholdOffsetSb = None

    erosionKernelSv = None
    erosionKernelSb = None

    erosionCheckVar = None
    erosionIterSv = None
    erosionIterSb = None

    dilationCheckVar = None
    dilationKernelSv = None
    dilationKernelSb = None

    dilationIterSv = None
    dilationIterSb = None

    cookieCutter = None
    imageFiles = []
    disableRefresh = False


    def __init__(self):
        self.cookieCutter = cookie_cutter.cookieCutter()

        self.window = tk.Tk()
        self.window.geometry("900x600")
        self.window.title('Cookie Cutter')

    def generateSplashForm(self, parentFrame):
        defaultInputPath = os.getcwd()
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
        pilImg = Image.new('RGB', (600, 500))
        pilImgResized = pilImg.resize((600, 500))
        self.outputPhotoImage = ImageTk.PhotoImage(image=pilImgResized) 
        self.outputImageLb = ttk.Label(previewFrame, image=self.outputPhotoImage)
        self.outputImageLb.grid(column=0, row=0, padx=5, pady=5)
        
        settingsFrame = ttk.Frame(mainFrame)
        settingsFrame.grid(row=0, column=1, padx=5, pady=5)

        # Notification Area
        notificationFrame = ttk.Frame(mainFrame)
        notificationFrame.grid(row=1, column=0, columnspan = 2, sticky="EW")
        self.notificationSv = tk.StringVar(notificationFrame, value="")
        notificationLb = ttk.Label(notificationFrame, textvariable=self.notificationSv)
        notificationLb.grid(column=0, row=0, padx=5, pady=5)


        # Export button
        exportBtn = ttk.Button(settingsFrame, text="Export Image")
        exportBtn.grid(column=0, row=0, padx=5, pady=5, sticky="NS")
        exportBtn.bind("<Button-1>", self.exportImageEvent)

        # Image selector
        ImageSelectorFrame = ttk.Frame(settingsFrame)
        ImageSelectorFrame.grid(row=1, column=0, padx=5, pady=5)
        imageLb = ttk.Label(ImageSelectorFrame, text="Image: ")
        imageLb.grid(column=0, row=0, padx=5, pady=5)
        self.imageNumSv = tk.StringVar(ImageSelectorFrame, value="0")
        self.imageNumSv.trace('w', lambda a, b, c: self.updateView())
        self.imageNumSb = ttk.Spinbox(ImageSelectorFrame, textvariable=self.imageNumSv, width=3, wrap=True)
        self.imageNumSb.grid(row=0, column=1, padx=5, pady=5)
        self.imageTotalSv = tk.StringVar(ImageSelectorFrame, value=" of 0")
        totalLb = ttk.Label(ImageSelectorFrame, textvariable=self.imageTotalSv)
        totalLb.grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)

        # Settings area
        settingsLabelFrame = ttk.LabelFrame(settingsFrame, text="Settings")
        settingsLabelFrame.grid(row=2, column=0, padx=5, pady=5)

        # High pass filter
        self.highPassCheckVar = tk.IntVar(value=True)
        self.highPassCheckVar.trace('w', lambda a, b, c: self.updateView())
        highPassCb = ttk.Checkbutton(settingsLabelFrame, variable=self.highPassCheckVar)
        highPassCb.grid(row=0, column=0, padx=5, pady=5)
        highPassLb = ttk.Label(settingsLabelFrame, text="High Pass Filter")
        highPassLb.grid(row=0, column=1, pady=5, sticky='W')
        highPassSettingsFrame = ttk.Frame(settingsLabelFrame)
        highPassSettingsFrame.grid(row=1, column=1, padx=20)

        highPassValueFrame = ttk.Frame(highPassSettingsFrame)
        highPassValueFrame.grid(row=0, column=0, padx=5, pady=5)
        highPassSigmaLb = ttk.Label(highPassValueFrame, text="Sigma:")
        highPassSigmaLb.grid(row=0, column=0, padx=5)
        self.highPassSigmaSv = tk.StringVar(highPassValueFrame, value="30")
        self.highPassSigmaSv.trace('w', lambda a, b, c: self.updateView())
        self.highPassSigmaSb = ttk.Spinbox(highPassValueFrame, textvariable=self.highPassSigmaSv, width=3, from_ = 1, to= 100)
        self.highPassSigmaSb.grid(row=0, column=1, padx=5)

        # Brightness threshold
        thresholdLb = ttk.Label(settingsLabelFrame, text="Brightness Threshold")
        thresholdLb.grid(row=2, column=1, pady=5, sticky='W')
        thresholdSettingsFrame = ttk.Frame(settingsLabelFrame)
        thresholdSettingsFrame.grid(row=3, column=1, padx=20)

        thresholdOffsetValueFrame = ttk.Frame(thresholdSettingsFrame)
        thresholdOffsetValueFrame.grid(row=0, column=0, padx=5, pady=5)
        thresholdOffsetLb = ttk.Label(thresholdOffsetValueFrame, text="Offset:")
        thresholdOffsetLb.grid(row=0, column=0, padx=5)
        self.thresholdOffsetSv = tk.StringVar(thresholdOffsetValueFrame, value="5")
        self.thresholdOffsetSv.trace('w', lambda a, b, c: self.updateView())
        self.thresholdOffsetSb = ttk.Spinbox(thresholdOffsetValueFrame, textvariable=self.thresholdOffsetSv, width=3, from_ = -255, to= 255)
        self.thresholdOffsetSb.grid(row=0, column=1, padx=5)

        # Erosion
        self.erosionCheckVar = tk.IntVar(value=True)
        self.erosionCheckVar.trace('w', lambda a, b, c: self.updateView())
        erosionCb = ttk.Checkbutton(settingsLabelFrame, variable=self.erosionCheckVar)
        erosionCb.grid(row=4, column=0, padx=5, pady=5)
        erosionLb = ttk.Label(settingsLabelFrame, text="Erosion")
        erosionLb.grid(row=4, column=1, pady=5, sticky='W')
        erosionSettingsFrame = ttk.Frame(settingsLabelFrame)
        erosionSettingsFrame.grid(row=5, column=1, padx=20)

        erosionKernelValueFrame = ttk.Frame(erosionSettingsFrame)
        erosionKernelValueFrame.grid(row=0, column=0, padx=5, pady=5)
        erosionKernelLb = ttk.Label(erosionKernelValueFrame, text="Kernel Size:")
        erosionKernelLb.grid(row=0, column=0, padx=5)
        self.erosionKernelSv = tk.StringVar(erosionKernelValueFrame, value="2")
        self.erosionKernelSv.trace('w', lambda a, b, c: self.updateView())
        self.erosionKernelSb = ttk.Spinbox(erosionKernelValueFrame, textvariable=self.erosionKernelSv, width=3, from_ = 1, to= 100)
        self.erosionKernelSb.grid(row=0, column=1, padx=5)

        erosionIterValueFrame = ttk.Frame(erosionSettingsFrame)
        erosionIterValueFrame.grid(row=1, column=0, padx=5, pady=5)
        erosionIterLb = ttk.Label(erosionIterValueFrame, text="Iterations:")
        erosionIterLb.grid(row=1, column=0, padx=5)
        self.erosionIterSv = tk.StringVar(erosionIterValueFrame, value="2")
        self.erosionIterSv.trace('w', lambda a, b, c: self.updateView())
        self.erosionIterSb = ttk.Spinbox(erosionIterValueFrame, textvariable=self.erosionIterSv, width=3, from_ = 1, to= 100)
        self.erosionIterSb.grid(row=1, column=1, padx=5)

        # dilation
        self.dilationCheckVar = tk.IntVar(value=True)
        self.dilationCheckVar.trace('w', lambda a, b, c: self.updateView())
        dilationCb = ttk.Checkbutton(settingsLabelFrame, variable=self.dilationCheckVar)
        dilationCb.grid(row=6, column=0, padx=5, pady=5)
        dilationLb = ttk.Label(settingsLabelFrame, text="Dilation")
        dilationLb.grid(row=6, column=1, pady=5, sticky='W')
        dilationSettingsFrame = ttk.Frame(settingsLabelFrame)
        dilationSettingsFrame.grid(row=7, column=1, padx=20)

        dilationKernelValueFrame = ttk.Frame(dilationSettingsFrame)
        dilationKernelValueFrame.grid(row=0, column=0, padx=5, pady=5)
        dilationKernelLb = ttk.Label(dilationKernelValueFrame, text="Kernel Size:")
        dilationKernelLb.grid(row=0, column=0, padx=5)
        self.dilationKernelSv = tk.StringVar(dilationKernelValueFrame, value="5")
        self.dilationKernelSv.trace('w', lambda a, b, c: self.updateView())
        self.dilationKernelSb = ttk.Spinbox(dilationKernelValueFrame, textvariable=self.dilationKernelSv, width=3, from_ = 1, to= 100)
        self.dilationKernelSb.grid(row=0, column=1, padx=5)

        dilationIterValueFrame = ttk.Frame(dilationSettingsFrame)
        dilationIterValueFrame.grid(row=1, column=0, padx=5, pady=5)
        dilationIterLb = ttk.Label(dilationIterValueFrame, text="Iterations:")
        dilationIterLb.grid(row=1, column=0, padx=5)
        self.dilationIterSv = tk.StringVar(dilationIterValueFrame, value="3")
        self.dilationIterSv.trace('w', lambda a, b, c: self.updateView())
        self.dilationIterSb = ttk.Spinbox(dilationIterValueFrame, textvariable=self.dilationIterSv, width=3, from_ = 1, to= 100)
        self.dilationIterSb.grid(row=1, column=1, padx=5)

        # Reset button
        resetButton = ttk.Button(settingsLabelFrame, text="Reset All")
        resetButton.grid(row=8, column=1, padx=5, pady=5, sticky="E")
        resetButton.bind("<Button-1>", self.resetAllSettings)

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

    def resetAllSettings(self, event):
        self.disableRefresh = True
        self.highPassSigmaSv.set("30")
        self.highPassCheckVar.set(True)
        self.thresholdOffsetSv.set("5")
        self.erosionKernelSv.set("2")
        self.erosionCheckVar.set(True)
        self.erosionIterSv.set("2")
        self.dilationCheckVar.set(True)
        self.dilationKernelSv.set("5")
        self.disableRefresh = False
        self.dilationIterSv.set("3")

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
        if self.disableRefresh:
            return
        
        # Reset view
        defaultForgroundColor = self.window.option_get("foreground", className='.')
        self.highPassSigmaSb.config(foreground=defaultForgroundColor)
        self.thresholdOffsetSb.config(foreground=defaultForgroundColor)
        self.erosionKernelSb.config(foreground=defaultForgroundColor)
        self.erosionIterSb.config(foreground=defaultForgroundColor)
        self.dilationKernelSb.config(foreground=defaultForgroundColor)
        self.dilationIterSb.config(foreground=defaultForgroundColor)
        self.notificationSv.set("")

        # Update view
        numOfImages = len(self.imageFiles)
        self.imageNumSb.config(from_= 0, to=numOfImages-1)
        self.imageTotalSv.set(" of " + str(numOfImages-1))

        curImageStr = self.imageNumSb.get()
        if not curImageStr.isdigit() or int(curImageStr) < 0 or int(curImageStr) >= numOfImages:
            # Invalid state ignoring
            return

        try:
            ccSettings = self.getCookieCutterSettingsFromForm()

            if ccSettings.enableHighFilterPass:
                self.highPassSigmaSb.config(state="enable")
            else:
                self.highPassSigmaSb.config(state="disable")

            if ccSettings.enableErosion:
                self.erosionKernelSb.config(state="enable")
                self.erosionIterSb.config(state="enable")
            else:
                self.erosionKernelSb.config(state="disable")
                self.erosionIterSb.config(state="disable")

            if ccSettings.enableDilation:
                self.dilationKernelSb.config(state="enable")
                self.dilationIterSb.config(state="enable")
            else:
                self.dilationKernelSb.config(state="disable")
                self.dilationIterSb.config(state="disable")

            imgRgb = self.cookieCutter.generatePreview(self.getCurrentImagePath(), ccSettings)

            pilImg = Image.fromarray(imgRgb)
            pilImgResized = pilImg.resize((600, 500))
            self.outputPhotoImage = ImageTk.PhotoImage(image=pilImgResized)
            self.outputImageLb.config(image=self.outputPhotoImage)
        except Exception as e:
            print(e)
            pass


    def exportImageEvent(self, event):
        inputFilePath = self.getCurrentImagePath()
        fileName = os.path.basename(inputFilePath)
        outputFolder = self.outputImgSv.get()
        outputPath = outputFolder + "/" + fileName

        try:
            ccSettings = self.getCookieCutterSettingsFromForm()
            self.cookieCutter.generateAndSaveBinaryImage(inputFilePath, outputPath, ccSettings)

            notificationMsg = "saved image to: " + outputPath
            print(notificationMsg)
            self.notificationSv.set(notificationMsg)
        except Exception as e:
            # Raise error to user
            messagebox.showerror(title="Failed to export result", message=str(e))
            pass

    def getCookieCutterSettingsFromForm(self):
        ccSettings = cookie_cutter.Settings()
        ccSettings.enableHighFilterPass = bool(self.highPassCheckVar.get())
        ccSettings.highFilterSigma = int(self.getStringVariableValue(self.highPassSigmaSv, self.highPassSigmaSb))
        ccSettings.thresholdOffset = int(self.getStringVariableValue(self.thresholdOffsetSv, self.thresholdOffsetSb))
        ccSettings.enableErosion = bool(self.erosionCheckVar.get())
        ccSettings.erosionKernel = int(self.getStringVariableValue(self.erosionKernelSv, self.erosionKernelSb))
        ccSettings.erosionIter = int(self.getStringVariableValue(self.erosionIterSv, self.erosionIterSb))
        ccSettings.enableDilation = bool(self.dilationCheckVar.get())
        ccSettings.dilationKernel = int(self.getStringVariableValue(self.dilationKernelSv, self.dilationKernelSb))
        ccSettings.dilationIter = int(self.getStringVariableValue(self.dilationIterSv, self.dilationIterSb))
        return ccSettings

    def getStringVariableValue(self, TkStringVar, spinBox):
        stringVar = TkStringVar.get()
        minValue = spinBox.config()['from'][4]
        maxValue = spinBox.config()['to'][4]
        if not stringVar.isdigit() or int(stringVar) < minValue or int(stringVar) > maxValue:
            spinBox.config(foreground="red")
            raise Exception("Invalid settings. Please review settings")
        return int(stringVar)

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
