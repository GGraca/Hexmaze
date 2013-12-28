import pygame, sys, copy
from pygame.locals import *
from random import *
from Globals import *
from Funcoes import *


class Box(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		self.pos  = pos
		self.size = int(size)
		self.h    = False

		self.hole = False
		self.block = False
		self.arg = None



		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((self.size, self.size))
		self.image.set_colorkey(TRCOLOR)
		self.img_pl = load_image("stone")
		self.fog = pygame.transform.smoothscale(load_image('fog'), (self.size, self.size))

		self.set_extras()

		self.hide()
		self.rect = self.image.get_rect()
		self.rect.center = pos.get()

	def show(self):
		if(self.h == False):
			self.image.fill(TRCOLOR)
			self.image = pygame.transform.smoothscale(self.img, (self.size, self.size))
			self.img_pl = self.img
		else:
			self.hide()

	def hide(self):
		self.image.fill(TRCOLOR)
		self.image = pygame.transform.smoothscale(self.img_pl, (self.size, self.size))
		self.image.blit(self.fog, (0,0))

	def player_on(self, p):
		pass
	def player_off(self, p):
		pass
	def player_active(self, p):
		pass

class Normal(Box):
	def set_extras(self):
		#self.blocked = True
		self.img = load_image('stone')

class Error(Box):
	def set_extras(self):
		self.img = load_image('error')

class Spawn(Box):
	def set_extras(self):
		self.img = load_image('spawn')

class Hole(Box):
	def set_extras(self):
		self.img = load_image('empty')
	def hide(self):
		self.image.fill(TRCOLOR)
		self.image = pygame.transform.smoothscale(self.img, (self.size, self.size))
	def player_on(self, p):
		p.spawn()

class Broken(Box):
	def set_extras(self):
		self.img_empty = load_image('empty')
		self.img_broken = load_image('broken')
		self.img = self.img_broken
	
	def player_off(self, p):
		self.hole = True
		self.img = self.img_empty

class Teleport(Box):
	def set_extras(self):
		self.match = None
		self.img = load_image('teleport')

	def player_on(self, p):
		p.dist.set(self.match.get())

class Smoke(Box):
	def set_extras(self):
		self.hex = None

	def show(self):
		self.hide()

	def player_on(self, p):
		if(self.hex == None):
			self.hex = hex_near(p.pos.get())
		for i in  self.hex:
			self.m.objs[i[1]][i[0]].h = True

	def player_off(self, p):
		for i in  self.hex:
			self.m.objs[i[1]][i[0]].h = False

class Slider(Box):
	def set_extras(self, a = 1):
		self.direccao = a
		string = "slider_" + str(a)
		self.img = load_image(string)
		

	def player_active(self, p):
		if(self.direccao == 1):		self.dir_d(p, 1, 4, True)
		elif(self.direccao == 2):	self.dir_d(p, 2, 5, True)	
		elif(self.direccao == 3):	self.dir_h(p, 'direita')
		elif(self.direccao == 4):	self.dir_d(p, 1, 4, False)
		elif(self.direccao == 5):	self.dir_d(p, 2, 5, False)
		elif(self.direccao == 6):	self.dir_h(p, 'esquerda')

	def dir_d(self, p, a, b, d):

		pos      = p.pos.get()
		pos_vals = []
		pos_m 	 = []
		new_line = []
		lado = 0
		
		#Anda na diagnal para cima, ate um canto
		while(pos[1] != 0) and (pos in self.m.positions):
			pos = near_pos(pos, a)
		if(pos[1]==0) and (pos not in self.m.positions):
			pos = near_pos(pos, b)
		elif(pos not in self.m.positions):
			pos = near_pos(pos, b)

		#Anda na diagonal para a direita baixo ate um canto e guarda pos e objs
		while(pos in self.m.positions):
			if(self.m.objs[pos[1]][pos[0]].block == False):
				pos_m.append(pos)										#posicoes na matrix
				pos_vals.append(self.m.objs[pos[1]][pos[0]].pos.get())	#posicoes em pixeis
				new_line.append(self.m.objs[pos[1]].pop(pos[0]))		#objecto
			pos = near_pos(pos, b)



		if(d == True):
			k = new_line.pop(0)
			new_line.append(k)
		else:
			k = new_line.pop(-1)
			new_line.insert(0, k)

		for i in range(len(pos_vals)):
			new_line[i].pos.set(pos_vals[i])
			new_line[i].rect.center = new_line[i].pos.get()

		for i in range(len(pos_m)):
			self.m.objs[pos_m[i][1]].insert(pos_m[i][0], new_line[i])

	def dir_h(self, p, d):
		y = p.pos.y
		x = len(self.m.objs[y])
		new_line = []
		pos_vals = []

		for i in range(x):
			#if(self.m.objs[y][i].block == False):
			pos_vals.append(self.m.objs[y][i].pos.get())

		if(d == 'direita'):
			new_line.append(self.m.objs[y].pop(x - 1))
			while len(self.m.objs[y]) != 0:
				new_line.append(self.m.objs[y].pop(0))
		else:
			while len(self.m.objs[y]) != 1:
				new_line.append(self.m.objs[y].pop(1))
			new_line.append(self.m.objs[y].pop(0))

		for i in range(x):
			new_line[i].pos.set(pos_vals[i])
			new_line[i].rect.center = new_line[i].pos.get()
		self.m.objs[y] = new_line
