# -*- coding: utf-8 -*-
import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN,\
		USEREVENT, QUIT, KEYDOWN
import string


def modrender(typeface, size, text, antialias, color, maxsize, borderoff):
	# local typeface!
	nofit = True
	while nofit:
		tmpfont = pygame.font.SysFont(typeface, size)
		bool1 = tmpfont.size(text)[0] < maxsize[0] - (2 * borderoff)
		nofit = not (bool1 and tmpfont.size(text)[1] < maxsize[1] - (2 * borderoff))
		if size <= 5:
			nofit = False
		else:
			size -= 1
	return tmpfont.render(text, antialias, color)


def getmaxsize(typeface, size, text, antialias, color, maxsize, borderoff):
	# local typeface!
	nofit = True
	while nofit:
		tmpfont = pygame.font.SysFont(typeface, size)
		bool1 = tmpfont.size(text)[0] < maxsize[0] - (2 * borderoff)
		nofit = not (bool1 and tmpfont.size(text)[1] < maxsize[1] - (2 * borderoff))
		if size <= 5:
			nofit = False
		else:
			size -= 1
	return size


class button():

	def __init__(self, name, content, ratio, button_design, pos_data, layer=1):
		"""Initalises with x and y as center point"""
		# basic font and then everything should be clear
		# three different instances of create_outline!
		# this way three images can be generated

		self.name = name
		self.type = "button"
		self.ratio = ratio
		self.layer = layer
		self.content = content

		size = list(content.get_size())
		if size[0] / float(size[1]) < ratio:
			size[0] = size[1] * ratio

		#set sizes
		self.pos_data = pos_data
		self.pos = pygame.Rect((0, 0), size)
		self.content_pos = pygame.Rect((0, 0), content.get_size())

		self.box_creator = lambda mode: create_outline(button_design, mode, self.pos)

		#create images
		self.buttons = [self.box_creator(mode)[0] for mode in range(3)]

		self.pos.size = create_outline(button_design,
					mode,
					self.pos)[1].size
		#set status
		self.state = 0
		self.klicked = False

		#set position status
		self.checked = False
		self.active_pos_search = False

	def get_rel_pos(self, object_list):
		#set status
		self.checked = True
		self.active_pos_search = True

		if self.pos_data["pos_rel_obj"] == "master_screen":
			rel_pos = object_list[0]
			self.pos_data["from"] = "BottomRight"
		else:
			#search and get relational points
			for obj in object_list[1:]:
				if obj.name == self.pos_data["pos_rel_obj"]:
					if obj.checked:
						if obj.active_pos_search:
							raise RuntimeError("Relational position refers to itself.")
						else:
							rel_pos = obj.pos
					else:
						rel_pos = obj.get_rel_pos(object_list)
		#get point from rect
		rel_point = get_point(rel_pos, self.pos_data["from"])

		#update position
		self.pos.x = int(self.pos_data["x_abs"]
				+ (self.pos_data["x_rel"] * rel_point[0]))
		self.pos.y = int(self.pos_data["y_abs"]
				+ (self.pos_data["y_rel"] * rel_point[1]))

		#set "to" pos to "from" pos
		dest_point = self.pos.topleft
		org_point = get_point(self.pos, self.pos_data["to"])
		self.pos.x += dest_point[0] - org_point[0]
		self.pos.y += dest_point[1] - org_point[1]
		self.content_pos.center = self.pos.center
		self.const_pos_center = self.pos.center

		#reset status and return pos for recursion
		self.active_pos_search = False
		return self.pos

	def update(self, events):
		# changes image when hovered over or being clicked
		# also posts a menu event to show that a button has been clicked
		if self.pos.collidepoint(pygame.mouse.get_pos()) and not self.klicked:
			self.state = 1
			for event in events:
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					menue = pygame.event.Event(USEREVENT, code="MENU")
					#use fastevent else fallback to normal events
					try:
						pygame.fastevent.post(menue)
					except:
						pygame.event.post(menue)
					self.klicked = True
					self.state = 2
		elif not self.klicked:
			self.state = 0
		else:
			self.state = 2

	def blit(self, screen):
		"""Blits the button"""
		screen.blit(self.buttons[self.state], self.pos)
		screen.blit(self.content, self.content_pos)


