import validators, os, urllib.request, json, csv, shutil, time
from pathlib import Path


inputString = '--> '

home = str(Path.home())
from tempfile import NamedTemporaryFile

class Manga:

    def __init__(self, id, name="", index = -1):

        
        if(validators.url(id)):
            self.url = id
            self.getMangaID()
        else:
            try:
                int(id)
                self.id = int(id)
                self.url = ""
                self.updateUrl()
            except ValueError:
                print("Invalid Identifier: "+id)
                return False
    
        self.name = name
        self.index = index

        if name == "":
            self.updateName()
        self.updateUrl()
    
    def updateName(self):
        if self.id != 0:
            with urllib.request.urlopen("https://api.mangadex.org/v2/manga/"+str(self.id)) as url:
                data = json.loads(url.read().decode())
                #print(data['data']['altTitles'])
                
                stockTitle = data['data']['title']
                print(f'Current Title: {self.name}')
                print(f'[1] {stockTitle}')
                index = 2;
                for title in data['data']['altTitles']:
                    print(f'[{index}] {title}')
                    index += 1
                print("0 to Skip")
                titleKey = int(input(inputString))
                if titleKey == 0:
                    print("Skipping")
                    return
                elif titleKey > 1:
                    titleKey -= 2
                    self.name = data['data']['altTitles'][titleKey]
                elif titleKey == 1:
                    self.name = stockTitle
                print("New Name: " + self.name)
                self.writeToCSV()
            return
    
    def updateUrl(self):
        if "mangadex" in self.url or self.id > 0:
            self.url = "https://mangadex.org/title/"+str(self.id)


    def getMangaID(self):
        if "mangadex" in self.url:
            self.id = self.url.split("/")[4]
        else:
            self.id = 0
        

    def information(self):
        # Print the URL, Name, and ID
        pass
        

    def writeToCSV(self):
        print(self.index)
        filename = home+'/.manga.csv'
        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)

        with open(filename, 'r', newline='') as csvFile, tempfile:
            print(csvFile.name)
            print(tempfile.name)
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            writer = csv.writer(tempfile, delimiter=',', quotechar='"')
            #go through our list, updating if we can
            for index, row in enumerate(reader):
                if(index == self.index):
                    print("88 "+self.url)
                    writer.writerow([self.url, self.name])
                else:
                    print(row)
                    row[1] = row[1].title()
                    writer.writerow(row)
            # if we are a new one, add at the bottom
            if self.index == -1:
                print("I'm new, be gentle")
                print(self.url)
                print(self.name)
                writer.writerow([self.url, self.name])

        shutil.move(tempfile.name, filename)

    def download(self):
        print("Downloading "+self.name)
        os.system('gallery-dl '+self.url)