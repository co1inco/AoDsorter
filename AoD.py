import urllib.request
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

loadGenre = False

pilError = False
try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    pilError = True


global sizeDivide
sizeDivide = 1


global canvasHeight
global canvasWidth
canvasHeight    = int(700   /sizeDivide)
canvasWidth     = int(529*2 /sizeDivide)


global mainSite
global mainList
global genreList

mainSite = "https://www.anime-on-demand.de"
mainList = "/animes/"
genreList = "/animes/genre/"


global genre
genre = ['Abenteuer', 'Action', 'Comedy',
         'Drama','Erotik',
         'Fantasy', 'Horror',
         'Mystery', 'Romance',
         'Science Fiction', 'Deutsch']

global searchTerm
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

global colors #(mostly called theme
colors = {}
colors['bgMain'] = None
colors['fgMain'] = None
colors['button'] = "grey"
colors['bgSort'] = "white"
colors['bgTile1'] = "white"
colors['fgTile1'] = None
colors['bgTile2'] = "grey"
colors['fgTile2'] = "black"
colors['font']    = "Helvetica"


class blocks(Frame):
    def __init__(self, app, video, bgType, theme=None):
        Frame.__init__(self, app)

        self.link = video.link

        if theme != None:
#            localFont = theme['font']
            if bgType == 1:
                localBg = theme['bgTile1']
                localFg = theme['fgTile1']
                bgSort = theme['bgSort']
            else:
                localBg = theme['bgTile2']
                localFg = theme['fgTile2']
                bgSort = theme['bgSort']
        else:
            localBg = None
            localFg = None
            bgSort = None
        localFont = "Helvetica"
#        localFont = "Consolas"
        self.config(bg=localBg)

        newName = video.name
        newText = video.text
        for s, r in replaceStr:
            newName = findReplaceString(newName, s, r)
            newText = findReplaceString(newText, s, r)
        
        cutoff = 45
        hoverLabel=False
        if len(newName) > cutoff/sizeDivide:
            tmpName = newName
            newName = newName[:int(cutoff/sizeDivide) - 3] + " ..."
            hoverLabel = True


        name = Label(self, text=newName, justify=LEFT, font=(localFont, int(16/sizeDivide), "bold"), wraplength = int(500/sizeDivide), bg=localBg, fg=localFg)
        name.pack(fill=X, side=TOP)

        if hoverLabel:
            createToolTip(name, tmpName)

        #   video.image[-10:]
        if not os.path.isfile("img/" + video.link[7:] + ".jpg"):
            print("Downloading Image: " + video.name) 
            f = open('img/' + video.link[7:] + ".jpg", 'wb')
            imageFile = urllib.request.urlopen(mainSite + video.image[1:]).read()
            f.write(imageFile)
            f.close()
            
        tmpImg = Image.open('img/' + video.link[7:] + ".jpg")
        width, height = tmpImg.size
        size = int(width/sizeDivide), int(height/sizeDivide) 
        tmpImg.thumbnail(size, Image.ANTIALIAS) 
        self.img = ImageTk.PhotoImage(tmpImg, master = self)

        if not newText.endswith(".") or not newText.endswith("!") or not newText.endswith("?"): # why dots sometimes missing??
            newText = newText + "."
        tmpText = ""
        hoverlabel = False
        breakText, charCount = lineBreak(newText, 220/sizeDivide, charCountYes=True,font=localFont, size=int(12/sizeDivide))
        if len(charCount) > 8:
            tmpText = breakText
            textLen = 0
            for i in range(0, 8):
                textLen = textLen + charCount[i]
            newText = newText[:textLen] + " (...)"
            hoverLabel = True
        body = Label(self, image = self.img, compound=LEFT, padx = 10,
                      text=newText, justify=LEFT, font=(localFont, int(12/sizeDivide)), wraplength = int(230/sizeDivide), bg=localBg, fg=localFg)
        body.pack()
        if hoverLabel:
            createToolTip(body, tmpText)

        emptyText = ""
        for i in range(58):
            emptyText = emptyText + " "
        emptyLine = Label(self, text=emptyText, bg = bgSort, font=("Consolas", int(12/sizeDivide))).pack(side=BOTTOM)

        button = Button(self, text = "goTo Website", command = self.openLink, bg=localBg, fg=localFg)
        button.pack(fill=X, side=BOTTOM)

        genreLabel = Label(self, text=video.getGenre(), justify=LEFT, font=("Helvetica bold", int(12/sizeDivide)),
                       wraplength = int(500/sizeDivide), bg=localBg, fg=localFg)
        genreLabel.pack(side=BOTTOM, fill=X)


    def openLink(self):
        link = mainSite + self.link
        print(link)
        webbrowser.open_new_tab(link)