class input_field():

	def __init__(self, x, y, text, typeface, color, box, layer=1):
		"""Creates a new inputfield"""
		self.name = text
		self.typeface = typeface
		self.color = color
		self.font = pygame.font.SysFont(self.typeface, 30)
		self.header = text
		self.img = box
		self.layer = layer
		self.pos = self.img.get_rect()
		self.pos = self.pos.move(x - (self.pos.w / 2.0), y - (self.pos.h / 2.0))
		self.text = ""
		self.render_text = modrender(self.typeface, 30, self.text,
			True, self.color,
			self.pos.size, 9)
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center
		self.render_header = modrender(self.typeface, 30, self.header,
			True, self.color,
			(50000, 10000), 0)
		self.headerpos = self.render_header.get_rect()
		self.headerpos.center = self.pos.center
		self.headerpos.y -= 50

	def get_all_key_input(self, should_get_all, events):
		"""Gets all pressed keys"""
		for event in events:
			if event.type == QUIT:
				exit()
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				tmp = (not key == "return" and not should_get_all)
				if (event.unicode in string.printable or (key[:5] == "world")) and tmp:
					return event.unicode
				elif should_get_all:
					return key

	def gettext(self, events):
		"""Returns text if return is pressed or removes one if delete is pressed"""
		key = self.get_all_key_input(False, events)
		if key is not None and self.textpos.width < self.pos.width - 18:
			self.text = self.text + key
		if key is None:
			key = self.get_all_key_input(True, events)
			if key == "return":
				return self.text
			if key == "backspace":
				self.text = self.text[:len(self.text) - 1]
		self.render_text = modrender(self.typeface, 30, self.text,
			True, self.color,
			self.pos.size, 9)
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center

	def blit(self, screen):
		"""Blits the inputfield"""
		screen.blit(self.render_header, self.headerpos)
		screen.blit(self.img, self.pos)
		screen.blit(self.render_text, self.textpos)


class slider():

	def __init__(self, name, label, typeface, color, size, ratio,
		options_list, default_value, design, pos_data, layer=1):
		"""Creates a new slider"""
		self.type = "slider"
		self.value = default_value
		self.dragged = False
		self.typeface = pygame.font.SysFont(typeface, int(size))
		self.color = color
		self.options_list = options_list
		self.name = name
		self.label = label
		self.ratio = ratio
		self.layer = layer
		self.knob_pos = pygame.Rect(0, 0, 0, 0)

		self.pos = pygame.Rect(0, 0, 0, 0)
		self.update([])
		self.pos_data = pos_data
		tmp_size = (self.render_text.get_size()[1])
		self.pos.size = (self.ratio * tmp_size, tmp_size)
		self.box = create_outline(design, 0, self.pos)
		self.pos.size = self.box[1].size
		self.knob = pygame.transform.scale(pygame.image.load(design["slider_knob"]),
					(self.pos.w / 15, self.pos.h))
		self.knob_pos = self.knob.get_rect()
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * self.value)
		self.scale = 1.0 / self.pos.w
		self.checked = False
		self.active_pos_search = False

	def get_rel_pos(self, object_list):
		#set status
		self.checked = True
		self.active_pos_search = True

		if self.pos_data["pos_rel_obj"] == "master_screen":
			rel_pos = object_list[0]
			self.pos_data["from"] = "BottomRight"
		else:
			#search and get relational points
			for obj in object_list[1:]:
				if obj.name == self.pos_data["pos_rel_obj"]:
					if obj.checked:
						if obj.active_pos_search:
							raise RuntimeError("Relational position refers to itself.")
						else:
							rel_pos = obj.pos
					else:
						rel_pos = obj.get_rel_pos(object_list)
		#get point from rect
		rel_point = get_point(rel_pos, self.pos_data["from"])

		#update position
		self.pos.x = int(self.pos_data["x_abs"]
				+ (self.pos_data["x_rel"] * rel_point[0]))
		self.pos.y = int(self.pos_data["y_abs"]
				+ (self.pos_data["y_rel"] * rel_point[1]))

		#set "to" pos to "from" pos
		dest_point = self.pos.topleft
		org_point = get_point(self.pos, self.pos_data["to"])
		self.pos.x += dest_point[0] - org_point[0]
		self.pos.y += dest_point[1] - org_point[1]
		self.box[1].center = self.pos.center

		#update knob position
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * self.value)

		#reset status and return pos for recursion
		self.active_pos_search = False
		return self.pos

	def center(self):
		"""Centeres itself around its topleft point"""
		self.pos.center = self.pos.topleft
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * self.value)

	def update(self, events):
		"""Modifies the slider (e.g. pos)"""
		for event in events:
			if event.type == MOUSEBUTTONUP:
				if event.button == 1:
					self.dragged = False
			if event.type == MOUSEBUTTONDOWN:
					if self.pos.collidepoint(pygame.mouse.get_pos()):
						if event.button == 1:
							self.dragged = True
			if self.dragged:
				self.value = (pygame.mouse.get_pos()[0] - self.pos.left) * self.scale

		if self.value < 0:
			self.value = 0
		if self.value > 1:
			self.value = 1

		if self.value <= 0.01:
			self.value = 0.0
		if self.value >= 0.995:
			self.value = 1.0000000001
		tmp = (self.value * (self.pos.w - self.knob_pos.w))
		self.knob_pos.left = self.pos.left + tmp

		steps = 1.0 / len(self.options_list)
		for area in range(len(self.options_list)):
			area += 1
			if self.value <= steps * area and self.value >= steps * (area - 1):
				break
		text = self.label + ": " + self.options_list[area - 1]
		self.render_text = self.typeface.render(text, True, self.color)

		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center

	def blit(self, screen):
		"""Blits the slider"""
		screen.blit(self.box[0], self.box[1])
		screen.blit(self.knob, self.knob_pos)
		screen.blit(self.render_text, self.textpos)


