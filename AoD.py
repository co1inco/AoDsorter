import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font as tkfont
import webbrowser
import os.path
import os
from io import BytesIO

from tkWidgets import *
import sqllib

loadGenre = True

pilError = False
try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    pilError = True


global sizeDivide
sizeDivide = 1

urls = ["https://www.anime-on-demand.de", "/animes/", "/animes/genre/"]

global genre
genre = ['Abenteuer', 'Action', 'Comedy',
         'Drama','Erotik',
         'Fantasy', 'Horror',
         'Mystery', 'Romance',
         'Science Fiction', 'Deutsch']

searchTerm = [ ['animebox-title'    , '</h3>'   ,  2,  0],  #Name
               ['animebox-image'    , 'alt'     , 12, -2],  #Image
               ['href'              , '\">'     ,  2,  0],  #Link
               ['animebox-shorttext', '</p>'    ,  2, -1]   #Short description
               ]

global replaceStr
replaceStr = [["&#39;", "'"],
              ["&amp;", "&"],
              ["&quot;", "\""]]


#backgrond colours

theme = {}
theme['bgMain'] = "#353638"
theme['fgMain'] = "white"
theme['buttonBg'] = "#aabe44"     #aabe44 #66cc00
theme['buttonFg'] = "#353638"
theme['entryBg'] = "#aabe44"
theme['entryFg'] = "#353638"
theme['bgSort'] = "#353638"
theme['bgTile1'] = "#353638"
theme['fgTile1'] = "white"
theme['bgTile2'] =  "#353638"
theme['fgTile2'] = "white"
theme['font']    = "Helvetica"
theme['data']    = "img/"
theme['guiScaleDiv'] = 1


global canvasHeight
global canvasWidth
canvasHeight    = int(700   /theme['guiScaleDiv'])
canvasWidth     = int(529*2 /theme['guiScaleDiv'])


class blocks(Frame):
    def __init__(self, app, video, bgType=0, theme=None):
        Frame.__init__(self, app)

        self.video = video

        if theme != None:
            localFont = theme['font']
            self.dataPath = theme['data']
            guiScale = theme['guiScaleDiv']
            buttonBg = theme['buttonBg']
            buttonFg = theme['buttonFg']
            if bgType == 1:
                localBg = theme['bgTile1']
                localFg = theme['fgTile1']
                bgSort = theme['bgSort']
            else:
                localBg = theme['bgTile2']
                localFg = theme['fgTile2']
                bgSort = theme['bgSort']
        else:
            self.dataPath = "img/"
            localBg = None
            localFg = None
            bgSort = None
            buttonBg = None
            buttonFg = None
            guiScale = 1
            localFont = "Helvetica"
#        localFont = "Consolas"

        self.config(bg=localBg, relief="solid", bd=1)


        newName = video.name
        newText = video.text
        for s, r in replaceStr:
            newName = findReplaceString(newName, s, r)
            newText = findReplaceString(newText, s, r)
        hoverLabel=False
        breakName, charCount = lineBreak(newName, 400/guiScale, charCountYes=True,font=localFont, size=int(16/guiScale+1*guiScale))
        if len(charCount) > 1:
            tmpName = breakName
            newName = newName[:int(charCount[0]) - 3] + " ..."
            hoverLabel = True
        name = Label(self, text=newName, justify=LEFT, font=(localFont, int(16/guiScale), "bold"), wraplength = int(500/guiScale), bg=localBg, fg=localFg)
        name.pack(fill=X, side=TOP)

        if hoverLabel:
            createToolTip(name, tmpName, localFont, int(16/guiScale), bg=localBg, fg=localFg, offsetX=27, offsetY=35)


#       body ---
        if not os.path.isfile(theme['data'] + self.video.link[7:] + ".jpg"):
            self.downloadImage()

        try:
            tmpImg = Image.open(theme['data'] + self.video.link[7:] + ".jpg")
        except OSError:
            self.downloadImage()
            tmpImg = Image.open(theme['data'] + self.video.link[7:] + ".jpg")
            
        width, height = tmpImg.size
        size = int(width/guiScale), int(height/guiScale) 
        tmpImg.thumbnail(size, Image.ANTIALIAS) 
        self.img = ImageTk.PhotoImage(tmpImg, master = self)

        if not newText.endswith(".") or not newText.endswith("!") or not newText.endswith("?"): # why dots sometimes missing??
            newText = newText + "."
        tmpText = ""
        hoverlabel = False
        breakText, charCount = lineBreak(newText, 220/guiScale, charCountYes=True,font=localFont, size=int(12/guiScale+1*guiScale))
        if len(charCount) > 8:
            tmpText = breakText
            textLen = 0
            for i in range(0, 8):
                textLen = textLen + charCount[i]
            newText = newText[:textLen] + " (...)"
            hoverLabel = True
        body = Label(self, image = self.img, compound=LEFT, padx = 10,
                      text=newText, justify=LEFT, font=(localFont, int(12/guiScale)), wraplength = int(230/guiScale), bg=localBg, fg=localFg)
        body.pack()
        if hoverLabel:
            createToolTip(body, tmpText, localFont, int(12/guiScale), bg=localBg, fg=localFg, offsetX=27)
