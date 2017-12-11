import random
from math import log10, floor, fmod

gui_available = True

try:
	import pygame
except ImportError:
	gui_available = False

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
square = dimensions**2
u = [[random.random(), random.random()] for x in range(square)]
iterations = 1000000
screen_size = 400
v_points = []
convergent_points = []
temp_convergence = []

step = 1.0 / (dimensions - 1)

for i in range(dimensions):
	for j in range(dimensions):
		convergent_points.append((0.5 * i, 0.5 * j))

print(convergent_points)

data = open("data.txt", "w")

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

if(gui_available):
	pygame.init()
	window = pygame.display.set_mode((screen_size, screen_size))
	pygame.display.set_caption("SOFM")

	def show_points():
		global u
		window.fill((255, 255, 255))
		pygame.draw.circle(window, (255, 0, 0), (int(screen_size * u[0][0]), int(screen_size * u[0][1])), 5)
		for i in range(square):
			pos = (int(screen_size*u[i][0]), int(screen_size*u[i][1]))
			for j in get_neighbours(i):
				end_pos = (int(screen_size*u[j][0]), int(screen_size*u[j][1]))
				pygame.draw.line(window, (0,0,0), pos, end_pos, 5)
		'''		
		for v in v_points:
			pygame.draw.circle(window, (255, 0, 0), (int(v[0] * screen_size), int(v[1] * screen_size)), 2)
		'''
		pygame.display.update()

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

for i in range(iterations):
	a = update_learning_coefficient(i + 1) # Uses i + 1 as log10 can't take 0 as input, has no affect on output
	b = 0.5 * a
	v1 = (random.random(), random.random())
	v_points.append(v1)
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
	if(i % 100 == 0):
		if(i != 0):
			print(str(i / 100))

		data.write(str(i / 100) + "\n")

		if(gui_available):
			show_points()

pygame.quit()
