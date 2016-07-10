# -*- coding: utf-8 -*-
import pygame
import disp_elem
import json


def convert2list(string):
	num_of_elem = string.count(",") + 1
	elements = []
	string = string[1:]
	for a in range(num_of_elem - 1):
		elements.append(string[:string.index(",")].strip())
		string = string[string.index(",") + 1:].strip()
	elements.append(string[:-1])
	return elements


def analyse_num(string, variables):
	string = string.strip()
	lstring = string[:string.index("+")].rstrip()
	rstring = string[string.index("+") + 1:].lstrip()
	if lstring[0] == "%":
		rel = int(lstring[1:]) / 100.0
	elif lstring[0] == "$":
		if variables[lstring[1:]] < 1.0001 and type(variables[lstring[1:]]) == float:
			rel = variables[lstring[1:]]
		else:
			absol = variables[lstring[1:]]
	else:
		absol = int(lstring)

	if rstring[0] == "%":
		rel = int(rstring[1:]) / 100.0
	elif rstring[0] == "$":
		if variables[rstring[1:]] < 1.0001 and type(variables[rstring[1:]]) == float:
			rel = variables[rstring[1:]]
		else:
			absol = variables[rstring[1:]]
	else:
		absol = int(rstring)

	return rel, absol


class create_menu():

	def __init__(self, filename, ref, additional_variables={}):

		#load variables and dependencies
		self.variables = self.load_vars(filename)

		#merge all types into list
		merged_variables = {}
		for variable in self.variables.values():
			merged_variables.update(variable)

		#add custom variables at runtime
		self.variables.update(additional_variables)
		print merged_variables

	def load_vars(self, filename):

		#load json file
		with open(filename) as conf_file:
			menu_conf = json.load(conf_file)

		#resolve imports
		imports = {}
		imported_files = [filename]
		if "imports" in menu_conf:
			for import_file in menu_conf["imports"]:
				#prevent looping imports
				if import_file in imported_files:
					continue
				else:
					imported_files.append(import_file)
				imported_files.append(import_file)
				imports.update(self.load_vars(import_file))
		menu_conf["variables"].update(imports)

		return menu_conf["variables"]

	def blit(self, screen, events):
		try:
			screen.blit(self.elems["surfs"]["background"][0],
				self.elems["surfs"]["background"][1])
		except:
			pass
		try:
			for external in self.elems["externals"]:
				external.blit(screen)
		except:
			pass
		for surf in self.elems["surfs"]:
			if surf != "background":
				screen.blit(self.elems["surfs"][surf][0], self.elems["surfs"][surf][1])
		for elem in self.elems["buttons"] + self.elems["sliders"]:
			elem.update(events)
			elem.blit(screen)

	def get_klicked(self):
		klicked = []
		for elem in self.elems["buttons"]:
			if elem.klicked:
				klicked.append(elem)
		return klicked

	def get_elem(self, name):
		for key in self.elems:
			for elem in self.elems[key]:
				if type(elem) != pygame.Surface:
					if elem.name == name:
						return elem
