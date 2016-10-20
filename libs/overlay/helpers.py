# -*- coding: utf-8 -*-
import random


global used_id_list
used_id_list = []


def get_unique_id():
	global used_id_list

	found_id = False
	while not found_id:
		new_id = random.random()
		found_id = new_id not in used_id_list
	return new_id
