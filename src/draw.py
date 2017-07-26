# -*- coding: utf-8 -*-
import pygame
import math
from . import settings
from . import sounds
from . import overlay_handler
from pygame.locals import USEREVENT


def init():
	"""Some variable initializing"""
	# nothing to explain here
	global alpha
	global no16to9
	global correcture
	global correcture_pos
	global show

	alpha = 0
	no16to9 = False
	show = 0
	if settings.aspect_ratio != 16.0 / 9:
		# makes a black stripe if not 16 to 9
		no16to9 = True
		delta_screeny = (settings.screeny_current
				- (settings.screenx_current * 9.0 / 16))
		correcture = pygame.Surface((settings.screenx_current, delta_screeny)
										).convert_alpha()
		correcture_pos = correcture.fill((0, 0, 0))
		correcture.set_alpha(255)
		correcture_pos.topleft = (0, (settings.screenx_current * 9.0 / 16))
	else:
		correcture_pos = pygame.Rect(0, settings.screeny_current, 0, 0)


def ingame():
	"""Draws everything while game runs"""
	# nothing to explain here i guess

	settings.world.blit()

	settings.player.blit(settings.screen)
	if settings.debugscreen:
		debug()
	drawsongname()
	drawtargetsum()
	drawworldname()
	overlay_handler.blit()

	if no16to9:
		settings.screen.blit(correcture, correcture_pos)

	pygame.display.flip()


def debug():
	"""shows debug info on screen"""
	# nothing to explain here too?

	rot_dest = settings.player.rot_dest
	rotation = settings.player.rotation
	font = settings.stdfont
	player_pos = settings.player.pos
	screen = settings.screen
	speed = settings.player.speed
	move = settings.player.should_move
	move_x = settings.player.move_x * speed
	move_y = settings.player.move_y * speed
	pos_x = settings.player.rel_x
	pos_y = settings.player.rel_y
	clock = settings.clock
	objects_on_screen = settings.objects_on_screen
	color = settings.color

	if pos_x >= 0.9 and pos_y >= 0.9:
		isnear = "True"
	else:
		isnear = "False"

	rot = str(rot_dest) + ", " + str(rotation) + ")"
	speed = "(" + str(round(move_x, 3)) + ", " + str(round(move_y, 3)) + ")"
	pos = ("(" + str(pos_x) + ", " + str(pos_y) + ")")
	fps = str(math.floor(clock.get_fps()))
	time = "time scince start: " + str(settings.time("get_time"))
	pixpos = "(" + str(player_pos.left) + ", " + str(player_pos.top) + ")"
	entitys = "Entitys: " + str(objects_on_screen)

	texttime = font.render(time, True, color)
	textfps = font.render("fps: " + fps, True, color)
	textxy = font.render("(x%, y%): " + pos, True, color)
	textpixpos = font.render("(x, y): " + pixpos, True, color)
	textrot = font.render("(destination, current): (" + rot, True, color)
	textspeed = font.render("(speedx, speedy): " + speed, True, color)
	isnear = font.render("Inzone: " + isnear, True, color)
	textdoesmove = font.render("move?: " + str(move), True, color)
	textentitys = font.render(entitys, True, color)

	screen.blit(textfps, (0, 0))
	screen.blit(textxy, (0, 20))
	screen.blit(textpixpos, (0, 40))
	screen.blit(textrot, (0, 60))
	screen.blit(textspeed, (0, 80))
	screen.blit(isnear, (0, 100))
	screen.blit(textdoesmove, (0, 120))
	screen.blit(texttime, (0, 140))
	screen.blit(textentitys, (0, 160))


def drawtargetsum():

	textlocaltargets = (str(len(settings.world.targets))
			+ " / "
			+ str(settings.dtargets))
	text1surf = settings.stdfont.render(textlocaltargets, 1, settings.color)
	text1rect = text1surf.get_rect()
	text1rect.right = settings.screenx_current
	text1rect.top = 40

	alltargets = 0
	for world in settings.localmap:
		alltargets += len(settings.localmap[world].targets)

	textglobaltargets = str(alltargets) + " / " + str(settings.dtargets * 8)
	text2surf = settings.stdfont.render(textglobaltargets, 1, settings.color)
	text2rect = text2surf.get_rect()
	text2rect.right = settings.screenx_current
	text2rect.top = 60
	settings.screen.blit(text1surf, text1rect)
	settings.screen.blit(text2surf, text2rect)


def drawsongname():
	"""shows the songname if new song is played"""
	global show
	global songname
	global font_pos
	global alpha

	screenx = settings.screenx_current
	screen = settings.screen
	typeface = settings.typeface

	for event in settings.events:
		if pygame.mixer.music.get_pos() < 4000 and sounds.music.volume != 0:
			show = 40 * 8
			font = pygame.font.SysFont(typeface, 15)
			song = sounds.music.playlist[0].replace("_", " ")[:-4]
			# To all of you:
			# USE BACKGROUND COLOR
			# cant apply alpha otherwise (took hours to figure out)
			songname = font.render(song, True, settings.color, (0, 0, 5))
			font_pos = songname.get_rect()
			font_pos.right = screenx - 10
			font_pos.top = 10
			alpha = 255
		if event.type == USEREVENT + 1 and sounds.music.volume != 0:
			show -= 1 if show > 0 else False
			if show <= 40 * 4 and alpha > 0:
				alpha -= 1.6
			try:
				songname.set_alpha(int(alpha))
			except Exception:
				pass
				# Timing error is not important

	if pygame.mixer.music.get_volume() != 0.0 and show != 0:
		screen.blit(songname, font_pos)


def drawworldname():
			font = pygame.font.SysFont(settings.typeface, 50)
			name = font.render("World: " + str(settings.world.name),
					True, settings.color)
			pos = name.get_rect()
			pos.centerx = settings.screenx_current / 2
			settings.screen.blit(name, pos)
