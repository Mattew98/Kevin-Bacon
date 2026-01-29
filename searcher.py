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
        globals()[f'picture{str(datareader.line_num)}'] = Picture(datareader.line_num,row[1],csvpeople)
        globalpictures.append(globals()[f'picture{str(datareader.line_num)}'])

#applying pictures to people

for picture in globalpictures:
    for person in picture.people:
        for p in globalpeople:
            if person==p.name:
                p.addpicture(picture.index)

print("Finished Loading.")

#test

for person in globalpeople:
    print(person.index, person.name, person.pictures)

for picture in globalpictures:
    print(picture.index,picture.path,picture.people)

#search function

def search(pictureindices,p1,p2,path,loopnum,peoplepath):
    if p1 not in peoplepath:
        peoplepath.append(p1)
        loopnum +=1
        for picture in globalpictures:
            if picture.index not in path:
                path1 = path
                if picture.index in pictureindices:
                    path1.append(picture.index)
                    for person in picture.people:
                        indices = []
                        for pic in globalpeople[peoplelist.index(person)].pictures:
                            indices.append(pic)
                        if person == p2:
                            print("Found!")
                            return path1, loopnum
                        elif person not in peoplepath:
                            return search(indices,person,p2,path1,loopnum,peoplepath)

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

foundpath = []
loops = 0

if p1 and p2:
    for person in globalpeople:
        if person.name==Person1:
            foundpath, loops = search(person.pictures,Person1,Person2,[],0,[])
else:
    print("Person not found")

from PIL import Image

if foundpath != []:
    print("Connection found from "+Person1+" to "+Person2+" in "+str(loops)+" steps.")
    for i,v in enumerate(foundpath):
        img = Image.open(globalpictures[i].path)
        img.show() 