# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 18:00:47 2020

@author: dykua

TKinter GUI for the style transfer
"""

from tkinter import *
from tkinter import filedialog
from Style_Transfer_Cam import style_transfer_cam
import cv2

def browse_file(entry):
    def browse():
        fname = filedialog.askopenfilename()
        entry.insert(0, fname)
    return browse

class Main_window(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.master.title("Style Transfer -- MAIN") 
        
        # output image size
        wLabel = Label(self.master, text="Width:")
        hLabel = Label(self.master, text="Height:")
        self.w = StringVar()
        self.h = StringVar()
        wEntry = Entry(self.master, textvariable=self.w, width=10)
        wEntry.insert(END, '400')
        hEntry = Entry(self.master, textvariable=self.h, width=10)
        hEntry.insert(END, '300')
        
        # browse video/image file
        inputLabel = Label(self.master, text="Input video/image file: ")
        
        self.input_file = StringVar()
        inputEntry = Entry(self.master, textvariable=self.input_file, width=40)

        inputButton = Button(self.master, text="BROWSE", command = browse_file(inputEntry))
                       
        # browse style file
        styleLabel = Label(self.master, text="Style image file: ")
        
        self.style_file = StringVar()
        styleEntry = Entry(self.master, textvariable=self.style_file, width=40)
        styleEntry.insert(0, './style_images/mosaic.jpg')

        styleButton = Button(self.master, text="BROWSE", command = browse_file(styleEntry))
        
        # write to file
        saveLabel = Label(self.master, text="Save as: ")
        
        self.save_file = StringVar()
        saveEntry = Entry(self.master, textvariable=self.save_file, width=40)
       
        # Radio button: camera, video, image
        TypeLabel = Label(self.master, text="Input Type:")
        self.input_option= IntVar()
        def feed_check():
            if self.input_option.get() == int(0):
               inputEntry.config(state=DISABLED)
                
            elif self.input_option.get() in [int(1), int(2)]:
               inputEntry.config(state=NORMAL)
            
            else:
                exit("Invalide value encountered!")
                
        
        opt_Button_0 = Radiobutton(self.master, text="Camera", variable=self.input_option,
                                   indicatoron=False, value= int(0), width=8, command = feed_check)
        opt_Button_1 = Radiobutton(self.master, text="Video", variable=self.input_option,
                                   indicatoron=False, value= int(1), width=8, command = feed_check)  
        opt_Button_2 = Radiobutton(self.master, text="Image", variable=self.input_option,
                                   indicatoron=False, value= int(2), width=8, command = feed_check) 
       
        
        # Confirm/Quit
        out_size = ( int(self.w.get()), int(self.h.get()) )
        self.transformer = style_transfer_cam( img_size = out_size )
        def confirm():
            option = self.input_option.get()
            if self.save_file.get() == '':
                savetofile = None
            else:
                savetofile = self.save_file.get()
            if option == int(0):
                self.transformer.run(feed = cv2.VideoCapture(0), 
                                     style_path= self.style_file.get(), 
                                     write_to = savetofile)
            elif option == int(1):
                self.transformer.run(feed = cv2.VideoCapture(self.input_file.get()), 
                                     style_path= self.style_file.get(), 
                                     write_to = savetofile)
            elif option == int(2):
                self.transformer.transfer_image(self.input_file.get(), 
                                                style_path= self.style_file.get(),
                                                write_to = savetofile)
            
        def quit():
            self.master.destroy()
            
        runButton = Button(self.master, text = "Run", command = confirm)
        QButton = Button(self.master, text = "Quit", command = quit)
        
        # grid arrangement
        TypeLabel.grid(row=0)
        opt_Button_0.grid(row=0, column=1)
        opt_Button_1.grid(row=0, column=2)
        opt_Button_2.grid(row=0, column=3)
        
        wLabel.grid(row=1)
        wEntry.grid(row=1, column = 1)
        hLabel.grid(row=1, column = 2)
        hEntry.grid(row=1, column = 3)
        
        inputLabel.grid(row=2)
        inputEntry.grid(row=2, column=1, columnspan=3)
        inputButton.grid(row=2, column=4)
        
        styleLabel.grid(row=3)
        styleEntry.grid(row=3, column=1, columnspan=3)
        styleButton.grid(row=3, column=4)
        
        saveLabel.grid(row=4)
        saveEntry.grid(row=4, column=1, columnspan=3)
        # saveButton.grid(row=4, column=4)
        
        runButton.grid(row=6, column=4)
        QButton.grid(row=6, column=5)

def make_gui():
    main_window = Tk()
    main_window.geometry("640x480")
    MW = Main_window(main_window)
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            main_window.destroy()

    main_window.protocol("WM_DELETE_WINDOW", on_closing)
    main_window.mainloop()
    
    return MW
    
if __name__ == '__main__':
    mw = make_gui()
