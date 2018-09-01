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
               ['animebox-shorttext', '</p>'    ,  2, -1]   #Short description
               ]


global imageSize
imageSize = [130, 73, 2]

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
            break
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
        
        self.resize(imageSize[0]*2*imageSize[2] ,imageSize[1]*imageSize[2])
        
        self.titleStr = findReplaceString(video.name)
        self.description = findReplaceString(video.text)
        self.image = video.image
        self.link = video.link
        self.id = video.link[7:]

        if False:
            self.dataPath = "data/"
            self.localBg = "#353638"
            self.localFg = "white"
            self.bgSort = "#353638"
            self.buttonBg = "#aabe44"
            
            self.btnFgTmp = self.palette()
            self.btnFgTmp.setColor(self.foregroundRole(), QtCore.Qt.green) #schrift
            self.btnFgTmp.setColor(self.backgroundRole(), QtCore.Qt.black)
            self.buttonFg = "#353638"
            self.localFont = "Helvetica"
        else:
            self.dataPath = "data/"
            self.localBg = None
            self.localFg = None
            self.bgSort = None
            self.buttonBg = None
            self.buttonFg = None
            self.localFont = "Helvetica"

        if not os.path.isfile(self.dataPath + self.id + ".jpg"):
            self.downloadImage()

        self.initUI()
        self.resize(imageSize[0]*2*imageSize[2] ,imageSize[1]*imageSize[2])
        
    def initUI(self):


        Vbox  = QVBoxLayout(self)
        Hbox2 = QHBoxLayout(self)

        titleLb = QLabel(self)
        titleFont = QFont("Helvetica", 5*imageSize[2]+2)
        titleFont.setBold(True)
        titleLb.setFont( titleFont )
        titleLb.setText(self.titleStr)
        titleLb.setWordWrap(True)
        Vbox.addWidget(titleLb)


        imgLabel = QLabel(self)
        
        errorCount = 0
        for i in range(0,2):
            try:
                pixmap = QPixmap(self.dataPath+str(self.id))
            except:
                if errorCount > 0:
                    pixmap = QPixmap(260,146)
                    pixmap.fill(QtCore.Qt.black)
                    print("Error loading Image: " + self.id)
                    break
                self.downloadImage()
                errorCount = errorCount+1 
                    
        img = pixmap.scaled(self.frameGeometry().width()*(1/1), self.frameGeometry().height()*(1/1), QtCore.Qt.KeepAspectRatio)  
        imgLabel.setPixmap(pixmap)
        Hbox2.addWidget(imgLabel)

        desc = QLabel(self.description, self)
        desc.setWordWrap(True)
        desc.setFont(QFont("Helvetica", 5*imageSize[2]+1))
        desc.setFixedWidth(imageSize[0]*imageSize[2])
        Hbox2.addWidget(desc)
        Vbox.addLayout(Hbox2)


        openbtn = QPushButton("Goto Stream", self)
        openbtn.clicked.connect(self.openLink)
        openbtn.setFont(QFont("Helvetica", 5*imageSize[2]+1))
        openbtn.resize(openbtn.sizeHint())
        Vbox.addWidget(openbtn)
        
        self.setLayout(Vbox)

        self.show()

    def openLink(self):
#        global urls
        link = urls[0] + self.link
        print(link)
        webbrowser.open_new_tab(link)

    def downloadImage(self):
        print("Downloading Image: " + self.titleStr)
        if not os.path.exists(self.dataPath):
            os.mkdir(self.dataPath)
        f = open(self.dataPath + self.link[7:] + ".jpg", 'wb')
        try:
            imageFile = urllib.request.urlopen(self.image[1:]).read()
            f.write(imageFile)
            f.close()
        except urllib.error.URLError:
            print("Error loading URL: " + self.image[1:])
            # window, that informs that the download failed

class OpenButton(QPushButton):
    def __init__(self, text, parent):
        self.setText(text)
        self.clicked.connect(self.openLink)
    def openLink(self):
        print(link)
        webbrowser.open_new_tab(link)    


class CheckButtons(QWidget):
    def __init__(self, pick):
        super().__init__()
        vbox = QVBoxLayout(self)
        self.pick = pick
        self.checkbox = []

        for i, j in enumerate(pick):
            self.checkbox.append(QCheckBox(j))
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
        return name


class VideoContainer(QWidget):
    def __init__(self, img):
        super().__init__()
        self.img = img
        self.initUI()

        self.sql = sqllib.sqlHandle()
        
        self.fillContainer(self.sql.genGenreList())

    def initUI(self):

        hbox = QHBoxLayout()
        controlbox = QVBoxLayout()

#        controlbox.addStretch(1)
        controlbox.setAlignment(QtCore.Qt.AlignCenter)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(False)
        self.scroll.setMinimumHeight(imageSize[1]*4*imageSize[2])
        self.scroll.setFixedWidth(imageSize[0]*4*imageSize[2]+100)
        
#        QScroller.grabGesture(self.scroll.viewport(), QScroller.LeftMouseButtonGesture)
        

        self.chkbox = CheckButtons(genre)
        controlbox.addWidget(self.chkbox)

        self.searchbox = QLineEdit(self)
        self.searchbox.resize(self.searchbox.sizeHint())
        self.searchbox.returnPressed.connect(self.startBtnHandle)
        controlbox.addWidget(self.searchbox) 

        startbtn = QPushButton("Start", self)
        startbtn.clicked.connect(self.startBtnHandle)
        startbtn.resize(startbtn.sizeHint())
        controlbox.addWidget(startbtn)
        
        hbox.addWidget(self.scroll)
        hbox.addLayout(controlbox)
                
        self.setLayout(hbox)


#        self.btnFgTmp = self.palette()
#        self.btnFgTmp.setColor(self.backgroundRole(), QtCore.Qt.black)
#        self.setPalette(self.btnFgTmp)

        self.show()

    def startBtnHandle(self):
        try:
            self.fillContainer(self.sql.genGenreList(self.chkbox.getName()))
        except Exception as e: print(e)
        

    def fillContainer(self, objects=[], search=None):
        search = self.searchbox.text()
        mygroupbox = QFrame()
        contentgrid = QGridLayout()
        contentlist = []

        falseEntrys = 0
        i=0
        for x, j in enumerate(objects):
            if search==None or j.checkName(search):
                contentlist.append( VideoWidget(j) )
                contentgrid.addWidget(contentlist[i], i/2, i%2)
                i = i+1

        print("Displayed Title: " + str(i))
        mygroupbox.setLayout(contentgrid)
        self.scroll.takeWidget()
        self.scroll.setWidget(mygroupbox)


    def removeAll(self):
        try:
            self.scroll.takeWidget()
        except Exception as e: print(e)
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = VideoContainer("data/2.jpg")
    ex.setWindowTitle('AoD Test')
#    ex.fillContainer()
    app.exec()


