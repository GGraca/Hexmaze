import os, sys, pygame, random
from pygame.locals import *
from Globals import * 
from Player import *
from MatrixClass import *
from Events import * 

def Game_Loop(nivel):


	m = Matrix(nivel)
	surfs = Game_Surfaces(m.matrix_size, screen_size.get())
	m.set_matrix(surfs.a)

	players = []
	for i in range(m.p):
		players.append(Player(m.p_spawn[i], i))

	inp = In_Game(players)

	while True:
		
		#Update:
		inp.update()
		if(inp.restart):
			return 1

		for p in players:
			p.update(m)

		m.update(players)

		#Paint:
		surfs.world.fill(BLACK)
		m.paint(surfs.world)

		surfs.players.fill(TRCOLOR)
		for p in players:
			p.paint(surfs.players)	
		
		#Blit:
		screen.blit(surfs.world, (surfs.world_pos))
		screen.blit(surfs.players, surfs.players_pos)
		pygame.display.flip()