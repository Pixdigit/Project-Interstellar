# -*- coding: utf-8 -*-
import creator
import pygame

pygame.init()
screen = pygame.display.set_mode((1, 1))


def ref_updater():
	variables_dict = {}
	variables_dict["fullscreen"] = 1
	variables_dict["volume"] = 0.5
	variables_dict["button_size"] = 0.5
	return variables_dict

menu_creator = creator.create_menu("../../assets/templates/settings.json",
			pygame.Rect((0, 0), (1920, 1080)),
			ref_updater)