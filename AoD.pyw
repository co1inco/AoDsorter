import urllib.request
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import os.path
import os
from io import BytesIO

pilError = False
try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    pilError = True

global height
global width
height = 700
width=540*2

global mainSite
global mainList
global genreList

mainSite = "https://www.anime-on-demand.de/"
mainList = "animes/"
genreList = "animes/genre/"

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
              ["&amp;", "&"]]


#backgrond colours
global bgMain
global bgSort
global bgTile1
global bgTile2

bgMain = None
bgSort = None
bgTile1 = None
bgTile2 = None


class blocks(Frame):
    def __init__(self, app, video, bgType):
        Frame.__init__(self, app)

        self.link = video.link

        if bgType == 1:
            backgrond = bgTile1
        else:
            backgrond = bgTile2

        newName = video.name
        newText = video.text
        for s, r in replaceStr:
            newName = findReplaceString(newName, s, r)
            newText = findReplaceString(newText, s, r)

        name = Label(self, text=newName, justify=LEFT, font=("Helvetica bold", 16), wraplength = 500, bg=backgrond)
        name.pack(fill=X, side=TOP)

        #video.image[-10:]
        if not os.path.isfile("img/" + video.link[7:] + ".jpg"):
            print("Downloading Image: " + video.name) 
            f = open('img/' + video.link[7:] + ".jpg", 'wb')
            imageFile = urllib.request.urlopen(mainSite + video.image[1:]).read()
            f.write(imageFile)
            f.close()
        
        self.img = ImageTk.PhotoImage(Image.open('img/' + video.link[7:] + ".jpg"), master = self)

        body = Label(self, image = self.img, compound=LEFT, padx = 10,
                      text=newText, justify=LEFT, font=("Helvetica", 12), wraplength = 250, bg=backgrond)
        body.pack()

 
        emtyLine = Label(self, text=' ', bg = bgSort).pack(side=BOTTOM)
        
        button = Button(self, text = "goTo Website", command = self.openLink)
        button.pack(fill=X, side=BOTTOM)

        genreLabel = Label(self, text=video.getGenre(), justify=LEFT, font=("Helvetica bold", 12),
                           wraplength = 500, bg=backgrond)
        genreLabel.pack(side=BOTTOM, fill=X)

#        panel = Label(self, image = self.img).pack(side=LEFT)
 #       topline = Label(self, text=video.text, justify=LEFT, font=("Helvetica", 12), wraplength = 250)
 #       topline.pack(side=TOP)

    def openLink(self):
        link = mainSite + self.link
        print(link)
        webbrowser.open_new_tab(link)
        
        
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

#        aName, text = get_part(text, name, '</h3>', 2, 0)

#        aImage, text = get_part(text, image, 'alt', 12, -2)

#        aLink, text = get_part(text, link, '\">', 2, 0)

#        aShort, text = get_part(text, short, '</p>', 2, -1)

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

def buildTitleList(app, animes, genre):

    global canvas

    def myfunction(event):
        canvas.configure(scrollregion=canvas.bbox("all"),width=width,height=height)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    myframe=Frame(app, relief=GROOVE,width=width,height=height,bd=1)
    myframe.place(x=0,y=0)

    canvas=Canvas(myframe)
    frame=Frame(canvas)
    myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left")
    canvas.create_window((0,0),window=frame,anchor='nw')
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    frame.bind("<Configure>",myfunction)
    
    frame.configure(bg = bgSort)

    if not os.path.exists("img/"):
        os.makedirs("img/")
    print("Loading Images")

#    loadingScreen = LoadingScreen("Download Anime list", 3)
    
    addedTileCount = 0
    for index, videoObj in enumerate(videoList):
#        loadingScreen.increaseProgress()
#        loadingScreen.update()
        if videoObj.checkGenre(genre):
            b = blocks( frame , videoObj, (int(addedTileCount/2))%2 + addedTileCount%2)
            b.configure(bg=bgSort)
            b.grid(sticky="W", row=int(addedTileCount/2), column=int(addedTileCount%2))
            addedTileCount = addedTileCount + 1

            app.update()
#    loadingScreen.__del__()

class Checkbar(Frame): #https://www.python-kurs.eu/tkinter_checkboxes.php
   def __init__(self, parent=None, picks=[], anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      count = 0
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var, bg = bgMain)
         chk.grid(row=count, sticky=W)
 
#         chk.pack( anchor=anchor, expand=YES, fill=X)
         self.vars.append(var)
         count = count + 1
   def state(self):
      return map((lambda var: var.get()), self.vars)

def windowControl(genre):

    def openList(genres, aktive):
        selectedGenres = []

        for index, item in enumerate(list(aktive)):
            if item == 1:
                selectedGenres.append(genres[index])

        print(selectedGenres)

        global app
        try:
            app.destroy()
        except:
            pass
        app = Tk()
        app.title("AoD List")

        app.geometry("1102x703")
        app.configure(bg=bgSort)
            
        app.resizable(False, False)
        buildTitleList(app, videoList, selectedGenres)

   
    sortWindow.deiconify() #make the sortWindow visible == "create"
    
    checkBts = Checkbar(sortWindow, genre)
    checkBts.pack()

    start = Button(sortWindow, text="Start", command=lambda: openList(genre, checkBts.state())).pack()

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

def createSortWindow():
    global sortWindow
    sortWindow = Tk()
    sortWindow.title("AoD Sorter")
    sortWindow.geometry("200x310")
    sortWindow.resizable(False, False)
    sortWindow.configure(bg=bgMain)
    sortWindow.withdraw()


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
                                         
        
    createSortWindow() #create and hide sortwindow (if not it would open an emty window while loading)

    loadingScreen = LoadingScreen("Download Anime list", len(genre)+1)

    videoList = get_title_list(mainSite + mainList)
    loadingScreen.increaseProgress()

    for index, item in enumerate(genre):
        
        loadingScreen.update()

        if genre[index] == "Deutsch":
            middel = mainList
        else:
            middel = genreList

        videoList = addGenre(mainSite + middel, genre[index], videoList)

        loadingScreen.increaseProgress()

    loadingScreen.__del__()

    
    windowControl(genre)





