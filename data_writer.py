import csv

#Prompt
def datawrite():
    Path = input("Path of picture:\n")
    Number = int(input("How many people in photo?\n"))
    People = []

    #Creating array of people in picture

    i = 0
    while i < Number:
        person = input("Person " + str(i)+":\n")
        People.append(person)
        i+=1

    #Adding new people to 'peopledata.csv'

    with open('peopledata.csv',newline='') as data:
        storedpeople = []
        reader=csv.reader(data,delimiter=',')
        for row in reader:
            if row!= []:
                storedpeople.append(row[1])
        for person in People:
            if person not in storedpeople:
                with open('peopledata.csv','a',newline='\n') as data:
                    writer = csv.writer(data,delimiter=',')
                    writer.writerow([str('-')]+[person]) #add a hyphon before the person name so python reads the csv row as an array and doesn't index through the string

    #Adding new pictures to 'picturedata.csv'       

    with open('picturedata.csv','a',newline='\n') as data:
        reader=csv.reader(data,delimiter=',')
        writer=csv.writer(data,delimiter=',')
        writer.writerow([Number]+[Path]+People) #Data stored as |Number of people in picture|Picture's file path|Person|Person|Person...

loops = input("How many pictures to add?\n")

j = 0

while j<int(loops): #repeat script to bulk-add pictures
    datawrite()
    j+=1