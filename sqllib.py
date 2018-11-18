import sqlite3
import urllib.request

import os

class Video():
    def __init__(self, name, image, link, text, type=None):
        self.name = name
        self.image = image
        self.link = link
        self.text = text
        self.img = None
        self.genre = []

        self.type = type

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


class sqlHandle():
    def __init__(self, path="./", file="database.db"):
        self.con = sqlite3.connect(path + file)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS Videos(Id INT, Name TEXT, Image TEXT, Link TEXT, Description TEXT, Type TEXT, Valid BOOL, PRIMARY KEY(Id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Genre(Id INT, GenreName TEXT)")


    def updateDatabase(self, urls, searchTerms, genre, loadingScreen=None):

        onlineListe = get_title_list(urls[0] + urls[1], searchTerms)
#        onlineListe = onlineListe[3:] remove title from online data (testing purposes)
        
        loadedGenre = False

        self.cur.execute("SELECT Id FROM Videos WHERE Valid = 0")
        invalid = []
        x = self.cur.fetchall()
        for i in x:
            invalid.append(i[0])

        
        for j in onlineListe:
            videoId = int(j.link[7:])
            
            self.cur.execute("SELECT Id From Videos WHERE ID = %s" % videoId)

            #add new
            if len(self.cur.fetchall()) == 0:
                if loadedGenre == False:
                    onlineListe = addGenre(urls, genre, onlineListe, searchTerms, loadingScreen)
                    loadedGenre = True
                    
                print(("add " + j.name).encode("utf-8"))
                self.cur.execute("INSERT INTO Videos VALUES('%s', '%s', '%s', '%s', '%s', '%s', 1)"
                            % (videoId, j.name, j.image, j.link, j.text, j.type))
                
                for k in j.genre: #move outside and only do it when new item
                    self.cur.execute("INSERT INTO Genre VALUES('%s', '%s')" % (videoId, k))
                continue

            #check if found entry is invalid (title readded)
            if videoId in invalid:
                print(j.name + " is back again \\o/") 
                self.cur.execute("UPDATE Videos SET Valid=1 WHERE ID = %s" % videoId)

        count = 0

        self.cur.execute("SELECT Id FROM Videos WHERE valid = 1")
        offlineList = self.cur.fetchall()
        self.removed = []
        if len(offlineList) > len(onlineListe):
            for i in offlineList:
                found = False
                for j in onlineListe:
                    if str(i[0]) == j.link[7:]:
                        found = True
                        break
                if found == False:
                    self.removed.append(i[0])
            for i in self.removed:
                self.cur.execute("SELECT name FROM Videos WHERE Id = %s" % i)
                print("Removed: " + self.cur.fetchall()[0][0])
                self.cur.execute("UPDATE Videos SET Valid=0 WHERE Id = %s" % i)
                        
        self.con.commit()


    def genVideoList(self):
        self.cur.execute("SELECT * FROM Videos WHERE Valid = 1 ORDER BY name")
        return self.createVideoObject(self.cur.fetchall())

    def genGenreList(self, genre = [], type=0):
        selection = ""
        print(genre)

        if type == 0:
            addType = ""
        elif type == 1:
            addType = "Type = 'Serie' AND"
        elif type == 2:
            addType = "Type = 'Film' AND"

        if len(genre):
            for i in genre:
                selection = selection + " Id IN (SELECT Id FROM genre WHERE genreName = '%s') AND" % i

        self.cur.execute("""SELECT * FROM videos
                            WHERE %s %s Valid = 1
                            ORDER BY name""" % (selection, addType))
        return self.createVideoObject(self.cur.fetchall())

    def getOutdated(self):
        self.cur.execute("SELECT id, name FROM Videos WHERE Valid = 0")
        return self.cur.fetchall()

    def getNewOutdated(self):
        removed = []
        for i in self.removed:
            self.cur.execute("SELECT id, name FROM Videos WHERE id = %s" % i)
            removed.append(self.cur.fetchall())
        return removed
    
    def execute(self, string):
        self.cur.execute(string)

    def genVideoListRaw(self):
        self.cur.execute("SELECT * FROM Videos ")
        return self.cur.fetchall()

    def genGenreListRaw(self, genre):
        self.cur.execute("""SELECT * FROM videos
                            WHERE Id IN (SELECT Id FROM genre
                                WHERE genreName = '%s')
                                ORDER BY name""", genre)
        return self.cur.fetchall()

    def createVideoObject(self, fetch):
        videoList = []
        for i in fetch:
            video = Video(i[1], i[2], i[3], i[4], i[5])
            self.cur.execute("SELECT genrename FROM genre WHERE id = %s" % i[0])
            for j in self.cur.fetchall():
                video.addGenre(j[0])
            videoList.append(video)
        return videoList

    def closeFile(self):
        self.con.close()

def addGenre(urls, genreList, videoList, searchTerm, loadingScreen=None):

    if loadingScreen != None:
        ls = loadingScreen(len(genreList)-1)

    for index, genre in enumerate(genreList):
        if genre == "Deutsch":
            url = urls[0] + urls[1]
        else:
            url = urls[0] + urls[2]

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

        for i in videoList:
            try:
                if i.name == title[0]:
                    i.addGenre(genre)
                    title.pop(0)
            except IndexError:
                break
        if loadingScreen != None:
            ls.setValue(index)

#    time.sleep(1)
    return videoList


def get_title_list(url, searchTerm):
    print(url)
   
    site = urllib.request.urlopen(url)
    text = site.read().decode("utf8")
    print("Main list download Finished")

    a = []

    Start = 1
    while Start > -1:

        aName, text = get_part(text, searchTerm[0])

        aImage, text = get_part(text, searchTerm[1])

        aLink, text = get_part(text, searchTerm[2])

        aType, text = get_part(text, searchTerm[3])

        aShort, text = get_part(text, searchTerm[4])        

        a.append(Video(aName, aImage, aLink, aShort, aType))
        Start = text.find(searchTerm[0][0])
    print("Main list processing Finished")
    return a       


def get_part(file, searchFor):
    termLen = len(searchFor[0])
    
    start = file.find(searchFor[0]) + termLen + searchFor[2]
    file = file[start:]
    end = file.find(searchFor[1]) + searchFor[3]
    out = file[:end]

    return out, file


if __name__ == '__main__':
    import AoD

    os.remove("database.db")
    genre = AoD.genre
    urls = AoD.urls
    s = sqlHandle()



