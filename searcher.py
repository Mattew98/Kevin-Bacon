print("Loading...")

#creating classes

class Picture:
    def __init__(self,index,path,people):
        self.index = index
        self.path = str(path)
        self.people = people

class Person:

    def __init__(self,index,name):
        self.index = index
        self.name = str(name)
        self.pictures=[]
        
    def addpicture(self,picture):
        self.pictures.append(picture)

import csv

#sorting people data and creating people classes

globalpeople = []
peoplelist = []

with open('peopledata.csv',newline='') as data:
    datareader = csv.reader(data,delimiter=',')
    rawrow=[]
    people = []
    for row in datareader:
        if row!=[]:
            rawrow.append(row)
            people.append(row[1])
            rawrow.sort()
    people.sort()
    with open('peopledata.csv','w',newline='') as data:
        datawriter=csv.writer(data,delimiter=',')
        datawriter.writerows("")
    with open('peopledata.csv','a',newline='\n') as data:
        datawriter=csv.writer(data,delimiter=',')
        for person in people:
            peoplelist.append(person)
            datawriter.writerow(rawrow[people.index(person)])
            globals()[f'person{str(people.index(person))}'] = Person(people.index(person),person)
            globalpeople.append(globals()[f'person{str(people.index(person))}'])

#creating picture classes and applying people to pictures

globalpictures=[]

with open('picturedata.csv',newline='') as data:
    datareader = csv.reader(data,delimiter=',')
    for row in datareader:
        csvpeople = []
        i = 0
        while i < int(row[0]):
            csvpeople.append(row[i+2])
            i+=1
        globals()[f'picture{str(datareader.line_num)}'] = Picture(datareader.line_num-1,row[1],csvpeople)
        globalpictures.append(globals()[f'picture{str(datareader.line_num)}'])

#applying pictures to people

for picture in globalpictures:
    for person in picture.people:
        for p in globalpeople:
            if person==p.name:
                p.addpicture(picture.index)

print("Finished Loading.")

#test

#for person in globalpeople:
#    print(person.index, person.name, person.pictures)

#for picture in globalpictures:
#    print(picture.index,picture.path,picture.people)

#search function

def subsearch(personindex, p2):
    people = []
    for pic in globalpeople[personindex].pictures:
        for person in globalpictures[pic].people:
            people.append(peoplelist.index(person))
            if person == p2:
                return people, True
    return people, False

globalpaths = []
searchedpeople = []

def search(p1,p2,loopnum):
    
    found = False
    loopnum+=1

    print("Loop: ",str(loopnum))

    if loopnum == 1:
        globals()[f'path{str(loopnum)}'] = []
        globals()[f'path{str(loopnum)}'].append(p1)
        searchedpeople.append(p1)
        globalpaths.append(globals()[f'path{str(loopnum)}'])

    elif loopnum > 1 and loopnum < 12:
        searchpaths = []
        for paths in globalpaths:
            if len(paths) == loopnum - 1:
                searchpaths.append(paths)
            elif len(paths) < loopnum - 1:
                del paths
        for path in searchpaths:
            newpeople, found = subsearch(path[loopnum-2],p2)
            for i,p in enumerate(newpeople):
                if p not in path and p not in searchedpeople:
                    searchedpeople.append(p)
                    globals()[f'path{str(loopnum)}|{str(i)}'] = path.copy()
                    globals()[f'path{str(loopnum)}|{str(i)}'].append(p)
                    globalpaths.append(globals()[f'path{str(loopnum)}|{str(i)}'])
                    if p == p2:
                        return globals()[f'path{str(loopnum)}|{str(i)}'], loopnum
    
    elif loopnum == 12:
        print("Error: 12+ people away")

    else:
        print("Error")
    
    if not found:
        return search(p1,p2,loopnum)

#run

Person1 = input("Person 1:\n")
Person2 = input("Person 2:\n")

#true check

p1 = False
p2 = False

for p in globalpeople:
    if p.name == Person1:
        p1 = True
    elif p.name == Person2:
        p2 = True

from PIL import Image

foundpath = []
loops = 0

per1 = 0
per2 = 0

if p1 and p2:
    foundpath = []
    peoplepath = []
    for person in globalpeople:
        if person.name==Person2:
            per2 = person.index
        elif person.name==Person1:
            per1 = person.index
    ppath, loops = search(per1,per2, 0)
    
    for i,person in enumerate(ppath):
        peoplepath.append(person)
        if i < len(ppath) - 1:
            for pic in globalpeople[person].pictures:
                if peoplelist[ppath[i+1]] in globalpictures[pic].people:
                    foundpath.append(pic)
                    break

    print(foundpath)
    print("Connection found from "+Person1+" to "+Person2+" in "+str(loops)+" steps.")
    print("\nThrough: \n")
    for p in peoplepath:
        print(globalpeople[p].name)
    for pic in foundpath:
        img = Image.open(globalpictures[pic].path)
        img.show() 
else:
    print("Person not found")