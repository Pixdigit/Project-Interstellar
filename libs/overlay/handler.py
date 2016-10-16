# -*- coding: utf-8 -*-


class create_overlay_handler():
	"""A mother-class for in-game overlays.

	init(self) inits the module
	add_element(self, overlay_obj, overwrite=False) adds an overlay element
	hide(self, elements=None) hides elements"""

	def __init__(self):
		self.objects = []
		self.objs_on_screen = set()

	def get_by_name(self, elem_name):
		for elem in self.objects:
			if elem.name == elem_name:
				return elem
		return None

	def add_element(self, overlay_obj, overwrite=False):
		"""Adds an overlay element to the handler.

		overwrite determines that if an object with the name already
		exists if it should be overwritten
		whereas the object must be a subclass of overlay_element_base_class
		"""

		if (overlay_obj.name not in self.objects) or overwrite:
			overlay_obj.deactivate()
			self.objects[overlay_obj.name] = overlay_obj

	def unhide(self, elements=None):
		"""Unhides elements.
		When called with no arguments, all elements get shown.
		Can also be called with name or a list with names.
		"""

		if elements is None:
			for object_name in self.objects:
				self.objects[object_name].activate()
		else:
			if type(elements) != list:
				elements = list(elements)
			for element_name in elements:
				self.objects[element_name].activate()

	def hide(self, elements=None):
		"""Hides elements.
		When called with no arguments, all elements get hidden.
		Can also be called with name or a list with names.
		"""

		if elements is None:
			for object_name in self.objects:
				self.objects[object_name].deactivate()
		else:
			if type(elements) != list:
				elements = list(elements)
			for element_name in elements:
				self.objects[element_name].deactivate()

	def blit(self, screen):
		for obj in list(self.objects.values()):
			obj.blit(screen)