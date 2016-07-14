# -*- coding: utf-8 -*-
import os
import json
import shutil

print(("Welcome to the Item creator setup!"))
print((""))
print(("Please enter following data to create a new Item:"))

entered_correct_data = False
while not entered_correct_data:
	try:
		name = raw_input("\nName of the Item: ")
	except KeyboardInterrupt:
		entered_correct_data = True
		continue

	if name == "":
		exit()
	elif os.path.isdir("./" + name):
		print(("\nAn item with the same name already exists."))
		print(("Please enter a new name or leave line blank if you want to abort."))
		print(("If you however want to overwrite it press ctrl + c"))
	else:
		os.mkdir("./" + name)
		init_file = open("./" + name + "/__init__.py", "w+")
		init_complete = "# -*- coding: utf-8 -*-\nfrom . import item"
		init_file.write(init_complete)
		if not os.path.exists("./" + name + "/item.py"):
			shutil.copy("./item_template.py", "./" + name + "/item.py")
		entered_correct_data = True

path = os.path.abspath("./") + "/" + name + "/"
image_path = path + "images/"

print(("\nPlease copy now the required images in the newly created folder."))
raw_input("Press enter to run a check if every file is present.")

test_finished = False
while not test_finished:

	if not os.path.exists(image_path):
		os.makedirs(image_path)
	if os.path.exists(path + "icon.png"):
		shutil.move(path + "icon.png", image_path + "icon.png")

	all_files_present = (
			os.path.isdir(image_path) and
			os.path.isfile(image_path + "icon.png"))

	if not all_files_present:
		print(("\nNot all needed images are present."))
		print(("Please check again, that all images are present."))
		retry = raw_input("Type \"retry\" to test again.\nLeave line empty to abort:")
		if not retry in ["retry", "\"retry\""]:
			exit()
	else:
		test_finished = True


dataset = {"name": name,
	"icon_path": "./images/icon.png",
	"caller": "player",
	"script": "./item.py"}

datafile = open(path + "data.json", "w+")

json.dump(dataset, datafile, indent=12)
