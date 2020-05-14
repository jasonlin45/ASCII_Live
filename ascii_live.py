import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageDraw
import time
import numpy

class Ascii_Live_Simple:
    def __init__(self, window, window_title, preview=True):

        self.window = window
        self.window.title(window_title)
        self.preview = preview

        # open webcam
        self.vid = VideoCapture()

        
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        if(self.preview):
            # Create a canvas for input
            in_label = tk.Label(window, text="Webcam Input", font=("Helvetica", 16))
            in_label.grid(row=0, column=0)
            self.canvas.grid(row=1, column=0, rowspan=4)




            # Create an output preview
            self.preview = tk.Frame(window, width = self.vid.width, height = self.vid.height)
            out_label = tk.Label(window, text="Estimated Output", font=("Helvetica", 16))
            self.preview.columnconfigure(0, weight=10)
            self.preview.grid_propagate(False)
            out_label.grid(row=0, column=1)
            
            # Output preview as a label
            self.ascii = tk.Label(self.preview, text="fwafwfawfwa", font=("Courier",8))
            self.ascii.grid(sticky="W")
            self.preview.grid(row=1, column=1, rowspan=4)
        else:
            # todo scale video dynamically with window width / height
            self.preview = tk.Frame(window, width = self.window.winfo_screenwidth(), height = self.window.winfo_screenheight())
            out_label = tk.Label(window, text="ASCII Live", font=("Courier", 16))
            self.preview.columnconfigure(0, weight=10)
            self.preview.grid_propagate(False)
            out_label.grid(row=0, column=0)

            # Output preview as a label
            self.ascii = tk.Label(self.preview, text="fwafwfawfwa", font=("Courier",6))
            self.ascii.grid()
            self.preview.grid(row=1, column=0)

        # 30 millisecond delay (approx 30 fps)
        self.delay = 30
        self.update()
 
        self.window.mainloop()            

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
         
        if ret:
            self.image = cv2.cvtColor(frame, cv2.cv2.COLOR_RGB2BGR)
            self.grey = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), (int(self.vid.width/3), int(self.vid.height/4)))[32:100, 0:213]
            #self.terminal = self.grey[80:360, 0:640]
            #self.terminal = cv2.resize(self.terminal,(30,25))
            self.levels = "@%#*+=-:. "
            #self.levels = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
            #self.ascii = Image.new('RGB', (int(self.vid.width), int(self.vid.height)), color = (0, 0, 0))
            #d = ImageDraw.Draw(self.ascii)
            out = ""
            for i in range(len(self.grey)):
                for j in range(len(self.grey[0])):
                    value = int(round(self.grey[i][j] / 255 * len(self.levels))) - 1 
                    if(value<0):
                        value=0
                    out += self.levels[value]
                #d.text((int(self.vid.width/3), i*3), line, fill=(255,255,255))
                out+="\n"
            out = out.strip()

            # term = ""
            # for i in range(len(self.terminal)):
            #     line = ""
            #     for j in range(len(self.terminal[0])):
            #         value = int(round(self.terminal[i][j] / 255 * len(self.levels))) - 1 
            #         if(value<0):
            #             value=0
            #         line += self.levels[value]
            #     #d.text((int(self.vid.width/3), i*3), line, fill=(255,255,255))
            #     line = line[0:80]
            #     term = term + line+"\n"
            # term = out.strip()
            # print(term)
            self.ascii.configure(text=out)
            while(self.ascii.cget("text")!=out):
                self.delay = 30
            
            if(self.preview):
                #self.ascii = numpy.array(self.ascii)
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                #self.ascii = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.ascii))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
                #self.preview.create_image(0, 0, image = self.ascii, anchor = tk.NW)

        self.window.after(self.delay, self.update)

 
class VideoCapture:
    def __init__(self):
        # Open default webcam
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open webcam", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
 
# run the app!
Ascii_Live_Simple(tk.Tk(), "ASCII Live", False)

