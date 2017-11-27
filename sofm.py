import random
from math import log10, floor, fmod

# Although this could be written in far fewer lines,
# writing it like this makes plugging in analysis points
# a lot easier at a later date ( and more readable )

# TODO
# -Use pygame to provide simple interface
# -Add way to record convergence
# -Add way to iterate over selection of formulas, starting conditions, etc, and generate convergence

# Current annealing functions:
#   1 / (1 + log10i)
#   ai, 0.8 <= a <= 0.9
#   1 / alog10i, a > 1
#   1 / ai, a > 0 

random.seed(331) # use same seed every time 
dimensions = 3
square = 3**2
u = [[random.random(), random.random()] for x in range(square)]
iterations = 1000000

def get_min_distance(v):
	d_min = 2 # Larger than max distance
	i_min = 0
	for i, e in enumerate(u):
		#print("Calculating distance for u" + str(i))
		d = ((v[0] - e[0])**2) + ((v[1] - e[1])**2)
		#print("The distance is " + str(d))
		if(d < d_min):
			d_min = d
			i_min = i
	
	return i_min

def update_learning_coefficient(a):
	return 1 / (1 + log10(a)) 

def get_neighbours(s):
	n = []
	for i in range(square):
		##print("Is " + str(i) + " a neighbour")
		if(i == s):
			continue
		val = ((floor(s/dimensions) - floor(i/dimensions))**2) + ((fmod(s, dimensions) - fmod(i, dimensions))**2)
		##print(val)
		if(val <= 1**2):
			n.append(i)
	return n

for i in range(iterations):
	a = update_learning_coefficient(i + 1) # Uses i + 1 as log10 can't take 0 as input, has no affect on output
	b = 0.5 * a
	v1 = (random.random(), random.random())
	s = get_min_distance(v1)
	#print("\n\nPoint closest was " + str(s) + ", of value " + str(u[s]))
	u[s][0] = u[s][0] + (a * (v1[0] - u[s][0]))
	u[s][1] = u[s][1] + (a * (v1[1] - u[s][1]))
	#print("Updated u" + str(s) + " is " + str(u[s]))
	
	neighbours = get_neighbours(s)
	for n in neighbours:
		u[n][0] = u[n][0] + (b * (v1[0] - u[n][0]))
		u[n][1] = u[n][1] + (b * (v1[1] - u[n][1]))
		#print("Neighbour " + str(n) + " updated to " + str(u[n]))
	
	#print("\n\n")
