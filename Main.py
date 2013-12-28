import pygame
from Loops import *
	
pygame.init()
pygame.display.set_caption('Hexmaze!')

scene = 1
while 1:
	if(scene == 0):
		scene = Menu_Loop()
	elif(scene == 1):
		scene = Game_Loop("Level_10")