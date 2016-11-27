import os
import pickle
import math as m
import random
import time
from visual import *
# from collections import namedtuple
import project3 as helper

# FSM imports
import oldStudent
import newStudent
import faculty
import staff

# Exam Cell - 0,0,25
# Pillar1 - 0,50,5
# Pillar2 - 0,50,5
# Reception - -50,75,5
# Account(Stu) - -65,30,10
# Account(Pri) - -65,-30,10
# Director - -50,-75,5
# COW - 50,75,5
# Dean(Aca) - 0,-75,10
# Dean(SA) - 70,0,15
# Bank - 50,-50,10

p = 0.3
v0 = 1.5
rd = 2
t = 0.5
A = 2000
B = 0.15
k = 120000
K = 240000
dt = 1.0/9

def createGrid():
    # rt = shapes.rectangle(width=200, height=200, thickness=0.03)

    scene.show_rendertime = True
    rt1 = shapes.circle(radius=25,pos=(100,100))
    rt2 = shapes.circle(radius=5,pos=(50,175))
    rt3 = shapes.circle(radius=5,pos=(50,25))
    rt5 = shapes.circle(radius=5,pos=(150,175))
    rt4 = shapes.circle(radius=10,pos=(35,130))
    rt6 = shapes.circle(radius=10,pos=(35,70))
    rt7 = shapes.circle(radius=10,pos=(100,25))
    rt8 = shapes.circle(radius=15,pos=(170,100))
    rt9 = shapes.circle(radius=10,pos=(150,50))

    cr1 = shapes.circle(radius=5, np=64, pos=(100,150))
    cr2 = shapes.circle(radius=5, np=64,pos=(100,50))


    extrusion(shape=rt1,color=color.red)
    extrusion(shape=rt2,color=color.red)
    extrusion(shape=rt3,color=color.red)
    extrusion(shape=rt4,color=color.red)
    extrusion(shape=rt5,color=color.red)
    extrusion(shape=rt6,color=color.red)
    extrusion(shape=rt7,color=color.red)
    extrusion(shape=rt8,color=color.red)
    extrusion(shape=rt9,color=color.red)
    extrusion(shape=cr1,color=color.cyan)
    extrusion(shape=cr2,color=color.cyan)
    # extrusion(shape=rt,color=color.yellow)
    scene.center = (100,100,0)
    # scene.userzoom = True
    # scene.userpin = True

def inOffice(office, building, gridSize):
    allPaths = {}
    for x in office.keys():
        for y in office.keys():
            if x == y or allPaths.has_key((x, y)):
                continue
            else:
                temp = {}
                temp.update(building)
                del temp[x]
                del temp[y]
                start = office[x][0:2]
                goal = office[y][0:2]
                D=(m.sqrt((start[0]-goal[0])**2+(start[1]-goal[1])**2))//10
                if D == 0:
                    D = 5
                val = helper.prm(start, goal, gridSize, temp.values(), D)
                allPaths[(x, y)] = val
                allPaths[(y, x)] = val
    return allPaths

def toOffice(doors, office, building, gridSize):
    allPaths = {}
    for x in office.keys():
        for y in doors.keys():
            temp = {}
            temp.update(building)
            del temp[x]

            start = doors[y][0:2]
            goal = office[x][0:2]

            D=(m.sqrt((start[0]-goal[0])**2+(start[1]-goal[1])**2))//10
            if D == 0:
                D = 5

            val = helper.prm(start, goal, gridSize, temp.values(), D)
            allPaths[(x, y)] = val
            allPaths[(y, x)] = val
    return allPaths


def hasReached (curPos, dest, building, doors, location):
    if location in building:
        if mag(vector(curPos[0], curPos[1], 0) - vector(dest[0], dest[1], 0)) <= building[location][2] + rd + rd:
            return True
    else:
         if mag(vector(curPos[0], curPos[1], 0) - vector(dest[0], dest[1], 0)) <= rd + rd:
             return True
    return False

def fagent(curAgent, users):
    tf = vector(0,0,0)
    for i in users:
        if curAgent != i:
            tempVal = vector(curAgent[1].pos[0], curAgent[1].pos[1], 0) - vector(i[1].pos[0], i[1].pos[1], 0)
            nij = norm(tempVal)
            dij = mag(tempVal)
            tij = vector(-nij.y, nij.x, 0)
            dvji = dot(i[1].velocity - curAgent[1].velocity, tij)
            rij = 2*rd
            if dij > rij:
                g=0
            else:
                g = rij - dij
            tf=tf+(A*m.exp((rij-dij)/B)+k*g)*nij+K*g*dvji*tij
    return tf


def fbuilding(curAgent, building):
    tf = vector(0,0,0)
    for i in building.values():
        tempVal = vector(curAgent[1].pos[0], curAgent[1].pos[1], 0) - vector(i[0], i[1], 0)
        nij = norm(tempVal)
        dij = mag(tempVal)
        tij = vector(-nij.y, nij.x, 0)
        dvji = dot(curAgent[1].velocity, tij)
        rij = rd + i[2]
        if dij>rij:
            g=0
        else:
            g=rij-dij
        tf=tf+(A*m.exp((rij-dij)/0.01)-k*g)*nij+K*g*dvji*tij
    return tf