#       body ---

        
        emptyText = ""
        """ takes ages to load
        tetx, lines = lineBreak(emptyText, int(529/guiScale), True, size=int(12/guiScale), font="Consolas")
        while len(lines) < 2:
            print(lines)
            emptyText = emptyText + " "
            tetx, lines = lineBreak(emptyText, int(529/guiScale), True, size=int(12/guiScale), font="Consolas")
        """
        for i in range(58):
            emptyText = emptyText + " "
        
        emptyLine = Label(self, text=emptyText, bg = bgSort, font=("Consolas", int(12/guiScale))).pack(side=BOTTOM) 

        button = Button(self, text = "goTo Website", command = self.openLink, bg=buttonBg, fg=buttonFg, font=(localFont, int(12/guiScale)))
        button.config(takefocus=1)
        button.config(width = int(50/guiScale))
        button.pack(side=BOTTOM)
#        button.pack(fill=X, side=BOTTOM)

        genreLabel = Label(self, text=video.getGenre(), justify=LEFT, font=("Helvetica bold", int(12/guiScale)),
                       wraplength = int(500/sizeDivide), bg=localBg, fg=localFg) 
        genreLabel.pack(side=BOTTOM, fill=X)


    def openLink(self):
        link = mainSite + self.video.link
        print(link)
        webbrowser.open_new_tab(link)


    def downloadImage(self):
            print("Downloading Image: " + self.video.name) 
            f = open(theme['data'] + self.video.link[7:] + ".jpg", 'wb')
            try:
                imageFile = urllib.request.urlopen(mainSite + "/" + self.video.image[1:]).read()
                f.write(imageFile)
                f.close()
            except urllib.error.URLError:
                # window, that informs that the download failed
                pass



class TitleList(Frame):
    def  __init__(self, app, theme=None):
        Frame.__init__(self, app)
        self.app = app

        self.theme = theme
        if self.theme != None:
            self.bg = theme['bgSort']
            self.configure(bg=self.bg)

        self.oldMouseMove = 0

    def setup(self):
        self.myframe=Frame(self.app, relief=GROOVE,width=canvasWidth,height=canvasHeight,bd=1, bg=self.bg)
        self.myframe.place(x=0,y=0)

        self.canvas=Canvas(self.myframe, bg=self.bg)
        self.frame=Frame(self.canvas, bg=self.bg)
        self.myscrollbar=Scrollbar(self.myframe,orient="vertical",command=self.canvas.yview, bg=self.bg)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        
        self.myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame.bind("<Configure>", self.myfunction)

#        self.myframe.bind_all("<Button-1>", self._on_button1)    #  touch support at some point?
#        self.myframe.bind_all("<B1-Motion>", self._on_b1_motion)

    def myfunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=canvasWidth, height=canvasHeight)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_button1(self, event):
        self.mouseXold = event.y
        print(self.canvas.yview())

    def _on_b1_motion(self, event):
        if self.mouseXold-event.y > 0:
            self.canvas.yview_scroll(1, "units")
        elif self.mouseXold-event.y < 0:
            self.canvas.yview_scroll(-1, "units")
        self.mouseXold = event.y
        print(event.y)
                
    def buildTitleList(self, animes, aktive, searchName, statusText, statusLabel):
        statusText.set("Working")
        statusLabel.config(fg="red")
        
        sNameStr = searchName.get()
        self.setup()

        selectedGenres = []

        for index, item in enumerate(list(aktive)):
            if item == 1:
                selectedGenres.append(genre[index])

        print("Search Gen: >" + str(selectedGenres) + "<")
        print("Search Str: >" + sNameStr + "<")
        
        if not os.path.exists("img/"):
            os.makedirs("img/")
        print("Loading Images")
    
        addedTileCount = 0
        for index, videoObj in enumerate(videoList):
            if videoObj.checkGenre(selectedGenres) and videoObj.checkName(sNameStr):
                b = blocks( self.frame , videoObj, (int(addedTileCount/2))%2 + addedTileCount%2, theme=self.theme)
                b.grid(sticky="W", row=int(addedTileCount/2), column=int(addedTileCount%2))
                addedTileCount = addedTileCount + 1

                self.update()

        statusText.set("Loaded %i Titel" % addedTileCount)
#        statusText.set("Finished")
        statusLabel.config(fg="green")

        return True
                