class TitleList(Frame):
    def  __init__(self, app, theme=None):
        Frame.__init__(self, app)
        self.app = app

        self.theme = theme
        if self.theme != None:
            self.bg = theme['bgSort']
            self.configure(bg=self.bg)

    def setup(self):
        self.myframe=Frame(self.app, relief=GROOVE,width=canvasWidth,height=canvasHeight,bd=1)
        self.myframe.place(x=0,y=0)

        self.canvas=Canvas(self.myframe)
        self.frame=Frame(self.canvas)
        self.myscrollbar=Scrollbar(self.myframe,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)

        self.myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame.bind("<Configure>", self.myfunction)

    def myfunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=canvasWidth, height=canvasHeight)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                
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

        statusText.set("Finished")
        statusLabel.config(fg="green")

        return True
                
   
        
class Video():
    def __init__(self, name, image, link, text):
        
        self.name = name
        self.image = image
        self.link = link
        self.text = text
        self.img = None

        self.genre = []

    def getGenre(self):
        return self.genre

    def addGenre(self, genre):
        self.genre.append(genre)

    def checkGenre(self, genres):
        inGenres = True
        i = 0
        for x in genres:
            inGenres = False
            j = 0
            for y in self.genre:
                if genres[i] == self.genre[j]:
                    inGenres = True
                    break
                j = j + 1
            if not inGenres:
                break
            i = i + 1
        return inGenres

    def checkName(self, searchName):
        name = self.name.lower()
        sName = searchName.lower()
        if name.find(sName) > -1:
            return True
        else:
            return False


class ChooseFrame(Frame):
    def __init__(self, videoList, videoCanvas, genreList, theme=None):
        if theme != None:
            bg = theme['bgMain']
            fg = theme['fgMain']
        else:
            bg = None
            fg = None
            
        Frame.__init__(self)
        self.config(bg=bg)
        self.checkBts = Checkbar( self , genreList, bg=bg, fg=fg)
        self.checkBts.pack()

        searchName = Entry(self, width=20)
        searchName.pack()

        statusStr = StringVar()
        statusStr.set("Waiting")
        statusLabel = Label(self, text=statusStr, textvariable=statusStr, bg=bg, fg=fg)
        statusLabel.pack(side=TOP)

        start = Button( self, text="Start", command=lambda: videoCanvas.buildTitleList(videoList, self.checkBts.state(), searchName, statusStr, statusLabel), bg=bg, fg=fg)
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

    

def get_part(file, searchFor):
    termLen = len(searchFor[0])
    
    start = file.find(searchFor[0]) + termLen + searchFor[2]
    file = file[start:]
    end = file.find(searchFor[1]) + searchFor[3]
    out = file[:end]

    return out, file


def get_title_list(url):
    print(url)

#    name = 'animebox-title'
#    image = 'animebox-image'
#    link = 'href'               # 'animebox-link'
#    short = 'animebox-shorttext'
    
    site = urllib.request.urlopen(url)
    text = site.read().decode("utf8")
    print("Main list download Finished")

    a = []

    Start = 1
    while Start > -1:

        aName, text = get_part(text, searchTerm[0])

        aImage, text = get_part(text, searchTerm[1])

        aLink, text = get_part(text, searchTerm[2])

        aShort, text = get_part(text, searchTerm[3])

        a.append(Video(aName, aImage, aLink, aShort))
        Start = text.find(searchTerm[0][0])
    print("Main list processing Finished")
    return a


def addGenre(url, genre, Animes): #gives back the full list and added genres |gets only one genre not a list

    k = genre.find(' ')
    
    urlGenre = genre
    if k > 0:
        urlGenre = genre[:k]+'%20'+genre[k+1:]
    if genre == "Deutsch":
        urlGenre = "nonomu"        
    
    name = 'animebox-title'
    
    termLen = len(name)
    
    site = urllib.request.urlopen(url + urlGenre)
    text = site.read().decode("utf8")
    print(genre + " Download Finished")

    title = []
    start = 1
    while start > -1:
        aName, text = get_part(text, searchTerm[0])
        title.append(aName)
        start = text.find(name)

    for i in Animes:
        try:
            if i.name == title[0]:
                i.addGenre(genre)
                title.pop(0)
        except IndexError:
            break
    return Animes
         

def windowControl(sortWindow, theme=None):
 
    sortWindow.deiconify() #make the sortWindow visible == "create"
    
    sortedList = TitleList(sortWindow, theme)
    sortedList.pack(side=LEFT)
#    sortedList.grid(column=2)

    checkBts = ChooseFrame(videoList, sortedList, genre, colors)
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
    sortWindow.title("AoD Sorter")
#    sortWindow.geometry("200x310")
    sizex = str(canvasWidth+150)
    sizey = str(canvasHeight)
    geometry = sizex + "x" + sizey
    sortWindow.geometry(geometry)
    sortWindow.resizable(False, False)
    sortWindow.withdraw()
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

    videoList = get_title_list(mainSite + mainList)
    loadingScreen.increaseProgress()

    for index, item in enumerate(genre):
        if loadGenre == False:
            break
        loadingScreen.update()
        if genre[index] == "Deutsch":
            middel = mainList
        else:
            middel = genreList
        videoList = addGenre(mainSite + middel, genre[index], videoList)
        loadingScreen.increaseProgress()

    loadingScreen.__del__()


    mainWindow.config(bg=colors['bgMain'])
    
    windowControl(mainWindow, colors)





