from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from  PyQt5 import QtCore

import os, os.path, sys
import webbrowser, urllib

import time
import random

import sqllib


global urls
urls = ["https://www.anime-on-demand.de", "/animes/", "/animes/genre/"]

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
               ['zu'                , '</a>'    ,  2,  0],  #film/serie
               ['animebox-shorttext', '</p>'    ,  2, -1]   #Short description
               ]

global theme
theme = {}
theme['imageSize'] = [130, 73, 2, 2] #last is additional font scaling after using normal scaling(#3)
theme['bgMain'] = "#353638"
theme['fgMain'] = "white"
theme['bgScroll'] = "#434544"
theme['buttonBg'] = "#aabe44"     #aabe44 #66cc00
theme['buttonFg'] = "#353638"
theme['entryBg'] = "#aabe44"
theme['entryFg'] = "#353638"
theme['font']    = "Helvica"
theme['data']    = "data/"

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, False)

global replaceStr
replaceStr = [["&#39;", "'"],
              ["&amp;", "&"],
              ["&quot;", "\""]]

def findReplaceString(stringIn):
    string = stringIn
    for i in replaceStr:
        replace = i[0]
        replaceWith = i[1]
        if string.find(replace) > -1:
            newName = ""
            rest = string
        else:
            continue
        length = len(replace)
            
        while True:
            place = rest.find(replace)
            if place < 0:
                string = (newName + rest)
                break
            newName = newName + rest[:place] + replaceWith
            rest = rest[place+length:]
    return string


class VideoWidget(QWidget):
    def __init__(self, video):
        super().__init__()
        
        self.titleStr = findReplaceString(video.name)
        self.description = findReplaceString(video.text)
        self.image = video.image
        self.link = video.link
        self.id = video.link[7:]
        self.genre = video.getGenre()
        self.type = video.type

        if theme!= None:
            self.theme = theme
            self.imageSize = theme['imageSize']
        else:
            self.theme = {}
            self.theme['data'] = "data/"
            self.imageSize = [130, 73, 2, 2]
            self.theme['buttonBg'] = None
            self.theme['buttonFg'] = None
            self.theme['font'] = "Helvetica"

        if not os.path.isfile(self.theme['data'] + self.id + ".jpg"):
            self.downloadImage()

        self.initUI()
        self.resize(self.imageSize[0]*2*self.imageSize[2] ,self.imageSize[1]*self.imageSize[2])
        

    def initUI(self):

        self.resize(self.imageSize[0]*2*self.imageSize[2] ,self.imageSize[1]*self.imageSize[2])

        Vbox  = QVBoxLayout(self)
        Hbox2 = QHBoxLayout()

        titleLb = QLabel(self)
        titleFont = QFont(self.theme['font'], 5*self.imageSize[2]+2)
#        titleFont.setPixelSize()
        titleFont.setBold(True)
        titleLb.setFont( titleFont )
        titleLb.setText("<font color='lightgrey'><b>%s:</b></font> %s" % (self.type, self.titleStr))
        titleLb.setWordWrap(True)
        Vbox.addWidget(titleLb)


        imgLabel = QLabel(self)
        
        errorCount = 0
        for i in range(0,2):
            try:
                pixmap = QPixmap(self.theme['data']+str(self.id))
            except:
                if errorCount > 0:
                    pixmap = QPixmap(self.imageSize[0]*self.imageSize[2],self.imageSize[1]*self.imageSize[2])
                    pixmap.fill(QtCore.Qt.black)
                    print("Error loading Image: " + self.id)
                    break
                self.downloadImage()
                errorCount = errorCount+1 
                    
        pixmap = pixmap.scaled(self.imageSize[0]*self.imageSize[2], self.imageSize[1]*self.imageSize[2], QtCore.Qt.KeepAspectRatio)  
        imgLabel.setPixmap(pixmap)
        Hbox2.addWidget(imgLabel)

        desc = QLabel(self.description, self)
        desc.setWordWrap(True)
        desc.setFont(QFont(self.theme['font'], 5*self.imageSize[2]+1))
        desc.setFixedWidth(self.imageSize[0]*self.imageSize[2])
        Hbox2.addWidget(desc)
        Vbox.addLayout(Hbox2)

        string = ""
        for i in self.genre:
            string = string + i + ", "
        string = string[:-2]
        genreLb = QLabel(string, self)
        genreLb.setWordWrap(True)
        genreLb.setFont(QFont(self.theme['font'], 5*self.imageSize[2]+1))
        genreLb.resize(genreLb.sizeHint())
        genreLb.setAlignment(QtCore.Qt.AlignCenter)
        Vbox.addWidget(genreLb)

        openbtn = QPushButton("Goto Stream", self)
        openbtn.clicked.connect(self.openLink)
        openbtn.setFont(QFont(self.theme['font'], 5*self.imageSize[2]+1))
        openbtn.setStyleSheet("background-color: %s; color: %s" % (self.theme['buttonBg'], self.theme['buttonFg']))
        openbtn.resize(openbtn.sizeHint())
        Vbox.addWidget(openbtn)
        
        self.setLayout(Vbox)

        self.show()

    def openLink(self):
        link = urls[0] + self.link
        print(link)
        webbrowser.open_new_tab(link)

    def downloadImage(self):
        print("Downloading Image: " + self.titleStr)
        if not os.path.exists(self.theme['data']):
            os.mkdir(self.theme['data'])
        f = open(self.theme['data'] + self.link[7:] + ".jpg", 'wb')
        try:
            imgUrl = "https" + self.image[self.image.find("://"):]
            print("Using Url: " + imgUrl)
            imageFile = urllib.request.urlopen(imgUrl).read()
            f.write(imageFile)
            f.close()
        except urllib.error.URLError:
            print("Error: Image download failed")
            f.close()
            os.remove(self.theme['data'] + self.link[7:] + ".jpg", 'wb')
            # window, that informs that the download failed?

