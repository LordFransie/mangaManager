import urllib.request, sys, getopt, json, csv, os, shutil, discord_webhook, validators, multiprocessing, requests
from manga import Manga
from multiprocessing import Pool
from pathlib import Path


list = []
session = None
downloadIndex = 0
version = "0.01"
inputString = '--> '
 

def loadManga(file = ".manga.csv"):
    home = str(Path.home())
    f = open(home+'/'+file)
    csv_f = csv.reader(f)
    for index, row in enumerate(csv_f):
        list.append(Manga(row[0],row[1],index))

def updateAllNames():
    for index, manga in enumerate(list):
        if index > 100:
            Manga.updateName()

def closeApp():
    for manga in list:
        manga.writeToCSV()

def newManga(id):
    list.append(Manga(id))

def downloadManga(manga):
    manga.download()

def downloadAllManga(processThreads = 5):
    with Pool(processes=processThreads) as pool:
        pool.map(downloadManga, list)



def mainMenu():
    print("Manga Manager " + version)
    print("What would you like to do")
    print("[1] Reload All Series")
    print("[2] Update Name(s)")
    print("[3] Add a New Series")
    print("[4] Download all Managa")
    print("[5] Test New Features")
    print("[6] Exit")
    menuSelection = int(input(inputString))
    print(menuSelection)
    if(menuSelection == 1):
        loadManga()
    elif(menuSelection == 2):
        pass
    elif(menuSelection == 3):
        print("MangaDex URL or ID")
        newManga(input(inputString))
    elif(menuSelection == 4):
        print("This is experimental and runs concurrently")
        processThreads = int(input("How Many Download Threads: "))
        downloadAllManga(processThreads)
    elif(menuSelection == 5):
        print(list[0].name)
    elif(menuSelection == 6):
        closeApp()
        return
    
    mainMenu()

loadManga()


def main(argv):
    inputfile = ''
    outputfile = ''
    launchMenu = True
    try:
        opts, args = getopt.getopt(argv,"hi:o:r:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-r"):
            launchMenu == False
            downloadAllManga(int(arg))

    if(launchMenu == True):
        mainMenu()
     

if __name__ == "__main__":
   main(sys.argv[1:])

# mainMenu()


# Write to file

# Download Logic

# Pull URLs

# Feed URL to gallery-dl

# Report to discord



