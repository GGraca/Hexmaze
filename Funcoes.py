import pygame
from math import * 

class xy:
	def __init__(self, x, y):
		self.set(x, y)
	def set(self, x, y = None):
		if(y == None):
			self.x = x[0]
			self.y = x[1]
		else:
			self.x = x
			self.y = y
	def get(self):
		return self.x, self.y

def load_image(name):
	try:
		return pygame.image.load("Images/" + name + ".png")
	except:
		print "Unable to load image: " + name

def hex_near((x,y)):
	l = []
	if(y%2 != 0):	d = -1
	else:	d = 0

	for a in range(-1, 2):
		for b in range(d, d+2):
			if(a == 0):
				if(b == d + 1):		b += 1
				if(y%2 == 0):		b -= 1
			l.append((x + b, y + a))
	return l

def near_pos((x, y), d):
	if(y%2 != 0):	a = 0
	else:				a = 1	

	if(d == 1):		return (x+a-1, y-1)
	if(d == 2): 	return (x+a, y-1)
	if(d == 3): 	return (x+1, y)
	if(d == 4): 	return (x+a, y+1)
	if(d == 5): 	return (x+a-1, y+1)
	if(d == 6): 	return (x-1, y)

def square_colision((x1, y1), (x2, y2), d):
	x = False
	y = False

	if abs(x1 - x2) <= d:
		x = True
	if abs(y1 - y2) <= d:
		y = True

	if(x and y):	return True