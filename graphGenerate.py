import matplotlib.pyplot as plt
import pickle

x = pickle.load(open("simTime2.dat", "rb"))
temp = x.keys()
y1 = []
y2 = []
y3 = []
y4 = []
for i in x.values():
	y1.append(i[0])
	y2.append(i[1])
	y3.append(i[2])
	y4.append(i[3])

plt.figure(1)

plt.plot (y1)
plt.ylabel('Simulation Time')
plt.xlabel ('Number of Agents')


plt.figure(2)
plt.plot(y2)
plt.ylabel('Avg Distance per Agent')
plt.xlabel('Number of Agents')


plt.figure(3)
plt.plot(y3)
plt.ylabel('Avg Speed per Agent')
plt.xlabel('Number of Agents')


plt.figure(4)
plt.plot(y4)
plt.ylabel('Avg Time per Agent')
plt.xlabel('Number of Agents')

plt.show()
