# -*- coding: utf-8 -*-
from . import objects
from . import settings


def init():
	global angle
	global amount
	global direction
	global fire
	global energy
	angle = 0
	amount = 1
	direction = "Clock"
	energy = 0
	fire = False


def update():
	global angle
	global amount
	global direction
	global fire
	global energy

	#TODO:find alternative to disabling lint
	#lint:disable
	if energy < 100:
		energy += 1
	if energy == 100 and fire:
		energy = 0
		fire = False
		for tmpangle in range(8):
			tmpangle *= 45
			tmp = objects.bullet(tmpangle, settings.player.pos)
			settings.bullets.append(tmp)

	# shoots in 8 direction and the one youre looking constantly
	if settings.psycomode:
		tmp = objects.bullet(settings.player.rotation, settings.player.pos)
		settings.bullets.append(tmp)
		for tmpangle in range(8):
			tmpangle *= 45
			tmp = objects.bullet(tmpangle, settings.player.pos)
			settings.bullets.append(tmp)

	if len(settings.morevents) > 0:
		for event in settings.morevents:
			if event == "Circle":
				for tmpangle in range(359):
					tmp = objects.bullet(tmpangle, settings.player.pos)
					settings.bullets.append(tmp)
			if event == "Add":
				if amount < 20:
					amount += 1
				else:
					amount = 0
			if event == "Remove":
				if amount > 0:
					amount -= 1
			if event == "Changedir":
				direction = settings.toggle(direction, "Clock", "Anti")
			settings.morevents.remove(event)

	if settings.infinitevents["fire1"]:
		tm = objects.bullet(settings.player.rotation, settings.player.pos)
		settings.bullets.append(tm)

	if settings.infinitevents["roundfire"]:
		if 0 < amount < 20:
			angle += 6
			if angle >= 360:
				angle -= 360
			diffangle = 360.0 / amount
			for a in range(amount):
				tmp_an = angle
				if direction != "Clock":
					tmp_an = 360 - tmp_an
				tmp = objects.bullet(a * diffangle + tmp_an, settings.player.pos)
				settings.bullets.append(tmp)
	#lint:enable
