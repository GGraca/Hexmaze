import pygame, sys
from pygame.locals import *
from random import * 
from BoxClass import *
from math import*
from Globals import *

class Matrix:
	def __init__(self, tipo):
		self.p = 0
		self.p_spawn = []

		self.objs     = []
		self.mr       = []

		self.positions	  = []
		self.holes    = []
		self.blocked  = []

		if(type(tipo) == str):
			self.read_file(tipo)

		self.matrix_size = (len(self.mr[1]), len(self.mr))

		







#Set-------------------------------------------------------------------------------------------------
	def read_file(self, ficheiro):
		f = open("Levels/" + ficheiro + ".map", 'r')
		string = f.read()
		f.close()

		string = string.translate(None, ' ')
		lista = string.split('\n')

		for i in lista:
			l = []
			k = i.split('.')
			for j in k:
				l.append(j.split(','))
			self.mr.append(l)

		for i in range(len(self.mr)):
			for j in range(len(self.mr[i])):
				if(self.mr[i][j][0] == "Spawn"):
					self.p += 1
					self.p_spawn.append((j,i))


	def set_matrix(self, size):
		self.size = size

		#Matrix
		soma_x = size 					#distancia entre blocos na horizontal
		soma_y = 7 * size / 8			#distancia entre blocos na vertical
		y = (size / 2) #+ self.y_inicial	#pos y inicial

		for i in range(len(self.mr)):
			lista = []
			x = (size / 2)	#+ self.x_inicial		#pos x inicial

			for j in range(len(self.mr[i])):

				self.positions.append((j, i))

				if(i%2 != 0):	k = x 
				else:			k = x + soma_x/2
				a = self.pick_block(self.mr[i][j], (k, y))
				lista.append(a)
				x += soma_x

			self.objs.append(lista)
			y += soma_y


		#Blocked
		#Vertical (excluindo cantos)
		for i in range(len(self.mr)):
			self.blocked.append((-1,i))
			self.blocked.append((len(self.mr[i]),i))

		#Horizontal
		for i in range(-1, len(self.mr[1]) + 1):
			self.blocked.append((i,-1))
			self.blocked.append((i, len(self.mr)))



	def pick_block(self, tipo, (x, y)):
		if(tipo[0] == 'Hole'):			return Hole(xy(x, y), self.size)
		elif(tipo[0] == 'Normal'):		return Normal(xy(x, y), self.size)
		elif(tipo[0] == 'Broken'):		return Broken(xy(x, y), self.size)
		elif(tipo[0] == 'Teleport'):	
			a = Teleport(xy(x, y), self.size)
			a.match = xy(int(tipo[1]), int(tipo[2]))
			return a
		elif(tipo[0] == 'Slider'):
			a = Slider(xy(x, y), self.size)
			a.m = self
			a.set_extras(int(tipo[1]))
			return a
		elif(tipo[0] == 'Smoke'):
			a = Smoke(xy(x, y), self.size)
			a.m = self
			return a
		elif(tipo[0] == "Spawn"):		return Spawn(xy(x, y), self.size)
		else:							return Error(xy(x, y), self.size)









#Update-------------------------------------------------------------------------------------------------
	def update(self, players):
		self.on_off(players)
		self.show_hide(players)



	def show_hide(self, players):
		for i in range(len(self.objs)):
			for j in range(len(self.objs[i])):
				self.objs[i][j].hide()
				try:
					if(self.objs[i][j].hole == True):
						self.holes.append((j,i))
						self.objs[i][j] = Hole(self.objs[i][j].pos, self.size)
					#if(self.objs[i][j].block == True):
					#	self.block.append((j,i))
				except:
					pass

		for p in players:
			self.objs[p.pos.y][p.pos.x].show()
			l = hex_near(p.pos.get())
			for i in l:
				if(i[1] >= 0) and (i[1] < len(self.objs)) and (i[0] >= 0) and (i[0] < len(self.objs[i[1]])):
					self.objs[i[1]][i[0]].show()



	def on_off(self, players):
		for p in players:
			
				#Active
				if(p.active == True):
					self.objs[p.pos.y][p.pos.x].player_active(p)
					p.active = False

				#On
				self.objs[p.pos.y][p.pos.x].player_on(p)


				#Off
				if(p.last_pos.get() != p.pos.get()):
					if(p.last_pos.y >= 0) and (p.last_pos.y < len(self.objs)) and (p.last_pos.x >= 0) and (p.last_pos.x < len(self.objs[p.last_pos.y])):
						self.objs[p.last_pos.y][p.last_pos.x].player_off(p)












#Paint---------------------------------------------------------------------------------------------------
	def paint(self, surface):
		lista = []
		for i in self.objs:
			for j in i:
				lista.append(j)

		todos = tuple(lista)
		allsprites = pygame.sprite.RenderPlain(todos)
		allsprites.draw(surface)
