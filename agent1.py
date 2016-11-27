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
dt = 1.0/3

def createGrid1():
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

def CreateGrid2():
    rt1 = shapes.circle(radius=100, pos=(200,150))
    rt2 = shapes.circle(radius=50, pos=(100,450))
    rt3 = shapes.circle(radius=125, pos=(400,300))
    rt4 = shapes.circle(radius=20, pos=(550,100))
    rt5 = shapes.circle(radius=25, pos=(500,450))

    extrusion(shape=rt1, color=color.red)
    extrusion(shape=rt2, color=color.red)
    extrusion(shape=rt3, color=color.red)
    extrusion(shape=rt4, color=color.red)
    extrusion(shape=rt5, color=color.red)

    scene.center = (300, 300, 0)


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

def getData1 (na, isdisplay=0, readFromFile="y"):
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
    if os.path.isfile("building1.dat") and os.path.isfile("doors1.dat"):
        if cmp(building, pickle.load(open("building1.dat", "rb"))) == 0 and cmp(doors, pickle.load(open("doors1.dat", "rb"))) == 0:
            isChanged = False
        else:
            pickle.dump(building, open("building1.dat", "wb"))
            pickle.dump(doors, open("doors1.dat", "wb"))
    else:
        pickle.dump(building, open("building1.dat", "wb"))
        pickle.dump(doors, open("doors1.dat", "wb"))

    # readFromFile = str(raw_input("Search and read from File (y/n) : "))
    
    start_time = time.time()
    if (readFromFile == "y"):
        if os.path.isfile("allpaths1.dat") and not isChanged:
            print "FILE STREAM"
            allPaths = pickle.load(open("allpaths1.dat", "rb"))
        else:
            print "CALCULATIONS"
            allPaths.update(inOffice(office, building, gridSize))
            allPaths.update(toOffice(doors, office, building, gridSize))
            pickle.dump(allPaths, open("allpaths1.dat", "wb"))
        
    else:
        allPaths.update(inOffice(office, building, gridSize))
        allPaths.update(toOffice(doors, office, building, gridSize))
        pickle.dump(allPaths, open("allpaths1.dat", "wb"))
    print ("--- %s seconds ---" % (time.time() - start_time))

    
    # na = int(input("No of Agents : "))
    agentType = [oldStudent, newStudent, faculty, staff]
    agentColor = [color.green, color.orange, color.blue, color.magenta]
    users = []
    noOfAgent = [0,0,0,0]
    if isdisplay == 1:
        createGrid1()
    start_time = time.time()
    for i in range(0, na):
        x = random.randint(0,4)
        # print x, agentType[x]
        noOfAgent[x] = noOfAgent[x]+1
        location = doors.keys()[random.randint(0,3)]
        users.append([])
        users[i].append(agentType[x].FSM())
        users[i].append(sphere(pos=doors[location], radius=rd, color=agentColor[x], velocity=vector(0, 0, 0), visible=False))
        if isdisplay == 1:
            users[i][1].visible = True
        # users[i].append(sphere(pos=doors[location], radius=rd, color = agentColor[x], velocity=vector(0,0,0), visible = False))
        users[i].append(location) #Source 2
        users[i].append(location) #Destination 3
        users[i].append([vector(0,0,0)]) #Direction 4
        users[i].append([])
        (isOver, nextDest) = (False, "None")
        while not isOver:
            (isOver, nextDest) = users[i][0].getNextState()
            users[i][5].append(nextDest)
        # print users[i][5]

    # print noOfAgent

    markDel = []
    while len(users)-len(markDel) > 0 :
        # print len(markDel)
        if isdisplay == 1:
            rate(50)
        
        for x in range(0, len(users)):
            if x in markDel:
                continue
            if hasReached (position[users[x][3]], users[x][1].pos, building, doors, users[x][3]):
                # print users[x][5]
                #If reached Destination
                # users[x][1].velocity = vector(0,0,0)
                
                if len(users[x][5]) == 0:
                    # Destination is Exit
                    # print "Deleted", users[x]
                    markDel.append(x)
                    # print len(users)
                    continue
                else :
                    # (isOver, nextDest) = (False, "None")
                    # (isOver, nextDest) = users[x][0].getNextState()
                    # print users[x][3]
                    nextDest = users[x][5][0]
                    # print nextDest
                    del users[x][5][0]
                    # if isOver:
                        # users[x].append("delete")
                        # print x , " is Over"
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
        markDel = []
    # print "Done!!!"
    return time.time() - start_time
    # print ("--- %s seconds ---" % (time.time() - start_time))