class OpenButton(QPushButton):
    def __init__(self, text, parent):
        self.setText(text)
        self.clicked.connect(self.openLink)
    def openLink(self):
        print(link)
        webbrowser.open_new_tab(link)    


class CheckButtons(QWidget):
    def __init__(self, pick, default=False):
        super().__init__()
        vbox = QVBoxLayout(self)
        self.pick = pick
        self.checkbox = []

        for i, j in enumerate(pick):
            self.checkbox.append(QCheckBox(j))
            self.checkbox[i].setChecked(default)
            vbox.addWidget(self.checkbox[i])
        self.show()

    def getState(self):
        state = []
        for i,j in enumerate(self.checkbox):
            if j.isChecked():
                state.append(1)
            else:
                state.append(0)
        return state

    def getName(self):
        name = []
        for i, j in enumerate(self.checkbox):
            if j.isChecked():
                name.append(self.pick[i])
        print("Genres: " + str(name))
        return name


class VideoContainer(QWidget):
    def __init__(self, database):
        super().__init__()
        self.initUI()

        self.sql = database
        self.currentType = 0

        self.fillContainer(self.sql.genGenreList())

    def initUI(self):

        self.setWindowTitle('AoD')
        self.setWindowIcon(QIcon('logo.ico'))
        self.setMaximumWidth(0)

        color = self.palette()
        color.setColor(self.backgroundRole(), QColor(theme['bgMain']))
        color.setColor(self.foregroundRole(), QColor(theme['fgMain']))
        self.setPalette(color)

        self.setFont(QFont("Helvetica", 5*theme['imageSize'][2]+1))

        hbox = QHBoxLayout()
        controlbox = QVBoxLayout()

#        controlbox.addStretch(1)
        controlbox.setAlignment(QtCore.Qt.AlignCenter)
        
        self.scroll = QScrollArea()
        QScroller.grabGesture(self.scroll.viewport(), QScroller.LeftMouseButtonGesture)
        self.scroll.setWidgetResizable(False)
        self.scroll.setMinimumHeight(theme['imageSize'][1]*4*theme['imageSize'][2])
        self.scroll.setFixedWidth(theme['imageSize'][0]*4*theme['imageSize'][2]+100)
        scrollBg = self.palette()
        scrollBg.setColor(self.backgroundRole(), QColor(theme['bgScroll']))
        self.scroll.setPalette(scrollBg)
               

        self.chkbox = CheckButtons(genre)
        controlbox.addWidget(self.chkbox)

        self.typeBtn = QPushButton("Filme/Serien", self)
        self.typeBtn.resize(self.typeBtn.sizeHint())
        self.typeBtn.clicked.connect(self.typeSelect)
        self.typeBtn.setStyleSheet("background-color: %s; color: %s; border: 0px;" % (theme['bgScroll'], theme['fgMain']))
        controlbox.addWidget(self.typeBtn)

        self.searchbox = QLineEdit(self)
        self.searchbox.resize(self.searchbox.sizeHint())
        self.searchbox.setPlaceholderText("Suchen...")
        self.searchbox.returnPressed.connect(self.startBtnHandle)
        self.searchbox.setStyleSheet("background-color: %s; color: %s; border: 0px;" % (theme['entryBg'], theme['entryFg']))
        controlbox.addWidget(self.searchbox) 

        startbtn = QPushButton("Start", self)
        startbtn.clicked.connect(self.startBtnHandle)
        startbtn.setStyleSheet("background-color: %s; color: %s" % (theme['buttonBg'], theme['buttonFg']))
        startbtn.resize(startbtn.sizeHint())
        controlbox.addWidget(startbtn)

        self.statusLb = QLabel("Ready", self)
        self.statusLb.resize(startbtn.sizeHint())
        controlbox.addWidget(self.statusLb)
        
        hbox.addWidget(self.scroll)
        hbox.addLayout(controlbox)
                
        self.setLayout(hbox)

        self.show()

    def typeSelect(self):
        if self.currentType == 0:
            self.currentType = 1
            self.typeBtn.setText("Serien")
        elif self.currentType == 1:
            self.currentType = 2
            self.typeBtn.setText("Filme")
        elif self.currentType == 2:
            self.currentType = 0
            self.typeBtn.setText("Filme/Serien")

    def startBtnHandle(self):
        try:
            self.fillContainer(self.sql.genGenreList(self.chkbox.getName(), self.currentType))
        except Exception as e: print(e)
        

    def fillContainer(self, objects=[], search=None):
        search = self.searchbox.text()
        print("Serarch: " + search)

        mygroupbox = QFrame()
        
        contentgrid = QGridLayout()
        contentlist = []

        i=0
        for x, j in enumerate(objects):
            if search==None or j.checkName(search):
                contentlist.append( VideoWidget(j) )               
                contentgrid.addWidget(contentlist[i], i/2, i%2)
                i = i+1

        print("Displayed Title: " + str(i))
        self.statusLb.setText("%i Titel geladen" % i)
        mygroupbox.setLayout(contentgrid)
        self.scroll.takeWidget()
        self.scroll.setWidget(mygroupbox)


    def removeAll(self):
        try:
            self.scroll.takeWidget()
        except Exception as e: print(e)
        

if __name__ == '__main__':

    database = sqllib.sqlHandle()
    database.updateDatabase(urls, searchTerm, genre)
    print(database.getNewOutdated())

    app = QApplication(sys.argv)
    ex = VideoContainer(database)
    os._exit(app.exec())


