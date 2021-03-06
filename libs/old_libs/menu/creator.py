# -*- coding: utf-8 -*-
import pygame
import json
import disp_elem


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

	with open(filename)as data_file:
		menu_data = json.load(data_file)

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
		self.menu_data = load_json(self.data_file)

		#load variables and dependencies
		#I dont know why the emtpy list. But it stops it from using the list
			#from the menu before
		self.variables = load_vars(self.data_file, [])

		#merge all types into list
		#and add std vars
		number_corrector = lambda float_var: (
						str(float_var * 100)[:str(float_var * 100).find(".")] + "%")
		floats_list = [number_corrector((x + 1) / 255.0) for x in range(255)]
		self.merged_variables = {"floats": floats_list}
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
		self.objects = []

		def get_data(data_dict, key_name, expect_type=None):

			def type_mismatch(expect_type):
				if expect_type is None:
					expect_type = "<type \"NoneType\">"
				error = (self.data_file[self.data_file.rfind("/") + 1:]
					+ ": "
					+ str(key_name)
					+ " should be an: "
					+ str(expect_type)[7:-2]
					+ " | Got an: "
					+ str(type(data_in))[7:-2]
					+ " == "
					+ str(data_in)
					)
				raise ValueError(error)

			#Try to load value
			try:
				data_in = data_dict[key_name]
			except KeyError:
				#Not in dict -> Raise error
				if not "name" in data_dict:
					data_dict["name"] = "NONAME"
				error = (str(key_name)
					+ " is not a property of: "
					+ data_dict["name"]
					)
				raise KeyError(error)

			#Got a vairable
			if (type(data_in) in [str, unicode]) and data_in[0] == "$":
				#Try to load variable
				try:
						data_in = get_data(self.merged_variables, data_in[1:])
				except KeyError:
					print ""
					raise KeyError(data_in + " is not a variable.")
				return data_in

			#If we expect a string anything goes
			if expect_type in [str, unicode]:
				return str(data_in)
			#If we expect int Try resolving percentages
			elif expect_type in [int, float]:
				try:
					if type(data_in) in [str, unicode]:
						if data_in[0] == "%":
							try:
								return float(data_in[1:]) / 100
							except ValueError:
								type_mismatch(float)
						else:
							return float(data_in)
					else:
						try:
							return float(data_in)
						except TypeError:
							type_mismatch()
				except ValueError:
					type_mismatch(expect_type)
			#If we got a list recursively resolve
			elif type(data_in) == list:
				new_list = []
				for item in data_in:
					#merge if element is list
					if type(item) in [str, unicode] and item[0] == "$":
						if type(self.merged_variables[item[1:]]) == list:
							new_list = new_list + get_data(data_in, data_in.index(item), None)
					else:
						new_list.append(get_data(data_in, data_in.index(item), None))
				return new_list
			#If we got a dict recursively resovle that
			elif type(data_in) == dict:
				new_data = {}
				for key in data_in:
					new_data[key] = get_data(data_in, key)
				return new_data
			#If input is int there is not much else to return
			elif type(data_in) in [int, float]:
				return float(data_in)
			#If no expection is given try float first then usual value
			elif expect_type is None:
				try:
					return get_data(data_dict, key_name, float)
				except ValueError:
					return data_in
			else:
				#If nothing else works return blank input
				if type(data_in) == expect_type or expect_type is None:
					return data_in
				else:
					type_mismatch(expect_type)
			raise RuntimeError("I have no idea how this happend! : "
					+ str(data_in) + " | " + str(expect_type))

		#create titles
		for title_data in self.object_data["titles"]:
			name = get_data(title_data, "name", str)
			label = get_data(title_data, "label", str)
			typeface = get_data(title_data, "typeface", str)
			size = get_data(title_data, "size", int)
			color = get_data(title_data, "color", list)
			bold = get_data(title_data, "bold", bool)
			italics = get_data(title_data, "italics", bool)
			pos_data = get_data(title_data, "position", dict)

			self.objects.append(disp_elem.text(name, label, typeface, size, color,
					bold, italics, pos_data))

		#create buttons
		for button_data in self.object_data["buttons"]:
			name = get_data(button_data, "name", str)
			label = get_data(button_data, "label", str)
			typeface = get_data(button_data, "typeface", str)
			size = get_data(button_data, "size", int)
			color = get_data(button_data, "color", list)
			box = get_data(button_data, "box", list)
			ratio = get_data(button_data, "width_to_hight_ratio", float)
			pos_data = get_data(button_data, "position", dict)

			self.objects.append(disp_elem.button(name, label, typeface, color, size,
					ratio, box, pos_data))

		#create sliders
		for slider_data in self.object_data["sliders"]:
			name = get_data(slider_data, "name", str)
			label = get_data(slider_data, "label", str)
			typeface = get_data(slider_data, "typeface", str)
			size = get_data(slider_data, "size", int)
			color = get_data(slider_data, "color", list)
			options_list = get_data(slider_data, "selection_range", list)
			default_value = get_data(slider_data, "preset_value", float)
			box = get_data(slider_data, "box", list)
			ratio = get_data(slider_data, "width_to_hight_ratio", float)
			pos_data = get_data(slider_data, "position", dict)
			self.objects.append(disp_elem.slider(name, label, typeface, color, size,
					ratio, options_list, default_value, box, pos_data))

		self.objects.insert(0, self.reference)
		for obj in self.objects[1:]:
			obj.get_rel_pos(self.objects)

	def blit(self, screen, events):
		#screen.blit(self.objects[0])
		for obj in self.objects[1:]:
			obj.update(events)
			obj.blit(screen)

	def get_klicked(self):
		klicked = []
		for obj in self.objects[1:]:
			if obj.type == "button":
				if obj.klicked:
					klicked.append(obj)
		return klicked

	def get_types(self, obj_type):
		obj_list = []
		for obj in self.objects[1:]:
			if obj.type == obj_type:
				obj_list.append(obj)
		return obj_list

	def get_obj(self, name):
		for obj in self.objects[1:]:
			if obj.name == name:
				return obj
