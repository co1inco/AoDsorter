import AoD
import csv

def arrayToString(array):
    string = "["
    for i in array:
        string = string + str(i) + ","
    if len(string)>1:
        string = string[:-1] + "]"
    else:
        string = string + "]"        
    return string

def stringToArray(string):
    array = []
    string = string[1:-1]
    array = string.split(",")
    return array

def readCSV(filename="test.csv"):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        return []

    offlineList = []
    readFile = csv.reader(file, delimiter=' ', quotechar='|')
    
    for i in readFile:
        if len(i) == 0:
            continue
        videoObj = AoD.Video(i[0], i[1], i[2], i[3])
        for j in stringToArray(i[4]):
            videoObj.addGenre(j)
        offlineList.append(videoObj)
    file.close()
    return offlineList

def writeCSV(objectList, filename="test.csv", mode="a"):
    file = open(filename, mode)
    writeFile = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in objectList:
        print("Write " + i.name)
        writeFile.writerow([i.name]+[i.image]+[i.link]+[i.text]+[arrayToString(i.genre)])
    file.close()

"""
def updateValid(titleList, filename="test.csv", valid=False):
    file = open(filename, "r")
    readFile = csv.reader(file, delimiter=' ', quotechar='|')
    rowNums = []
    rowText = []
    for i, j in enumerate(readFile):
        if len(j) == 0: #emty line
            continue
        for k in titleList:
            if j[0] == k.name:
                if j[5] == "True":
                    rowNums.append(i+1)
                    rowText.append(j)
                    print("remove " + k.name)
    file.close()

    bottle_list = []
    with open(filename, 'r') as b:
        for i, j in enumerate(rowText):
            bottles = csv.reader(b)
            bottle_list.extend(bottles)

            line_to_override = {rowNums[i]:[j[0], j[1], j[2], j[3], j[4], str(valid), j[6]]}

            with open(filename, 'w') as b:
                writer = csv.writer(b)
                for line, row in enumerate(bottle_list):
                     data = line_to_override.get(line, row)
                     writer.writerow(data)
 """       
        
def updateTitleList(offlinelist, onlinelist, filename="test.csv"):
    removedTitle = []
    for i in offlinelist:
        found = False
        for j in onlinelist:
            if i.name == j.name:
                onlinelist.remove(j)
                found = True
                break
        if found == True:
            continue
        else:
            removedTitle.append(i)

    if len(removedTitle) > 0:
        for i in removedTitle:
            offlinelist.remove(i)
            print("Removed: " + i.name)
    return onlinelist


if __name__ == '__main__':
    from AOD import *
    
    mainSite = "https://www.anime-on-demand.de"
    mainList = "/animes/"
    genreList = "/animes/genre/" 

    genre = ['Abenteuer', 'Action', 'Comedy','Erotik']
    #onlinelist = AoD.get_title_list(mainSite+mainList)
    onlinelist = readCSV(filename="off-test.csv")
  
    #writeCSV(onlineList, mode="w")
    offlinelist = readCSV()
    offlinelist = updateTitleList(offlinelist, onlinelist, genre)


    



