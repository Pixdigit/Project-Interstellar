# -*- coding: utf-8 -*-
import creator
import pygame

pygame.init()
screen = pygame.display.set_mode((1, 1))

menu_creator = creator.create_menu("../../assets/templates/settings.json",
			pygame.Rect((0, 0), (1920, 1080)),
			{"fullscreen": 1, "volume": 0.5, "button_size": 0.5})