def ftarget(curAgent, users, gx, gy):
    curAgent[4] = norm(vector(gx, gy, 0) - vector(curAgent[1].pos[0], curAgent[1].pos[1], 0))
    avg = vector(0, 0, 0)
    tot = 0
    for a in users:
        if a != curAgent and mag(vector(curAgent[1].pos[0], curAgent[1].pos[1], 0) - vector(a[1].pos[0], a[1].pos[1], 0)) <= 20 :
            avg = avg + curAgent[4]
            tot = tot + 1
    if tot != 0:
        avg = avg / tot
    
    curAgent[4] = norm((1-p)*curAgent[4]+p*avg)
    v = (v0 * curAgent[4] - curAgent[1].velocity)/t
    return v

def getData ():
    gridSize = 200
    office = {'Director': (50, 25, 5), 'Dean-Affairs': (170, 100, 15), 'COW': (150, 175, 5), 'Exam-Cell': (100, 100, 25), 'Dean-Academics': (100,
    25, 10), 'Accounts-Priority': (35, 70, 10), 'Accounts-Student': (35, 130, 10), 'Reception': (50, 175, 5),
    'Bank': (150, 50, 10)}

    doors = {'Exit1': (185, 0, 0), 'Exit2': (185, 200, 0), 'Entry': (15, 200, 0)}

    building = {'Pillar1': (100, 150, 5), 'Pillar2': (100, 50, 5)}
    building.update(office)

    position = {}
    position.update(building)
    position.update(doors)

    allPaths = {}
    isChanged = True
    if os.path.isfile("building.dat") and os.path.isfile("doors.dat"):
        if cmp(building, pickle.load(open("building.dat", "rb"))) == 0 and cmp(doors, pickle.load(open("doors.dat", "rb"))) == 0:
            isChanged = False
        else:
            pickle.dump(building, open("building.dat", "wb"))
            pickle.dump(doors, open("doors.dat", "wb"))

    readFromFile = str(raw_input("Search and read from File (y/n) : "))
    
    start_time = time.time()
    if (readFromFile == "y"):
        if os.path.isfile("allPaths.dat") and not isChanged:
            print "FILE STREAM"
            allPaths = pickle.load(open("allPaths.dat", "rb"))
        else:
            print "CALCULATIONS"
            allPaths.update(inOffice(office, building, gridSize))
            allPaths.update(toOffice(doors, office, building, gridSize))
            pickle.dump(allPaths, open("allPaths.dat", "wb"))
        
    else:
        allPaths.update(inOffice(office, building, gridSize))
        allPaths.update(toOffice(doors, office, building, gridSize))
        pickle.dump(allPaths, open("allPaths.dat", "wb"))
    print ("--- %s seconds ---" % (time.time() - start_time))

    
    na = int(input("No of Agents : "))
    agentType = [oldStudent, newStudent, faculty, staff]
    agentColor = [color.green, color.orange, color.blue, color.magenta]
    users = []
    noOfAgent = [0,0,0,0]
    # noOfLocation = {}
    createGrid()
    for i in range(0, na):
        x = random.randint(0,4)
        # print x, agentType[x]
        noOfAgent[x] = noOfAgent[x]+1
        location = doors.keys()[random.randint(0,3)]
        # location = 'Entry'
        # print location
        # if (noOfLocation.has_key(location)):
            # noOfLocation[location] = noOfLocation[location] + 1
        # else:
            # noOfLocation[location] = 1
        users.append([])
        users[i].append(agentType[x].FSM())
        users[i].append(sphere(pos=doors[location], radius=rd, color = agentColor[x], velocity=vector(0,0,0)))
        users[i].append(location) #Source 2
        users[i].append(location) #Destination 3
        users[i].append([vector(0,0,0)]) #Direction 4
        users[i].append(x)

    print noOfAgent

    while len(users) > 0 :
        rate(200)
        markDel = []
        
        for x in range(0, len(users)):
            # print x
            if hasReached (position[users[x][3]], users[x][1].pos, building, doors, users[x][3]):
                # print users[x][5]
                #If reached Destination
                # users[x][1].velocity = vector(0,0,0)
                
                if len(users[x]) == 7:
                    # Destination is Exit
                    print "Deleted", users[x]
                    markDel.append(x)
                    # print len(users)
                    continue
                else :
                    (isOver, nextDest) = (False, "None")
                    (isOver, nextDest) = users[x][0].getNextState()
                    if isOver:
                        users[x].append("delete")
                        print x , " is Over"
                    users[x][2] = users[x][3]
                    users[x][3] = nextDest
            # print "users[x][3] = ", users[x][3], "Over"
            socialForce = fagent(users[x], users) + fbuilding(users[x], building) + ftarget(users[x], users, position[users[x][3]][0], position[users[x][3]][1])
            users[x][1].velocity = users[x][1].velocity + socialForce*dt
            if (mag (users[x][1].velocity) > v0):
                users[x][1].velocity = v0 * norm(users[x][1].velocity)
            users[x][1].pos = users[x][1].pos + users[x][1].velocity*dt
            # check(i, na)

        for i in markDel:
            del users[i]



getData()