from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os


def Test():
    pass

class LoadingScreen():
    def __init__(self, work, length):
        self.length = length
        self.lScreen = Toplevel()
        Label(self.lScreen, text="Working").pack()
        self.progress = 0

        self.work  = Label(self.lScreen, text=work).pack()
        
        self.progress_str = StringVar()
        self.progress_str.set(str(self.progress) + ' / ' + str(self.length))
        self.propgressLabel = Label(self.lScreen, text=self.progress_str, textvariable=self.progress_str).pack()

        self.progress_var = DoubleVar()
        self.prog_bar = ttk.Progressbar(self.lScreen, variable=self.progress_var, maximum=length)
        self.prog_bar.pack()

        self.lScreen.pack_slaves()

        self.lScreen.protocol("WM_DELETE_WINDOW", self.destroyed)

    def increaseProgress(self):
        self.progress = self.progress + 1
        if self.progress >= self.length:
            progress = 0
        self.progress_var.set(self.progress)
        self.progress_str.set(str(self.progress) + ' / ' + str(self.length))

    def update(self):
        self.lScreen.update()

    def destroyed(self):
        os._exit(1)
        pass

    def __del__(self):
        self.lScreen.destroy()
        del self
        

class Checkbar(Frame): #https://www.python-kurs.eu/tkinter_checkboxes.php
    def __init__(self, parent=None, picks=[], anchor=W, bg=None, fg=None):
        Frame.__init__(self, parent)
        self.config(bg=bg)
        self.vars = []
        count = 0
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var, bg=bg, fg=fg)
            chk.configure(selectcolor=bg)
            chk.grid(row=count, sticky=W)
 
#           chk.pack( anchor=anchor, expand=YES, fill=X)
            self.vars.append(var)
            count = count + 1
    def state(self):
        return map((lambda var: var.get()), self.vars)



class ToolTip(object):
    def __init__(self, widget, font, size, bg, fg, offX=0, offY=0):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
		
        self.font = font
        self.size = size
        self.bg = bg
        self.fg = fg

        self.offX = offX
        self.offY = offY

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + self.offX
        y = y + cy + self.widget.winfo_rooty() + self.offY
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass

        self.tipwindow.bind('<Leave>', self.leave)
        
        label = Label(tw, text=self.text, justify=LEFT,
                      background=self.bg, fg=self.fg, relief=SOLID, borderwidth=1,
                      font=(self.font, self.size, "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def leave(self, event):
        print("leave")

def createToolTip(widget, text, font="tahoma", size=8, bg="#ffffe0", fg=None, offsetX=0, offsetY=0):
    toolTip = ToolTip(widget, font, size, bg, fg, offsetX, offsetY)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
