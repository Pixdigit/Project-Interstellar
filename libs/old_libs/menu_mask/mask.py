# -*- coding: utf-8 -*-


class new_mask():

	def __init__(self):
		self.slots = {}
		self.highest_id = 0
		self.groups = {"general": set()}

	def add_slot(self, slot_pos, group="general", slot_id=None):
		if slot_id is None:
			self.highest_id += 1
			slot_id = self.highest_id
		else:
			found = False
			while not found:
				if not slot_id in list(self.slots.keys()):
					found = True
				else:
					slot_id += 1
			if slot_id > self.highest_id:
				self.highest_id = slot_id

		self.slots[slot_id] = slot_pos
		try:
			self.groups[group].add(slot_id)
		except KeyError as error:
			if group not in self.groups:
				raise NameError("Group \"" + group + "\" does not exist.")
			else:
				raise KeyError(error)

	def add_group(self, group_name, id_set=set([])):
		if type(id_set) == list:
			id_set = set(id_set)
		for slot_id in id_set.copy():
			if slot_id not in self.slots:
				if slot_id >= self.highest_id:
					id_set.remove(slot_id)
				else:
					raise KeyError("Slot can not be added to group: "
							+ str(slot_id) + " does not exist.")
		if group_name in self.groups:
			self.groups[group_name].union(id_set)
		else:
			self.groups[group_name] = id_set
