# -*- coding: utf-8 -*-
from . import settings
from . import menu
import pygame
import math


def init():
	settings.time("start")


def handle():
	target_shooting()
	player_hit_by_explosion()


def target_shooting():

	alltargets = 0
	for world in settings.localmap:
		alltargets += len(settings.localmap[world].targets)

	if alltargets == 0:
		from . import draw
		from . import movement

		while len(settings.explosions_disp) != 0:
			draw.ingame()
			movement.handle()

		screen = settings.screen

		fade = pygame.Surface((settings.screenx_current, settings.screeny_current))
		fade.fill((0, 0, 0))
		fade.set_alpha(0)
		fade_pos = fade.get_rect()

		font = pygame.font.SysFont(settings.typeface, 50)

		points = settings.time("get_time")
		color = settings.color
		texttime = font.render("Your time: " + str(points) + "ms", True, color)
		tmp = str(points / (settings.dtargets * 8.0))[:6]
		texttt = font.render("You needed " + tmp + "ms per target", True, color)
		textrect = texttime.get_rect()
		textrectpertarget = texttt.get_rect()
		textrect.center = settings.screen.get_rect().center
		textrectpertarget.center = textrect.center
		textrectpertarget.top += 40

		while settings.run:
			settings.upd("get_events")

			for event in settings.events:
				if event.type == pygame.QUIT:
					settings.quit()
				if event.type == pygame.KEYDOWN:
					key = pygame.key.name(event.key)
					if key == "escape" or key == "return":
						settings.run = False
						settings.reset()

			screen.blit(fade, fade_pos)
			screen.blit(texttime, textrect)
			screen.blit(texttt, textrectpertarget)
			pygame.display.flip()


def player_hit_by_explosion():

	# need to be globals so it is are preserved everytime this is called
	global running

	for explosion in settings.explosions_disp:
		distance = math.sqrt(
				(explosion.pos.centerx - settings.player.pos.centerx) ** 2
				+ (explosion.pos.centery - settings.player.pos.centery) ** 2)

		if distance <= 20 and (not ("running" in globals())):
			running = "Wow this variable exists"
			settings.player.explode()
	if settings.player.explosion_anim is not None:
		if (settings.player.explosion_anim.state in ["paused", "stopped"]
			or settings.player.explosion_anim.isFinished()):
				play_failed_sequence()


def play_failed_sequence():

	menu.game_over()