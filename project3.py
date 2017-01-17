import random as r
import math as m
from visual import *
p=0.3
a=20
b=30
allpaths=[]
curpos=[]
curvel=[]
direction=[]
##----------constants used in social force model--------------##
v0=1.5
rd=0.35
t=0.5
A=2000
B=0.15
k=120000
K=240000
dt=1.0/9
chk=[]
def inc():
    return 10

#calculates shortest distance from start node
def dijkstra(nodes,e,wt,initial):
    visited = {initial: 0}
    path = {}
    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]
        for edge in e[min_node]:
            weight = current_weight + wt[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node
    return visited,path


def delta():
    return 0.5

# calculates sqaure of euclidean distance
def getDist(p1,p2):
    d=(p1[0]-p2[0])**2+(p1[1]-p2[1])**2
    return d

# checks if point lies outside obstacles
def feasibleCheckPoint(build,point):
    num=len(build)
    chk=False
    for i in range(0,num):
        d=getDist(point,build[i])
        if d<=build[i][2]**2:
            chk=True
            break
    if chk==True:
        return False
    else:
        return True

# randomly generates points inside the grid
def generatePoints(n,numOfPoints,build):
    dic={}
    v=[]
    for i in range(0,numOfPoints):
        point=(int(r.randrange(0,n,1)),int(r.randrange(0,n,1)))
        while(feasibleCheckPoint(build,point)==False or point in dic ):
            point=(int(r.randrange(0,n,1)),int(r.randrange(0,n,1)))
        dic[point]=1;
        v.append(point)    
    return v;

# checks if edge crosses the obstacles or not
def feasibleEdgeCheck(p1,p2,build):
    if m.sqrt(getDist(p1,p2))<delta():
        return True
    mid=((p1[0]+p2[0])/2.0,(p1[1]+p2[1])/2.0)
    if feasibleCheckPoint(build,mid)==False:
        return False
    return feasibleEdgeCheck(p1,mid,build) and feasibleEdgeCheck(mid,p2,build)

# generates valid edges between vetices which are less than D distance apart
def generateEdges(v,build,D):
    num=len(v)
    e=dict()
    wt={}
    for i in range(0,num):
        if v[i] not in e:
            e[v[i]]=[]
        for j in range(0,num):
            if i==j:
                continue
            if getDist(v[i],v[j])<=D*D:
                if feasibleEdgeCheck(v[i],v[j],build)==True:
                    e[v[i]].append(v[j])
                    wt[(v[i],v[j])]=m.sqrt(getDist(v[i],v[j]))

    return e,wt

# stores the shortest path to goal for each agent in allpaths
def printPath(start,goal,path):
    global allpaths
    path1=[]
    while goal in path:
        path1=[goal]+path1
        goal=path[goal]
    path1=[start]+path1
    # print (path1)
    # allpaths.append(path1)
    return path1
    
# calculates force due to target on an agent according to social force model 
def ftarget(i,na,gx,gy) :
    global direction
    direction[i]=norm(vector(gx,gy,0)-vector(curpos[i][0],curpos[i][1],0))
    avg=vector(0,0,0)
    tot=0
    for a in range(0,na):
        if a!=i and mag(vector(curpos[i][0],curpos[i][1],0)-vector(curpos[a][0],curpos[a][1],0))<=20 :
            avg+=direction[i];
            tot+=1
    if tot!=0:
        avg/=tot
    
    direction[i]=norm((1-p)*direction[i]+p*avg)
    v=(v0*direction[i]-curvel[i])/t
    #print("target")
    #print( v.x,v.y)
    return v

# calculates force due to other agents on an agent according to social force model 
def fagent(s,na) :
    global chk
    tf=vector(0,0,0)
    for i in range (0,na) :
        if i!=s:# and not chk[i] :
            nij=norm(vector(curpos[s][0],curpos[s][1],0)-vector(curpos[i][0],curpos[i][1],0))
            dij=mag(vector(curpos[s][0],curpos[s][1],0)-vector(curpos[i][0],curpos[i][1],0))
            tij=vector(-nij.y,nij.x,0)
            dvji=dot(curvel[i]-curvel[s],tij)
            rij=2*rd
            if dij>rij:
                g=0
            else:
                g=rij-dij
            tf=tf+(A*m.exp((rij-dij)/B)+k*g)*nij+K*g*dvji*tij
    #print(tf.x,tf.y)
    return tf


# calculates force due to obstacles on an agent according to social force model 
def fbuilding(s,build) :
    global chk
    tf=vector(0,0,0)
    l=len(build)
    for i in range (0,l) :
        nij=norm(vector(curpos[s][0],curpos[s][1],0)-vector(build[i][0],build[i][1],0))
        dij=mag(vector(curpos[s][0],curpos[s][1],0)-vector(build[i][0],build[i][1],0))
        tij=vector(-nij.y,nij.x,0)
        dvji=dot(curvel[s],tij)
        rij=rd+build[i][2]
        if dij>rij:
            g=0
        else:
            g=rij-dij
        tf=tf+(A*m.exp((rij-dij)/0.01)-k*g)*nij+K*g*dvji*tij
    return tf

# debug fucntion for colusion detection!
def check(s,na) :
    global chk
    for i in range(0,na) :
        d=m.sqrt((curpos[i][0]-curpos[s][0])**2 + (curpos[i][1]-curpos[s][1])**2)


# simulates collision free basic motion along a path for an agent
def simulatepaths(build,na,goal) :
    agent=[]
    l=len(build)
    sphere(pos=(goal[0],goal[1]),radius=1)
    deltat = 0.0005
    nextgoal={}
    vectors=[]
    for i in range(0,l):
        sphere(pos=(build[i][0],build[i][1]),radius=(build[i][2]))
        
    for i in range (0,na):
        agent.append(sphere(pos=(allpaths[i][0][0],allpaths[i][0][1]),radius=rd))
        agent[i].velocity=vector(0,0,0)
        curpos[i][0]=allpaths[i][0][0]
        curpos[i][1]=allpaths[i][0][1]
        curvel[i]=vector(0,0,0)
        nextgoal[i]=1    
    while True:
        rate(50)
        flag=0
        for i in range (0,na):
            if nextgoal[i]!=len(allpaths[i]):
                flag=1
                break
        if flag==0:
            break
        for i in range (0,na):
            if nextgoal[i]==len(allpaths[i]) :
                continue
            force=fagent(i,na)+fbuilding(i,build)+ftarget(i,na,allpaths[i][nextgoal[i]][0],allpaths[i][nextgoal[i]][1])
            agent[i].velocity=agent[i].velocity+force*dt
            if mag(agent[i].velocity)>v0:
                agent[i].velocity=v0*norm(agent[i].velocity)
            agent[i].pos=agent[i].pos+agent[i].velocity*dt
            curpos[i][0]=agent[i].pos.x
            curpos[i][1]=agent[i].pos.y
            curvel[i]=agent[i].velocity
            check(i,na)
            if ((agent[i].pos.x-allpaths[i][nextgoal[i]][0])**2 + (agent[i].pos.y-allpaths[i][nextgoal[i]][1])**2)<rd :
                nextgoal[i]=nextgoal[i]+1
                if nextgoal[i]==len(allpaths[i]):
                    agent[i].velocity=vector(0,0,0)
                    curvel[i]=vector(0,0,0)
                    chk[i]=True
 
# generates a probabilistic roadmap 
def prm(start,goal,n,build,D):
    global a
    global b
    numOfPoints=int(r.randrange(a,b,1))
    v=generatePoints(n,numOfPoints,build)
    v.append(start)
    v.append(goal)
    (e,wt)=generateEdges(v,build,D)
    (visited,path)=dijkstra(v,e,wt,start)
    if (goal in visited)==False:
        a=a+inc()
        b=b+inc()
        return prm(start,goal,n,build,2*D)
    else:
        return printPath(start,goal,path)
        
# used for getting inputs from user
def getData():
    global a
    global b
    a=20
    b=30
    n=int(input("Enter Grid Size:"))
    start=(int(input("Enter X-cord of Starting point:")),int(input("Enter Y-cord of Starting point:")))
    goal=(int(input("Enter X-cord of Goal point:")),int(input("Enter Y-cord of Goal point:")))
    D=(m.sqrt((start[0]-goal[0])**2+(start[1]-goal[1])**2))//10
   
    numOfBuild=int(input("Enter No. of buildings:"))
    na=int(input("Enter no of Agents:"))
    build=[]
    # goal1=[]
    for i in range(0,numOfBuild):
        build.append([])
        build[i].append(int(input()))
        build[i].append(int(input()))
        build[i].append(int(input()))
        if D==0:
            D=build[i][2]
        if build[i][2]!=0 and build[i][2]<D:
            D=build[i][2]

    for i in range(0,na):
        chk.append([])
        chk[i].append(False)
        a=20
        b=30
        x = prm(start,goal,n,build,D)
        allpaths.append(x)
        curpos.append([])
        curvel.append([])
        direction.append([])
        # goal1.append([])
        curpos[i].append(0)
        curpos[i].append(0)
        curvel[i].append(vector(0,0,0))
        direction[i].append(vector(0,0,0))
        # goal1[i].append((na-i)*(n/na))
        # goal1[i].append(n)
    simulatepaths(build,na,goal)
    #simulatepaths2(n,na,goal1)

# getData()