from . import settings
from . import objects
from . import draw
import pygame
"""An abstact level for handeling multiple worlds."""


class world():

	def __init__(self, name):
		self.name = name

	def generate(self, background, dstars, dtargets):
		# initialize a new "world"

		# load background image
		self.background = background
		self.background_pos = self.background.get_rect()
		# set background position
		self.background_pos.left = int(-(settings.player.rel_x * (
			settings.screenx_current * (settings.fake_size - 1))))
		self.background_pos.top = int(-(settings.player.rel_y * (
			settings.screeny_current * (settings.fake_size - 1))))

		# create targets and stars
		self.stars = []
		self.targets = []
		for counter in range(dstars):
			tmpstar = objects.stars()
			self.stars.append(tmpstar)
		for counter in range(dtargets):
			tmptarget = objects.target()
			self.targets.append(tmptarget)

		self.warp1 = objects.warp_station()

		self.adjust_to_screen()

	def move(self):
		"""Move everything in the world."""
		player_pos = settings.player.pos

		self.background_pos.left = int(-(settings.player.rel_x * (
			settings.screenx_current * (settings.fake_size - 1))))
		self.background_pos.top = int(-(settings.player.rel_y * (
			settings.screeny_current * (settings.fake_size - 1))))

		self.warp1.move(player_pos)
		self.warp1.test(player_pos)

		for star in self.stars:
			star.move(player_pos.left, player_pos.top)

		for bullet in settings.bullets:
			bullet.move(player_pos)
			if not bullet.pos.colliderect(self.background_pos):
				settings.bullets.remove(bullet)

		for target in self.targets:
			target.move(player_pos.left, player_pos.top)
			for bullet in settings.bullets:
				target.test_ishit(bullet.pos)
			if target.gothit:
				self.targets.remove(target)
				#TODO: move from settings to here
				settings.explosions_disp.append(target)
				settings.explosions_disp = list(set(settings.explosions_disp))

		for explosion in settings.explosions_disp:
			if explosion.kill_entity:
				settings.explosions_disp.remove(explosion)
				pass
			else:
				explosion.move(player_pos.left, player_pos.top)

	def blit(self):
		"""Blit everything in the world."""

		# blit background
		settings.screen.blit(self.background, self.background_pos)

		# Blit all objects
		settings.objects_on_screen = 0
		for star in self.stars:
			isdisplayed = star.blitstar()
			if isdisplayed:
				settings.objects_on_screen += 1
		for bullet in settings.bullets:
			isdisplayed = bullet.blit()
			if isdisplayed:
				settings.objects_on_screen += 1
		for target in self.targets:
			isdisplayed = target.blit()
			if isdisplayed:
				settings.objects_on_screen += 1
		for explosion in settings.explosions_disp:
			explosion.blit()
		self.warp1.blit()

	def adjust_to_screen(self):

		tmpx = settings.screenx_current * settings.fake_size
		tmpy = settings.screeny_current * settings.fake_size
		screen_current = (int(tmpx), int(tmpy))
		background = pygame.image.load("./assets/sprites/Background2.tif").convert()
		self.background = pygame.transform.smoothscale(background, screen_current)
		self.background_pos = self.background.get_rect()

		tmp = -(settings.player.pos.x * (settings.screenx_current *
					(settings.fake_size - 1)))
		self.background_pos.left = int(tmp)
		tmp = -(settings.player.pos.y * (settings.screeny_current *
					(settings.fake_size - 1)))
		self.background_pos.top = tmp

		draw.no16to9 = False
		if settings.aspect_ratio != 16.0 / 9:
			draw.no16to9 = True
			delta_screeny = (settings.screeny_current
					- (settings.screenx_current * 9.0 / 16))
			draw.correcture = pygame.Surface((settings.screenx_current, delta_screeny)
						).convert_alpha()
			draw.correcture_pos = draw.correcture.fill((0, 0, 0))
			draw.correcture.set_alpha(255)
			draw.correcture_pos.topleft = (0, (settings.screenx_current * 9.0 / 16))

		for star in self.stars:
			star.update(settings.screenx_current / 1920.0)

		for target in self.targets:
			target.update()

		self.warp1.update()
