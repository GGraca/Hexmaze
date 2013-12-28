import os, sys, pygame, random
from pygame.locals import *
from Globals import *
from Funcoes import *

class In_Game:
	def __init__(self, players):
		self.player_action = False
		self.matrix_action = False
		self.restart = 0

		self.players = players
		self.clock = pygame.time.Clock()
		self.set_player_keys()

	def set_player_keys(self):
		for p in self.players:
			p.k['cima'] = globals()[p.k['cima']]
			p.k['baixo'] = globals()[p.k['baixo']]
			p.k['esquerda'] = globals()[p.k['esquerda']]
			p.k['direita'] = globals()[p.k['direita']]
			p.k['active'] = globals()[p.k['active']]

	def update(self):
		self.clock.tick(30)

		for event in pygame.event.get():
			if event.type == QUIT:
				quit()
				sys.exit()

			#INPUT
			for p in self.players:
				self.input(p, event)


	def input(self, p, e):
		if e.type == KEYDOWN:
			if e.key == p.k['direita']:
				if p.k['key'] == None:
					p.k['key'] = "direita"
					p.k['diagonal'] = False
			if e.key == p.k['esquerda']:
				if p.k['key'] == None:
					p.k['key'] = "esquerda"
					p.k['diagonal'] = False
			if e.key == p.k['cima']:
				if p.k['key'] == None:
					p.k['key'] = "cima"
			if e.key == p.k['baixo']:
				if p.k['key'] == None:
					p.k['key'] = "baixo"

				
		if e.type == KEYUP:
			if(e.key == K_r):
				self.restart = True


			if e.key == p.k['direita']:
				if(p.k['key'] == "direita"):
					p.k['key'] = None
					if(p.k['diagonal'] != True):
						p.dist.set(near_pos(p.pos.get(), 3))
				elif(p.k['key'] == "baixo"):
					p.dist.set(near_pos(p.pos.get(), 4))
				elif(p.k['key'] == "cima"):
					p.dist.set(near_pos(p.pos.get(), 2))

			elif e.key == p.k['esquerda']:
				if(p.k['key'] == "esquerda"):
					p.k['key'] = None
					if(p.k['diagonal'] != True):
						p.dist.set(near_pos(p.pos.get(), 6))
				elif(p.k['key'] == "baixo"):
					p.dist.set(near_pos(p.pos.get(), 5))
				elif(p.k['key'] == "cima"):
					p.dist.set(near_pos(p.pos.get(), 1))

			elif e.key == p.k['cima']:
				if(p.k['key'] == "cima"):
					p.k['key'] = None
				elif(p.k['key'] == "esquerda"):
					p.dist.set(near_pos(p.pos.get(), 1))
					p.k['diagonal'] = True
				elif(p.k['key'] == "direita"):
					p.dist.set(near_pos(p.pos.get(), 2))
					p.k['diagonal'] = True

			elif e.key == p.k['baixo']:
				if(p.k['key'] == "baixo"):
					p.k['key'] = None
				elif(p.k['key'] == "esquerda"):
					p.dist.set(near_pos(p.pos.get(), 5))
					p.k['diagonal'] = True
				elif(p.k['key'] == "direita"):
					p.dist.set(near_pos(p.pos.get(), 4))
					p.k['diagonal'] = True

			if e.key == p.k['active']:
				p.active = True
