import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

class gui:
    def __init__(self):
        pass

    def splash(self):
        self.window = tk.Tk()
        self.window.geometry("900x500")
        self.window.title('Cookie Cutter')

        splashFrame = ttk.Frame(self.window)

        inputImgLb = ttk.Label(splashFrame, text="input images folder:")
        inputImgLb.grid(column=0, row=0, padx=5, pady=5)
        self.inputImgSv = tk.StringVar(splashFrame, value='/fda')
        inputImgEn = ttk.Entry(splashFrame, textvariable=self.inputImgSv)
        inputImgEn.grid(column=1, row=0, padx=5, pady=5)
        inputBrowseBtn = ttk.Button(splashFrame, text="browse")
        inputBrowseBtn.grid(column=2, row=0, padx=5, pady=5)
        inputBrowseBtn.bind("<Button-1>", self.inputFolderEvent)

        outputImgLb = ttk.Label(splashFrame, text="output images folder:")
        outputImgLb.grid(column=0, row=1, padx=5, pady=5)
        self.outputImgSv = tk.StringVar(splashFrame, value='/fda')
        outputImgEn = ttk.Entry(splashFrame, textvariable=self.outputImgSv)
        outputImgEn.grid(column=1, row=1, padx=5, pady=5)
        outputBrowseBtn = ttk.Button(splashFrame, text="browse")
        outputBrowseBtn.grid(column=2, row=1, padx=5, pady=5)
        outputBrowseBtn.bind("<Button-1>", self.outputFolderEvent)

        splashFrame.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)
        inputBrowseBtn = ttk.Button(self.window, text="done")
        inputBrowseBtn.grid(column=0, row=1, sticky=tk.E, padx=10, pady=5)
        self.window.mainloop()

    def inputFolderEvent(self, event):
        path = filedialog.askdirectory()
        self.inputImgSv.set(path)

    def outputFolderEvent(self, event):
        path = filedialog.askdirectory()
        self.outputImgSv.set(path)
