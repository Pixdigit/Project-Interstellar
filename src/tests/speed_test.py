import random
from timeit import repeat

class obj():

	def __init__(self, name):
		self.name = name

#fastest
def a(name, objects):
	for elem in objects:
		if elem.name == name:
			return elem
	return None

#slowest
def b(name, objects):
	elms = [obj.name for obj in objects if obj.name == name]
	if len(elms) != 0:
		return elms[0]
	else:
		return None

#slower than a but faster as b if the index of searched item is small
def c(name, objects):
	elms = [obj.name for obj in objects if obj.name == name]
	try:
		return elms[0]
	except IndexError:
		return None

global obj_list
obj_list = [obj(str(i%50)) for i in range(100)]

def test(func_name, test_num):
	print(func_name)
	print repeat(func_name + "(\"" + str(test_num) + "\", obj_list)", "from __main__ import " + func_name + ", obj_list", number=100000)

test("a", 100)
test("b", 100)
test("c", 100)
