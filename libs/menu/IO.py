# -*- coding: utf-8 -*-
"""A module for overwriting variabels."""
import json


def write(filename, variable, value):
	return
	with open(filename, "r+") as conf_file:
		for line in conf_file:
			last = line
		if last.strip():
			conf_file.write("\n")
	lines = []
	with open(filename, "r+") as conf_file:
		for line in conf_file:
			if line.strip():
				if line.strip()[0] == "<":
					ident = line.index("<")
					varname = (line[ident + 2:line.index("=") - 1]).strip()
					if varname == variable:
						line = line[:line.index("=") + 1]
						line = line + " " + str(value) + "\n"
			lines.append(line)
	conf_file.close()
	with open(filename, "w") as conf_file:
		conf_file.writelines(lines)


def read(filename, variable):
	with open(filename, "r+") as conf_file:
		data = json.load(conf_file)
	for data_type in data:
		for var_name in data_type:
			if var_name == variable:
				return data_type[var_name]
