#Searching function for locally-found picture data for "Kevin Bacon" 6 degrees of separation
#problem.

#Made by Matthew Riddoch
#https://github.com/Mattew98

print("Loading...")

#creating classes

class Picture:
    def __init__(self,index,path,people):
        self.index = index #index of picture = 'picturedata.csv' row number
        self.path = str(path) #picture path
        self.people = people #people in picture

class Person:

    def __init__(self,index,name):
        self.index = index #index of person = 'peopledata.csv' row number
        self.name = str(name) #name of person as string
        self.pictures=[] #pictures the person is in
        
    def addpicture(self,picture): #function to add pictures to self.pictures
        self.pictures.append(picture)

import csv

#sorting people data and creating people classes

globalpeople = [] #reference arrays to be indexed later
peoplelist = []

with open('peopledata.csv',newline='') as data: #opening and sorting the data in 'peopledata.csv'
    datareader = csv.reader(data,delimiter=',')
    rawrow=[]
    people = []
    for row in datareader: #return array of sorted values
        if row!=[]:
            rawrow.append(row)
            people.append(row[1])
            rawrow.sort()
    people.sort()
    with open('peopledata.csv','w',newline='') as data: #remove current data in csv file
        datawriter=csv.writer(data,delimiter=',')
        datawriter.writerows("")
    with open('peopledata.csv','a',newline='\n') as data: #rewrite the csv file data
        datawriter=csv.writer(data,delimiter=',')
        for person in people:
            peoplelist.append(person)
            datawriter.writerow(rawrow[people.index(person)])
            globals()[f'person{str(people.index(person))}'] = Person(people.index(person),person) #create global class instances for each person in 'peopledata.csv'
            globalpeople.append(globals()[f'person{str(people.index(person))}'])

#creating picture classes and applying people to pictures

globalpictures=[]

with open('picturedata.csv',newline='') as data: #reading 'picturedata.csv'
    datareader = csv.reader(data,delimiter=',')
    for row in datareader:
        csvpeople = []
        i = 0
        while i < int(row[0]): #the number of people in each picture is the first variable in each 'picturedata.csv' row
            csvpeople.append(row[i+2])
            i+=1
        globals()[f'picture{str(datareader.line_num)}'] = Picture(datareader.line_num-1,row[1],csvpeople) #create global class instances for each picture in 'picturedata.csv'
        globalpictures.append(globals()[f'picture{str(datareader.line_num)}'])

#applying pictures to people

for picture in globalpictures: #adding picture index values to the relevant people classes (e.g. adding picture xxx to person ABC if person is in picture)
    for person in picture.people:
        for p in globalpeople:
            if person==p.name:
                p.addpicture(picture.index)

print("Finished Loading.")

#test code:

#for person in globalpeople:
#    print(person.index, person.name, person.pictures)

#for picture in globalpictures:
#    print(picture.index,picture.path,picture.people)

#search function

def subsearch(personindex, p2): #returns the "children" of each picture that 'p1' is in
    people = []
    for pic in globalpeople[personindex].pictures:
        for person in globalpictures[pic].people:
            people.append(peoplelist.index(person))
            if person == p2:
                return people, True
    return people, False

#global arrays to be referenced by search function
globalpaths = []
searchedpeople = []

def search(p1,p2,loopnum): #recursive function to search for people linked to others
    
    found = False
    loopnum+=1

    print("Loop: ",str(loopnum))

    if loopnum == 1: #first loop only contains one person so just adds person to searched people
        globals()[f'path{str(loopnum)}'] = []
        globals()[f'path{str(loopnum)}'].append(p1)
        searchedpeople.append(p1)
        globalpaths.append(globals()[f'path{str(loopnum)}'])

    elif loopnum > 1 and loopnum < 12:
        searchpaths = []
        for paths in globalpaths: #loops through each possible path stored in 'globalpaths'
            if len(paths) == loopnum - 1: #only search through paths of the right length
                searchpaths.append(paths)
            elif len(paths) < loopnum - 1: #remove paths of a smaller length to save stack memory
                del paths
        for path in searchpaths: #now only searching through relevant arrays
            newpeople, found = subsearch(path[loopnum-2],p2)
            for i,p in enumerate(newpeople):
                if p not in path and p not in searchedpeople: #check we're not repeating people
                    searchedpeople.append(p)
                    globals()[f'path{str(loopnum)}|{str(i)}'] = path.copy() #create a new path with the new person index added on the end
                    globals()[f'path{str(loopnum)}|{str(i)}'].append(p)
                    globalpaths.append(globals()[f'path{str(loopnum)}|{str(i)}'])
                    if p == p2:
                        return globals()[f'path{str(loopnum)}|{str(i)}'], loopnum #if 'p2' is found, return the correct path of people index values
    
    elif loopnum == 12: #stop recursions at 12 loops (used to be an issue before I optimised memory use, kept in because it should only be 6 loops)
        print("Error: 12+ people away")

    else:
        print("Error")
    
    if not found: #return self (next loop)
        return search(p1,p2,loopnum)

#run

#inputting people in string form

Person1 = input("Person 1:\n")
Person2 = input("Person 2:\n")

#check if the people have been catalogued

p1 = False
p2 = False

for p in globalpeople:
    if p.name == Person1:
        p1 = True
    elif p.name == Person2:
        p2 = True

#get image opening library

from PIL import Image

#global variables to be referenced soon

foundpath = []
loops = 0

per1 = 0
per2 = 0

#using found people to run search function

if p1 and p2:
    foundpath = [] #path of pictures instead of people
    for person in globalpeople:
        if person.name==Person2:
            per2 = person.index
        elif person.name==Person1:
            per1 = person.index
    ppath, loops = search(per1,per2, 0)
    
    for i,person in enumerate(ppath):
        if i < len(ppath) - 1:
            for pic in globalpeople[person].pictures:
                if peoplelist[ppath[i+1]] in globalpictures[pic].people: #if person i and person i+1 in ppath are in the same picture, add it to path
                    foundpath.append(pic)
                    break
    
    #results

    print(foundpath)
    print("Connection found from "+Person1+" to "+Person2+" in "+str(loops)+" steps.")
    print("\nThrough: \n")
    for p in ppath:
        print(globalpeople[p].name)
    for pic in foundpath:
        img = Image.open(globalpictures[pic].path)
        img.show() 
else:
    print("Person not found") #if entered person is not found in 'peopledata.csv'