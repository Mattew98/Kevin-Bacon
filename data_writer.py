import csv

#Prompt

Path = input("Path of picture:\n")
Number = int(input("How many people in photo?\n"))
People = []

#Creating array of people in picture

i = 0
while i < Number:
    person = input("Person " + str(i)+":\n")
    People.append(person)
    i+=1

#Adding new people to database

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
                writer.writerow([str('-')]+[person])

#Adding new pictures to database       

with open('picturedata.csv','a',newline='\n') as data:
    reader=csv.reader(data,delimiter=',')
    writer=csv.writer(data,delimiter=',')
    writer.writerow([Number]+[Path]+People)