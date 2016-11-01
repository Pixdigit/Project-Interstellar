# -*- coding: utf-8 -*-
import creator
import pygame


x = int(1920 * 0.5)
res = [x, int(x * 9 / 16.0)]

pygame.init()
screen = pygame.display.set_mode(res)


def ref_updater():
	variables_dict = {}
	variables_dict["fullscreen"] = 1
	variables_dict["volume"] = 0.5
	variables_dict["button_size"] = 0.5
	return variables_dict

menu = creator.create_menu("./assets/templates/settings.json",
			pygame.Rect((0, 0), res),
			ref_updater)

for a in range(2000):
	screen.fill((0, 0, 0))
	events = pygame.event.get()
	menu.blit(screen, events)
	pygame.display.flip()
