import pygame
TRCOLOR = (239, 58, 10)

class Game_Surfaces:
	def __init__(self, m_size, screen_xy):
		self.world = None
		self.world_pos = None

		self.players = None
		self.players_pos = None

		self.set_all(m_size, screen_xy)



	def set_all(self, m_size, screen_xy):
		self.set_sizes(m_size, screen_xy)
		self.set_surfaces()



	def set_sizes(self, m_size, s):
		x = m_size[0] * 1.0
		y = m_size[1] * 0.916

		self.a = s[0]/ x
		self.i = ((s[0]-(self.a * x))/2, (s[1]-(self.a * y))/2)

		if(y * self.a > s[1]):

			self.a = s[1]/ y
			self.i = ((s[0]-(self.a * x))/2, (s[1]-(self.a * y))/2)

		x = x * self.a
		y = y * self.a
		self.xy = (x, y)

	def set_surfaces(self):
		#World
		self.world = pygame.Surface(self.xy)
		a = self.i
		self.world_pos = a



		self.world.set_colorkey(TRCOLOR)
		self.world = self.world.convert()

		#Players
		self.players = pygame.Surface(self.xy)
		self.players_pos = a
		self.players.set_colorkey(TRCOLOR)
		self.players = self.players.convert()