class text():

	default_conf = {
		"color": [0, 0, 0],
		"font": "monospace",
		"size": 20,
		"bold": False,
		"italics": False,
		"underline": False,
		"anitalias": True}

	def __init__(self, name, label, font_config, pos_data, layer=1):
		self.type = "text"
		self.name = name
		self.label = label
		self.conf = font_config
		for attr in ["color", "font", "size",
				"bold", "italics", "underline", "anitalias"]:
			if attr not in self.conf:
				self.conf[attr] = text.default_conf[attr]

		self.conf["size"] = int(self.conf["size"])

		self.layer = layer
		self.renderer = pygame.font.SysFont(self.conf["font"], self.conf["size"],
					bold=self.conf["bold"], italic=self.conf["italics"])
		self.renderer.set_underline(self.conf["underline"])
		self.text_img = self.render()
		self.pos_data = pos_data
		self.pos = pygame.Rect((0, 0), self.text_img.get_size())

		self.checked = False
		self.active_pos_search = False

	def get_rel_pos(self, object_list):
		#set status
		self.checked = True
		self.active_pos_search = True

		if self.pos_data["pos_rel_obj"] == "master_screen":
			rel_pos = object_list[0]
			self.pos_data["from"] = "BottomRight"
		else:
			#search and get relational points
			for obj in object_list[1:]:
				if obj.name == self.pos_data["pos_rel_obj"]:
					if obj.checked:
						if obj.active_pos_search:
							raise RuntimeError("Relational position refers to itself.")
						else:
							rel_pos = obj.pos
					else:
						rel_pos = obj.get_rel_pos(object_list)
		#get point from rect
		rel_point = get_point(rel_pos, self.pos_data["from"])

		#update position
		self.pos.x = int(self.pos_data["x_abs"]
				+ (self.pos_data["x_rel"] * rel_point[0]))
		self.pos.y = int(self.pos_data["y_abs"]
				+ (self.pos_data["y_rel"] * rel_point[1]))

		#set "to" pos to "from" pos
		dest_point = self.pos.topleft
		org_point = get_point(self.pos, self.pos_data["to"])
		self.pos.x += dest_point[0] - org_point[0]
		self.pos.y += dest_point[1] - org_point[1]

		#reset status and return pos for recursion
		self.active_pos_search = False
		return self.pos

	def render(self):
		self.text_img = self.renderer.render(self.label,
						self.conf["anitalias"], self.conf["color"])
		return self.text_img

	def update(self, events):
		pass

	def blit(self, screen):
		screen.blit(self.text_img, self.pos)


