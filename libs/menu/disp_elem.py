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

	def __init__(self, name, label, typeface, color, size,
			ratio, button_design, pos_data):
		"""Initalises with x and y as center point"""
		# basic font and then everything should be clear
		# three different instances of create_outline!
		# this way three images can be generated

		self.name = name
		self.type = "button"

		# Loads the font
		self.font = pygame.font.SysFont(typeface, int(size))

		# renders the text and creates a rect
		self.label = label
		text = self.font.render(self.label, True, color)
		text_pos = text.get_rect()

		# creating emtpy surface that is the size of the desired button
		self.ratio = ratio
		tmp_centertext_image = pygame.Surface((text_pos.h * ratio,
						text_pos.h)).convert_alpha()
		tmp_centertext_image.fill((0, 0, 0, 0))
		tmp_center_pos = tmp_centertext_image.get_rect()

		# bliting the text onto the surface
		text_pos.center = tmp_center_pos.center
		tmp_centertext_image.blit(text, text_pos)

		# Adding image to interface
		text = tmp_centertext_image
		text_pos = text.get_rect()

		# saving typeface for later use
		self.typeface = typeface

		#set temporary position
		self.pos_data = pos_data
		self.pos = pygame.Rect((0, 0), text_pos.size)

		#create images and add text inside button
		self.buttons = []
		for num in range(3):
			self.buttons.append(create_outline(button_design))
			self.buttons[num].create_box(num, self.pos)

			# defines position in the middle of button
			text_pos.centerx = self.buttons[num].pos.centerx - self.buttons[num].pos.x

			text_pos.centery = self.buttons[num].pos.centery - self.buttons[num].pos.y
			# blits text centered in button
			self.buttons[num].box.blit(text, text_pos)
		self.pos.size = self.buttons[0].pos.size

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
			self.pos_data["relation_point"] = "BottomRight"
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

	def changetext(self, text, color):
		"""Changes the text inside the button"""
		# renders the text and creates a rect
		text = self.font.render(text, True, color)
		text_pos = text.get_rect()

		# creating emtpy surface that is the size of the desired button
		tmp_centertext_image = pygame.Surface((text_pos.h * self.ratio,
					text_pos.h)).convert_alpha()
		tmp_centertext_image.fill((0, 0, 0, 0))
		tmp_center_pos = tmp_centertext_image.get_rect()

		# bliting the text onto the surface
		text_pos.center = tmp_center_pos.center
		tmp_centertext_image.blit(text, text_pos)
		text = tmp_centertext_image

		for num in range(len(self.buttons)):
			self.buttons[num].create_box(num, text_pos)
			text_pos.center = self.buttons[num].pos.center
			self.buttons[num].box.blit(text, text_pos)

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
		screen.blit(self.buttons[self.state].box, self.pos)


class input_field():

	def __init__(self, x, y, text, typeface, color, box):
		"""Creates a new inputfield"""
		self.name = text
		self.typeface = typeface
		self.color = color
		self.font = pygame.font.SysFont(self.typeface, 30)
		self.header = text
		self.img = box
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
		options_list, default_value, box, pos_data):
		"""Creates a new slider"""
		self.type = "slider"
		self.value = default_value
		self.box = create_outline(box)
		self.dragged = False
		self.typeface = pygame.font.SysFont(typeface, size)
		self.color = color
		self.options_list = options_list
		self.name = name
		self.label = label
		self.borderoff = box["border_size"]
		self.state = 1
		self.ratio = ratio
		self.knob_pos = pygame.Rect(0, 0, 0, 0)

		self.pos = pygame.Rect(0, 0, 0, 0)
		self.update([])
		self.pos_data = pos_data
		tmp_size = (self.render_text.get_size()[1])
		self.pos.size = (self.ratio * tmp_size, tmp_size)
		self.box.create_box(0, self.pos)
		self.pos.size = self.box.box.get_size()
		self.knob = pygame.transform.scale(pygame.image.load(box["slider_knob"]),
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
		self.state = area - 1
		self.render_text = self.typeface.render(text, True, self.color)

	def blit(self, screen):
		"""Blits the slider"""
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center
		screen.blit(self.box.box, self.pos)
		screen.blit(self.knob, self.knob_pos)
		screen.blit(self.render_text, self.textpos)


class create_outline():

	def __init__(self, button_design):
		self.resources = button_design
		self.modes = [self.create_template(a) for a in range(3)]

	def create_template(self, x_pos):
		design = self.resources["outline"]
		design = pygame.image.load(design)
		self.color = None

		# gets selected background color
		if "inner_color" in self.resources:
			color = self.resources["inner_color"]
			if len(color) == 3:
				self.color = (int(color[0]), int(color[1]), int(color[2]))
			if len(color) == 4:
				self.color = (int(color[0]), int(color[1]), int(color[2]), int(color[3]))
		else:
			self.color = (0, 0, 0, 0)

		design_rect = design.get_rect()
		size = design_rect.h
		# extract the selected collum
		line_string = pygame.Surface((1, size))
		line_string.blit(design, (0, 0), pygame.Rect(x_pos, 0, 1, size))
		design = line_string
		design_rect = design.get_rect()
		self.pixels = {}
		# create the final surface to blit pattern to
		self.pattern = pygame.Surface((1, size))
		# set the pixel colors for the pattern
		for a in range(size):
			self.pattern.set_at((0, a), design.get_at((0, a)))
		# transforms linear pattern into a corner
		corner = pygame.Surface((size, size))
		for a in range(size):
			for x in range(size):
				for y in range(size):
					if x >= a and y >= a:
						corner.set_at((x, y), self.pattern.get_at((0, a)))
		return [self.pattern, corner]

	def create_box(self, mode, rect):
		posx = rect.x
		posy = rect.y
		width = rect.w
		height = rect.height
		border = self.modes[mode][0].get_height()
		width += border * 2
		height += border * 2
		self.top = pygame.Surface((width, border))

		# creating top frame line
		for pos in range(width):
			self.top.blit(self.modes[mode][0], pygame.Rect(pos, 0, 0, 0))

		# blit left top corner
		self.top.blit(self.modes[mode][1], pygame.Rect(0, 0, 0, 0))

		# blit right top corner
		self.top.blit(pygame.transform.flip(self.modes[mode][1], True, False),
					pygame.Rect(width - border, 0, 0, 0))

		# create bottom line
		self.bottom = pygame.transform.flip(self.top, False, True)

		# create left frame line
		self.left = pygame.Surface((border, height))
		tmp_line = pygame.transform.rotate(self.modes[mode][0], 90)
		for pos in range(height):
			self.left.blit(tmp_line, pygame.Rect(0, pos, 0, 0))

		# create right frame line
		self.right = pygame.transform.flip(self.left, True, False)

		# Merge all together
		final = pygame.Surface((width, height), pygame.SRCALPHA)
		final.fill(self.color)
		final.blit(self.left, pygame.Rect(0, 0, 0, 0))
		final.blit(self.right, pygame.Rect(width - border, 0, 0, 0))
		final.blit(self.top, pygame.Rect(0, 0, 0, 0))
		final.blit(self.bottom, pygame.Rect(0, height - border, 0, 0))

		self.box = final
		self.pos = self.box.get_rect()
		self.pos.x = posx - border
		self.pos.y = posy - border

		return (self.pos, self.box)


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
