# -*- coding: utf-8 -*-
import pygame
import json
import disp_elem
from pprint import pprint


def convert2list(string):
	num_of_elem = string.count(",") + 1
	elements = []
	string = string[1:]
	for a in range(num_of_elem - 1):
		elements.append(string[:string.index(",")].strip())
		string = string[string.index(",") + 1:].strip()
	elements.append(string[:-1])
	return elements


datatypes = ["strings",
	"floats",
	"lists",
	"colors",
	"box_designs"]


#This loader returns filename when json loading failed
def load_json(json_file):
	with open(json_file) as conf_file:
		try:
			json_data = json.load(conf_file)
		except ValueError:
			raise ValueError("JSON loading error: " + json_file)
	return json_data


def add_key(key, dictionary, datatype):
	if key not in dictionary:
		dictionary[key] = datatype()
	return dictionary


def merge(iter1, iter2):
	"""Recursive merging of iter1 and iter2. Items in iter1 will be preserved"""

	if type(iter1) != type(iter2):
		raise ValueError("Cannot merge different iterables.")

	if type(iter1) == list:
		return list(set(iter1 + iter2))

	if type(iter1) == dict:
		for new_key in iter2:
			new_value = iter2[new_key]

			if type(new_value) not in [dict, list]:
				if new_key not in iter1:
					iter1[new_key] = new_value
			else:
				if new_key not in iter1:
					iter1[new_key] = iter2[new_key]
				else:
					iter1[new_key] = merge(iter1[new_key], iter2[new_key])

	return iter1


def load_vars(filename, pre_imports=[]):

	menu_data = load_json(filename)

	#add keys if not existing
	menu_data = add_key("variables", menu_data, dict)
	menu_data = add_key("imports", menu_data, list)
	variables = menu_data["variables"]
	variables = add_key("lists", variables, dict)
	variables = add_key("strings", variables, dict)
	variables = add_key("floats", variables, dict)
	variables = add_key("images", variables, dict)

	#resolve imports
	imports = {datatype: {} for datatype in datatypes}
	pre_imports.append(filename)
	for import_file in menu_data["imports"]:
		#prevent looping imports
		if import_file in pre_imports:
			continue
		else:
			#merge new vairables
			imports = merge(imports, load_vars(import_file, pre_imports=pre_imports))

	variables = merge(variables, imports)

	return variables


class create_menu():

	def __init__(self, filename, ref, ref_updater):

		self.data_file = filename
		self.reference = ref
		self.menu_data = load_json(filename)

		#load variables and dependencies
		self.variables = load_vars(self.data_file)

		#merge all types into list
		self.merged_variables = {}
		for variable in list(self.variables.values()):
			self.merged_variables.update(variable)

		#add custom runtime variables
		self.ref_updater = ref_updater
		self.merged_variables.update(self.ref_updater())

		self.load_objects()

	def load_objects(self):

		add_key("objects", self.menu_data, dict)
		add_key("sliders", self.menu_data["objects"], list)
		add_key("buttons", self.menu_data["objects"], list)
		add_key("titles", self.menu_data["objects"], list)
		add_key("images", self.menu_data["objects"], list)

		self.object_data = self.menu_data["objects"]

		def get_data(data_dict, key_name, expect_type=None):

			def type_mismatch(expect_type):
				if expect_type is None:
					expect_type = "<type \"NoneType\">"
				error = (self.data_file[self.data_file.rfind("/") + 1:]
					+ ": "
					+ key_name
					+ " should be an: "
					+ str(expect_type)[7:-2]
					+ " | Got an: "
					+ str(type(data_in))[7:-2]
					+ " == "
					+ str(data_in)
					)
				raise ValueError(error)

			try:
				data_in = data_dict[key_name]
			except KeyError:
				if not "name" in data_dict:
					data_dict["name"] = "NONAME"
				error = (key_name
					+ "is not a property of: "
					+ data_dict["name"]
					)
				raise KeyError(error)

			if (type(data_in) in [str, unicode]) and data_in[0] == "$":
				try:
					data_in = self.merged_variables[data_in[1:]]
				except KeyError:
					raise KeyError(data_in + " is not a variable.")
				return data_in

			if expect_type in [str, unicode]:
				#variable definition
				return str(data_in)
			elif expect_type in [int, float]:
				try:
					if type(data_in) in [str, unicode]:
						if data_in[0] == "%":
							try:
								return float(data_in[1:]) / 100
							except ValueError:
								type_mismatch(float)
						warning = ("Depreceated value storage: "
							+ " = \""
							+ str(data_in)
							+ "\"")
						print(warning)
					return float(data_in)
				except ValueError:
					type_mismatch(expect_type)
			elif type(data_in) == list:
				new_list = [get_data(data_in, x, None) for x in range(len(data_in))]
				return new_list
			else:
				if type(data_in) == expect_type or expect_type is None:
					return data_in
				else:
					type_mismatch(expect_type)

		#create sliders
		for slider_data in self.object_data["sliders"]:
			name = get_data(slider_data, "name", str)
			default_value = get_data(slider_data, "preset_value", float)
			options_list = get_data(slider_data, "selection_range", list)
			size = get_data(slider_data, "size", int)
			ratio = get_data(slider_data, "width_to_hight_ratio", float)
			typeface = get_data(slider_data, "typeface", str)
			color = get_data(slider_data, "color", list)
			box = get_data(slider_data, "box", list)
			rel_x = get_data(slider_data["position"], "x_rel", float)
			rel_y = get_data(slider_data["position"], "y_rel", float)
			x = get_data(slider_data["position"], "x_abs", float)
			y = get_data(slider_data["position"], "y_abs", float)

			disp_elem.slider(name, default_value, options_list, size, ratio, typeface,
					color, box, rel_x, x, rel_y, y, self.reference)

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
