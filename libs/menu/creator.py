# -*- coding: utf-8 -*-
import pygame
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


#This loader returns filename when json loading failed
def load_json(json_file):
	with open(json_file) as conf_file:
		try:
			json_data = json.load(conf_file)
		except ValueError:
			raise ValueError("JSON loading error: " + json_file)
	return json_data


class create_menu():

	def __init__(self, filename, ref, ref_updater):

		self.data_file = filename
		self.reference = ref

		#load variables and dependencies
		self.variables = self.load_vars(self.data_file)

		#merge all types into list
		self.merged_variables = {}
		for variable in list(self.variables.values()):
			self.merged_variables.update(variable)

		#add custom runtime variables
		self.ref_updater = ref_updater
		self.merged_variables.update(self.ref_updater())

		self.load_objects()

	def load_vars(self, filename, imported_files=[]):

		def add_key(key, dictionary, datatype):
			if key not in dictionary:
				dictionary[key] = datatype()

		self.menu_data = load_json(self.data_file)

		add_key("variables", self.menu_data, dict)
		add_key("lists", self.menu_data["variables"], dict)
		add_key("strings", self.menu_data["variables"], dict)
		add_key("floats", self.menu_data["variables"], dict)
		add_key("images", self.menu_data["variables"], dict)
		add_key("imports", self.menu_data, list)
		add_key("objects", self.menu_data, dict)
		add_key("sliders", self.menu_data["objects"], list)
		add_key("buttons", self.menu_data["objects"], list)
		add_key("titles", self.menu_data["objects"], list)
		add_key("images", self.menu_data["objects"], list)

		#resolve imports
		imports = {}
		imported_files.append(self.data_file)
		for import_file in self.menu_data["imports"]:
			#prevent looping imports
			if import_file in imported_files:
				continue
			else:
				imported_files.append(import_file)
			#merge new vairables
			imports.update(self.load_vars(import_file, imported_files=imported_files))
		self.menu_data["variables"].update(imports)

		exit()
		return self.menu_data["variables"]

	def load_objects(self):
		self.object_data = self.menu_data["objects"]

		def get_data(data_in, expect_type):

			def type_mismatch():
				error = (self.data_file[self.data_file.rfind("/") + 1:]
					+ ": "
					#+ var_name
					+ " is not a "
					+ str(expect_type)[7:-2]
					+ "  | "
					+ str(data_in)
					)
				raise ValueError(error)

			if type(data_in) in [str, unicode]:
				#variable definition
				if data_in[0] == "$":
					try:
						data_in = self.merged_variables[data_in[1:]]
					except KeyError:
						raise KeyError(data_in + " is not a variable.")

					if type(data_in) != expect_type:
						type_mismatch()
					return data_in

			elif expect_type in [int, float]:
				try:
					warning = ("Depreceated value storage: "
						#+ var_name
						+ " = \""
						+ data_in
						+ "\"")
					print(warning)
					return float(data_in)
				except ValueError:
					type_mismatch()
			elif type(data_in) == list:
				return [get_data(x, None) for x in data_in]
			else:
				if type(data_in) in [expect_type, None]:
					return data_in
				else:
					type_mismatch()

		#create sliders
		for slider_data in self.object_data["sliders"]:
			name = get_data(slider_data["name"], str)
			default_value = get_data(slider_data["preset_value"], float)
			options_list = get_data(slider_data["selection_range"], list)
			size = get_data(slider_data["size"], int)
			ratio = get_data(slider_data["width_to_hight_ratio"], float)
			typeface = get_data(slider_data["typeface"], str)
			color = get_data(slider_data["color"], list)
			box = get_data(slider_data["box"], list)
			rel_x = get_data(slider_data["position"]["x_rel"], float)
			rel_y = get_data(slider_data["position"]["y_rel"], float)
			x = get_data(slider_data["position"]["x_abs"], float)
			y = get_data(slider_data["position"]["y_abs"], float)
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