class ChooseFrame(Frame):
    def __init__(self, videoList, videoListFrame, genreList, theme=None):
        if theme != None:
            bg = theme['bgMain']
            fg = theme['fgMain']
            butBg = theme['buttonBg']
            butFg = theme['buttonFg']
            textB = theme['entryBg']
            textF = theme['entryFg']
        else:
            bg = None
            fg = None
            butBg = None
            butFg = None
            textB = None
            textF = None
            
        Frame.__init__(self)
        self.config(bg=bg)
        self.checkBts = Checkbar( self , genreList, bg=bg, fg=fg)
        self.checkBts.pack(padx=20)

        searchName = Entry(self, width=20, bg=textB, fg=textF)
        searchName.pack()

        statusStr = StringVar()
        statusStr.set("Waiting")
        statusLabel = Label(self, text=statusStr, textvariable=statusStr, bg=bg, fg=fg)
        statusLabel.pack(side=TOP)

        start = Button( self, text="Start", command=lambda: videoListFrame.buildTitleList(videoList, self.checkBts.state(), searchName, statusStr, statusLabel), bg=bg, fg=fg)
        start.config(bg=butBg, fg=butFg)
        start.pack()


def findReplaceString(string, replace, replaceWith):
    if string.find(replace) > -1:
        newName = ""
        rest = string
    else:
        return string
    length = len(replace)
            
    while True:
        place = rest.find(replace)
        if place < 0:
            return (newName + rest)
        newName = newName + rest[:place] + replaceWith
        rest = rest[place+length:]


def lineBreak(string, wraplenght, charCountYes = False, font = "Helvetica", size=8):
    def charInFont(string, wraplenght, font = "Helvetica", size=8):
        font = tkfont.Font(family=font, size=size)
        i = 0
        while font.measure(string[:i]) < wraplenght:
            i = i + 1
            if i >= len(string):
                break
        return i
    
    charCount = []
    newString = ""
    while True:
        lenght = charInFont(string, wraplenght, size=size)

        if len(string) <= lenght:
            newString = newString + string
            charCount.append(len(string))
            break
        
        currentChar = lenght
        for i in range(lenght, 0, -1):
            if i == 1:
                newString = newString + string[:lenght] + "\n"
                charCount.append(len(string[:lenght]))
                string = string[lenght:]
                break
            if string[i] == " ":
                newString = newString + string[:i] + "\n"
                charCount.append(len(string[:i]))
                string = string[i+1:]
                break

    if charCountYes:
        return newString, charCount
    else:
        return newString


def windowControl(sortWindow, theme=None):
    sortWindow.deiconify()
    sortedList = TitleList(sortWindow, theme)
    sortedList.pack(side=LEFT)
#    sortedList.grid(column=2)

    checkBts = ChooseFrame(videoList, sortedList, genre, theme)
    checkBts.pack(side=RIGHT)
    sortWindow.protocol("WM_DELETE_WINDOW", closeWindow)
    sortWindow.mainloop()


def closeWindow():
    try:
        app.destroy()
    except:
        pass

    try:
        sortWindow.destroy()
    except:
        pass
    os._exit(0)
    

def createSortWindow():
    sortWindow = Tk()
    sortWindow.withdraw()
    sortWindow.title("AoD Sorter")
    sizex = str(canvasWidth+150+20)
    sizey = str(canvasHeight)
    geometry = sizex + "x" + sizey
    sortWindow.geometry(geometry)
    sortWindow.resizable(False, False)
    if os.path.isfile("logo.ico"):
        sortWindow.iconbitmap(os.getcwd() + '/logo.ico')
    return sortWindow


if __name__ == "__main__":
    
    if pilError:
        Tk().withdraw()
        if messagebox.askokcancel("Problem loading PIL",
                                  "Try install pillow via commandline?\n Execute: pip install pillow",
                                  icon='error'):
            os.system("pip install pillow")
            try:
                from PIL import Image, ImageTk
            except:
                messagebox.showerror("Error", "Sorry, still not working")
                raise SystemExit
        else:
            closeWindow()
            raise SystemExit
                                         
        
    mainWindow = createSortWindow() #create and hide sortwindow (if not it would open an emty window while loading)

    loadingScreen = LoadingScreen("Download Anime list", len(genre)+1)
    loadingScreen.update()

#    videoList = get_title_list(urls[0] + urls[1])
#    loadingScreen.increaseProgress()

#    videoList = addGenre(urls, genre, videoList, loadingScreen)
    sqlStuff = sqllib.sqlHandle()
    sqlStuff.updateDatabase(urls, searchTerm, genre, loadingScreen)
#    videoList = sqlStuff.genVideoList()
    videoList = sqlStuff.genGenreList()

    loadingScreen.__del__()

    removed = sqlStuff.getNewOutdated()
    if len(removed) > 0:
        string = ""
        for i in removed:
            string = string + "Removed " + i[0][1] + "\n"
        messagebox.showerror("Removed Title", string)

    mainWindow.config(bg=theme['bgMain'])
    
    windowControl(mainWindow, theme)





