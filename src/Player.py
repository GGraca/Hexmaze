import pygame, sys
from pygame.locals import *
from Globals import * 
from random import *
from Funcoes import *

def set_players(n):
	players = []
	if(n >= 1):
		players.append(Player(GREEN, 1))
	if(n >= 2):
		players.append(Player(RED, 2))

	return players

class Player(pygame.sprite.Sprite):

	def __init__(self, spawn, p_id):
		self.p_id = p_id
		self.color = (255,0,0) 		#cor do jogador # para tirar quando houver imagem
		self.size = 10 			#tamanho do jogador # mudar de acordo com o ecra
		self.k = {}				#keyboard input
		
		self.spawn_pos = spawn
		self.pos = None	#pos xy dentro da matriz
		self.dist = None		#pos que e' atribuida ao jogador
		self.last_pos = xy(0,0)	#pos anterior (usada para player_off())
		
		self.image = None		#sprite do objecto
		self.rect = None		#propriedades do tamanho do sprite
		self.active = False

		pygame.sprite.Sprite.__init__(self)
		self.set_sprite()
		self.spawn()
		self.set_keys()

	def set_sprite(self):
		self.image = pygame.Surface((self.size * 2, self.size * 2))
		#self.image.set_colorkey(TRCOLOR)
		self.image.fill(TRCOLOR)
		
		pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size, 0)
		self.rect = self.image.get_rect()

	def set_keys(self):
		f = open("Controls.txt", 'r')
		temp = f.readline()
		if(self.p_id == 1):
			pass
		else:
			for i in range(7):
				temp = f.readline()

		self.k.update({'cima': f.readline().translate(None, '\n')})
		self.k.update({'baixo': f.readline().translate(None, '\n')})
		self.k.update({'esquerda': f.readline().translate(None, '\n')})
		self.k.update({'direita': f.readline().translate(None, '\n')})
		self.k.update({'active': f.readline().translate(None, '\n')})

		f.close()


	def paint(self, surface):
		allsprites = pygame.sprite.RenderPlain((self))
		allsprites.draw(surface)

	def spawn(self):
		self.k.update({'key': None, 'diagonal': None})

		self.pos = xy(-1,-1)
		self.dist = xy(self.spawn_pos[0], self.spawn_pos[1])

	def update(self, matrix):
		self.last_pos.set(self.pos.get())
		#print self.pos.get()
		self.mov(matrix)

		#self.rect.center = pygame.mouse.get_pos()
	def mov(self, matrix):
		if(self.dist.get() != self.pos.get()):
			if(self.dist.get() in matrix.blocked):
				self.dist.set(self.pos.get())
			else:
				a, b = self.dist.get()
				c = (matrix.objs[b][a].pos.x , matrix.objs[b][a].pos.y )
				self.rect.center = c
				self.pos.set(self.dist.get())