import tkinter

from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from pathlib import Path
from tkinter.messagebox import showinfo

#import midiToBom
import os


class Menubar(ttk.Frame):
    """Builds a menu bar for the top of the main window"""
    def __init__(self, parent, *args, **kwargs):
        ''' Constructor'''
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_menubar()

    def on_exit(self):
        '''Exits program'''
        quit()

    def display_about(self):
        '''Displays help document'''
        #self.new_win = tkinter.Toplevel(self.root) # Set parent
        os.system("start " + "about.txt")
        pass


    def init_menubar(self):
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar) # Creates a "File" menu
        self.menu_file.add_command(label='Exit', command=self.on_exit) # Adds an option to the menu
        self.menubar.add_cascade(menu=self.menu_file, label='File') # Adds File menu to the bar. Can also be used to create submenus.

        self.menu_help = tkinter.Menu(self.menubar)
        self.menu_help.add_command(label='Open About .txt', command=self.display_about)
        self.menubar.add_cascade(menu=self.menu_help, label='About')

        self.root.config(menu=self.menubar)


def browseFiles():
    workingdir = Path.cwd()
    filename = filedialog.askopenfilename(initialdir = workingdir,
                                          title = "Select a File",
                                          filetypes = (("Images","*.jpg*"), ("Images","*.jpeg*"))
                                        )
    return str(filename)


class GUI(ttk.Frame):
    """Main GUI class"""
    def __init__(self, parent, tosc, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.tosc = tosc
        self.root = parent
        self.fileName = ""
        self.fileNameBom = ""
        self.init_gui()

    def browseImage(self):
        self.fileName = browseFiles()
        self.tosc.image_path = self.fileName.split(".")[0]
        self.renderImage()

    def renderImage(self):
        self.image_file = Image.open(self.fileName)
        self.render = ImageTk.PhotoImage(self.image_file)
        self.img = ttk.Label(self, image=self.render)
        self.img.place(x=0, y=0)
        self.gridLayout()

    def gridLayout(self):
        self.button_browse.grid(row=1, column=0, sticky='ew')
        self.button_convert.grid(row=2, column=0, sticky='ew')
        self.img.grid(row=3, column=0, sticky='ew')
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def convert(self):
        self.tosc.pixelateImage()
        self.tosc.draw()
        self.tosc.save()

        self.render = ImageTk.PhotoImage(self.tosc.image_pixelated)
        self.img = ttk.Label(self, image=self.render)
        self.img.place(x=0,y=0)
        self.gridLayout()

        showinfo("Done", "File was converted")

    def init_gui(self):
        self.root.title("Image to TOSC")
        #self.root.wm_iconbitmap('bbicon.ico')

        windowSize = "512x512"
        
        self.root.geometry(windowSize)
        self.grid(column=0, row=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1) # Allows column to stretch upon resizing
        self.grid_rowconfigure(0, weight=1) # Same with row
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
        
        # Menu Bar
        self.menubar = Menubar(self.root)
        
        # Create Widgets

        self.button_browse = ttk.Button(self, text='Browse image', command=self.browseImage)

        self.button_convert = ttk.Button(self, text='Convert', command= self.convert)

        self.fileName = f"{self.tosc.image_path}.jpg"
        self.renderImage()
        self.gridLayout()

            

def start(tosc):    
    root = tkinter.Tk()
    GUI(root, tosc)
    root.mainloop()