def getData2(na, isdisplay=0, readFromFile="y"):
    gridSize = 600
    office = {'Admin': (200, 150, 100), 'CC3': (100, 450, 50), 'Ground': (400, 300, 125),
              'HQ': (550, 100, 20), 'Cafeteria': (500, 50, 25)}

    doors = {'Main-Gate': (150, 0, 0), 'Pocket-Gate': (400, 0, 0)}

    building = {}
    building.update(office)

    position = {}
    position.update(building)
    position.update(doors)

    allPaths = {}
    isChanged = True
    if os.path.isfile("building2.dat") and os.path.isfile("doors2.dat"):
        if cmp(building, pickle.load(open("building2.dat", "rb"))) == 0 and cmp(doors, pickle.load(open("doors2.dat", "rb"))) == 0:
            isChanged = False
        else:
            pickle.dump(building, open("building2.dat", "wb"))
            pickle.dump(doors, open("doors2.dat", "wb"))
    else:
        pickle.dump(building, open("building2.dat", "wb"))
        pickle.dump(doors, open("doors2.dat", "wb"))

    # readFromFile = str(raw_input("Search and read from File (y/n) : "))

    start_time = time.time()
    if (readFromFile == "y"):
        if os.path.isfile("allpaths2.dat") and not isChanged:
            print "FILE STREAM"
            allPaths = pickle.load(open("allpaths2.dat", "rb"))
        else:
            print "CALCULATIONS"
            allPaths.update(inOffice(office, building, gridSize))
            allPaths.update(toOffice(doors, office, building, gridSize))
            pickle.dump(allPaths, open("allpaths2.dat", "wb"))

    else:
        allPaths.update(inOffice(office, building, gridSize))
        allPaths.update(toOffice(doors, office, building, gridSize))
        pickle.dump(allPaths, open("allpaths2.dat", "wb"))
    print ("--- %s seconds ---" % (time.time() - start_time))

    # na = int(input("No of Agents : "))
    agentType = [externalStudent, internalStudent]
    agentColor = [color.green, color.orange]
    users = []
    noOfAgent = [0, 0, 0, 0]
    if isdisplay == 1:
        createGrid1()
    start_time = time.time()
    for i in range(0, na):
        x = random.randint(0, 2)
        # print x, agentType[x]
        noOfAgent[x] = noOfAgent[x] + 1
        location = x
        users.append([])
        users[i].append(agentType[x].FSM())
        users[i].append(sphere(pos=doors[location], radius=rd, color=agentColor[x], velocity=vector(0, 0, 0), visible=False))
        if isdisplay == 1:
            users[i][1].visible = True
        # users[i].append(sphere(pos=doors[location], radius=rd, color = agentColor[x], velocity=vector(0,0,0), visible = False))
        users[i].append(location)  # Source 2
        users[i].append(location)  # Destination 3
        users[i].append([vector(0, 0, 0)])  # Direction 4
        users[i].append([])
        (isOver, nextDest) = (False, "None")
        while not isOver:
            (isOver, nextDest) = users[i][0].getNextState()
            users[i][5].append(nextDest)
            # print users[i][5]

    # print noOfAgent

    markDel = []
    while len(users) - len(markDel) > 0:
        # print len(markDel)
        if isdisplay == 1:
            rate(50)

        for x in range(0, len(users)):
            if x in markDel:
                continue
            if hasReached(position[users[x][3]], users[x][1].pos, building, doors, users[x][3]):
                # print users[x][5]
                # If reached Destination
                # users[x][1].velocity = vector(0,0,0)

                if len(users[x][5]) == 0:
                    # Destination is Exit
                    # print "Deleted", users[x]
                    markDel.append(x)
                    # print len(users)
                    continue
                else:
                    # (isOver, nextDest) = (False, "None")
                    # (isOver, nextDest) = users[x][0].getNextState()
                    # print users[x][3]
                    nextDest = users[x][5][0]
                    # print nextDest
                    del users[x][5][0]
                    # if isOver:
                    # users[x].append("delete")
                    # print x , " is Over"
                    users[x][2] = users[x][3]
                    users[x][3] = nextDest
            # print "users[x][3] = ", users[x][3], "Over"
            socialForce = fagent(users[x], users) + fbuilding(users[x], building) + ftarget(users[x], users,
                                                                                            position[users[x][3]][0],
                                                                                            position[users[x][3]][1])
            users[x][1].velocity = users[x][1].velocity + socialForce * dt
            if (mag(users[x][1].velocity) > v0):
                users[x][1].velocity = v0 * norm(users[x][1].velocity)
            users[x][1].pos = users[x][1].pos + users[x][1].velocity * dt
            # check(i, na)

        for i in markDel:
            del users[i]
        markDel = []
    # print "Done!!!"
    return time.time() - start_time
    # print ("--- %s seconds ---" % (time.time() - start_time))

# simTime = pickle.load(open("simtime1.dat", "rb"))
# print simTime
# for i in range(27,80):
#     simTime[i] = getData1(i)
#     print i, simTime[i]
#     pickle.dump(simTime, open("simtime1.dat", "wb"))