class image():

	def __init__(self, name, image, pos_data, klickable=False, layer=1):
		if type(image) in [str, file]:
			self.image = pygame.image.load(image)
		elif type(image) == pygame.Surface:
			self.image = image
		self.pos_data = pos_data
		self.layer = layer
		if klickable:
			self.type = "klickable_image"
		else:
			self.type = "image"
		self.name = name
		self.pos = pygame.Rect(0, 0, 0, 0)
		self.checked = False
		self.active_pos_search = False

	def update(self, events):
		pass

	def get_rel_pos(self, object_list):
		#set status
		self.checked = True
		self.active_pos_search = True

		if self.pos_data["pos_rel_obj"] == "master_screen":
			rel_pos = object_list[0]
			self.pos_data["from"] = "BottomRight"
		else:
			#search and get relational points
			for obj in object_list[1:]:
				if obj.name == self.pos_data["pos_rel_obj"]:
					if obj.checked:
						if obj.active_pos_search:
							raise RuntimeError("Relational position refers to itself.")
						else:
							rel_pos = obj.pos
					else:
						rel_pos = obj.get_rel_pos(object_list)
		#get point from rect
		rel_point = get_point(rel_pos, self.pos_data["from"])

		#update position
		self.pos.x = int(self.pos_data["x_abs"]
				+ (self.pos_data["x_rel"] * rel_point[0]))
		self.pos.y = int(self.pos_data["y_abs"]
				+ (self.pos_data["y_rel"] * rel_point[1]))

		#set "to" pos to "from" pos
		dest_point = self.pos.topleft
		org_point = get_point(self.pos, self.pos_data["to"])
		self.pos.x += dest_point[0] - org_point[0]
		self.pos.y += dest_point[1] - org_point[1]

		#reset status and return pos for recursion
		self.active_pos_search = False
		return self.pos

	def blit(self, screen):
		screen.blit(self.image, self.pos)


def create_outline(button_design, mode, rect):

	design = pygame.image.load(button_design["outline"])
	color = None

	# gets selected background color
	if "inner_color" in button_design:
		design_color = button_design["inner_color"]
		color = tuple([int(design_color[i]) for i in range(len(design_color))])
	else:
		color = (0, 0, 0, 0)

	#prepare outline
	design_rect = design.get_rect()
	design_size = design_rect.h
	# extract the selected collum
	line_string = pygame.Surface((1, design_size))
	line_string.blit(design, (0, 0), pygame.Rect(mode, 0, 1, design_size))
	design = line_string
	design_rect = design.get_rect()
	# pixels for the straight lines
	pattern = pygame.Surface((1, design_size))
	# set the pixel colors for the pattern
	for a in range(design_size):
		pattern.set_at((0, a), design.get_at((0, a)))
	#transforms linear pattern into a corner
	corner = pygame.Surface((design_size, design_size))
	for a in range(design_size):
		for x in range(design_size):
			for y in range(design_size):
				if x >= a and y >= a:
					corner.set_at((x, y), pattern.get_at((0, a)))
	width = rect.w
	height = rect.h
	border_size = design_size
	width += border_size * 2
	height += border_size * 2

	# creating top frame line
	top = pygame.Surface((width, border_size))
	for pos in range(width):
		top.blit(pattern, pygame.Rect(pos, 0, 0, 0))

	# blit left top corner
	top.blit(corner, pygame.Rect(0, 0, 0, 0))

	# blit right top corner
	top.blit(pygame.transform.flip(corner, True, False),
				pygame.Rect(width - border_size, 0, 0, 0))

	# create bottom line
	bottom = pygame.transform.flip(top, False, True)

	# create left frame line
	left = pygame.Surface((border_size, height))
	tmp_pattern = pygame.transform.rotate(pattern, 90)
	for pos in range(height):
		left.blit(tmp_pattern, pygame.Rect(0, pos, 0, 0))

	# create right frame line
	right = pygame.transform.flip(left, True, False)

	# Merge all together
	final = pygame.Surface((width, height), pygame.SRCALPHA)
	final.fill(color)
	final.blit(left, pygame.Rect(0, 0, 0, 0))
	final.blit(right, pygame.Rect(width - border_size, 0, 0, 0))
	final.blit(top, pygame.Rect(0, 0, 0, 0))
	final.blit(bottom, pygame.Rect(0, height - border_size, 0, 0))

	pos = final.get_rect()
	pos.x = rect.x - border_size
	pos.y = rect.y - border_size

	return final, pos


def get_point(rect, point_name):
	point_name = point_name.lower()
	if point_name == "topleft":
		return rect.topleft
	if point_name in ["topcenter", "topmid"]:
		return rect.midtop
	if point_name == "topright":
		return rect.topright
	if point_name == "centerleft":
		return rect.midleft
	if point_name in ["centercenter", "center", "midmid", "mid"]:
		return rect.center
	if point_name == "centerright":
		return rect.midright
	if point_name == "bottomleft":
		return rect.bottomleft
	if point_name in ["bottomcenter", "bottommid"]:
		return rect.midbottom
	if point_name == "bottomright":
		return rect.bottomright

	#did not match
	raise ValueError(point_name + " is not a valid point.")
