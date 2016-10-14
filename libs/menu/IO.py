# -*- coding: utf-8 -*-
"""A module for overwriting variabels."""
import json


def write(filename, variable_name, value):
	with open(filename, "r") as conf_file:
		conf = json.load(conf_file)

	if not "variables" in conf:
		conf["variables"] = {}

	conf["variables"][variable_name] = value

	with open(filename, "w") as conf_file:
		json.dump(conf, conf_file, indent=12, sort_keys=True)


def read(filename, variable_name):
	with open(filename, "r+") as conf_file:
		data = json.load(conf_file)

	if "variables" not in data:
		data["variables"] = []

	return data["variables"][variable_name]
