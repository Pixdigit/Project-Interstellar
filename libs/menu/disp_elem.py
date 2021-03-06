# -*- coding: utf-8 -*-
import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN,\
		USEREVENT, QUIT, KEYDOWN
import string
import templates


def modrender(typeface, size, text, antialias, color, maxsize, borderoff):
	#renders with maximum size
	# local typeface!
	nofit = True
	while nofit:
		tmpfont = pygame.font.SysFont(typeface, size)
		height_fits = tmpfont.size(text)[0] < maxsize[0] - (2 * borderoff)
		nofit = not (height_fits
			and tmpfont.size(text)[1] < maxsize[1] - (2 * borderoff))
		if size <= 5:
			nofit = False
		else:
			size -= 1
	return tmpfont.render(text, antialias, color)


class button(templates.element_template, object):

	def __init__(self, name, content_obj, ratio, button_design, pos_data, layer=1):
		"""Initalises with x and y as center point"""
		#Note: No actual prototype behaviour from JS
		self.proto = super(button, self)
		self.proto.__init__()
		self.name = name
		self.type = "button"
		self.ratio = ratio
		self.layer = layer
		self.content = content_obj
		self.button_design = button_design

		#set size to ratio
		size = list(self.content.get_size())
		if size[0] / float(size[1]) < ratio:
			size[0] = int(size[1] * ratio)

		self.pos_data = pos_data
		self.pos.size = size
		self.ever_center = self.pos.center

		#create the images of the button
		self.buttons = []
		for i in range(3):
			image = create_outline(button_design, i, self.pos)[0]
			self.content.pos.center = (image.get_size()[0] / 2, image.get_size()[1] / 2)
			self.content.blit(image)
			self.buttons.append(image)
		#adjust rect to include border
		self.pos.size = image.get_size()

		#set status
		self.state = 0
		self.klicked = False

	def get_rel_pos(self, object_list):
		self.proto.get_rel_pos(object_list)
		self.ever_center = self.pos.center
		return self.pos

	def change_text(self, new_text):
		assert self.content.type == "text"  # Tried to change text of image

		self.content.change_text(new_text)

		size = list(self.content.get_size())
		if size[0] / float(size[1]) < self.ratio:
			size[0] = int(size[1] * self.ratio)

		self.buttons = []
		for i in range(3):
			image = create_outline(self.button_design, i, pygame.Rect((0, 0), size))[0]
			self.content.pos.center = (image.get_size()[0] / 2, image.get_size()[1] / 2)
			self.content.blit(image)
			self.buttons.append(image)
		self.img = self.buttons[self.state]
		self.pos.size = self.img.get_size()
		self.pos.center = self.ever_center

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
		self.img = self.buttons[self.state]


class input_field(templates.element_template, object):

	def __init__(self, x, y, text, typeface, color, box, layer=1):
		"""Creates a new inputfield"""
		#Note: No actual prototype behaviour from JS
		self.proto = super(input_field, self)
		self.proto.__init__()
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
		self.proto.blit(screen)
		screen.blit(self.render_header, self.headerpos)
		screen.blit(self.render_text, self.textpos)


class slider(templates.element_template, object):

	def __init__(self, name, label, typeface, color, size, ratio,
		options_list, default_value, design, pos_data, layer=1):
		"""Creates a new slider"""
		#Note: No actual prototype behaviour from JS
		self.proto = super(slider, self)
		self.proto.__init__()
		self.type = "slider"
		#Set the slider centered in the category
		self.value = default_value + 1.0 / (len(options_list) * 2)
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
		self.img, pos = create_outline(design, 0, self.pos)
		self.pos.size = pos.size
		self.knob = pygame.transform.scale(pygame.image.load(design["slider_knob"]),
					(self.pos.w / 15, self.pos.h)).convert()
		self.knob_pos = self.knob.get_rect()
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * self.value)
		self.scale = 1.0 / self.pos.w

	def get_rel_pos(self, object_list):
		self.pos = self.proto.get_rel_pos(object_list)
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * self.value)
		return self.pos

	def get_selection_index(self):
		steps = 1.0 / len(self.options_list)
		for area in range(len(self.options_list)):
			area += 1
			if self.value <= steps * area and self.value >= steps * (area - 1):
				break
		return area - 1

	def get_selection_name(self):
		return self.options_list[self.get_selection_index()]

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

		text = self.label + ": " + self.get_selection_name()
		self.render_text = self.typeface.render(text, True, self.color)

		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center

	def blit(self, screen):
		"""Blits the slider"""
		self.proto.blit(screen)
		screen.blit(self.knob, self.knob_pos)
		screen.blit(self.render_text, self.textpos)


class text(templates.element_template, object):

	def __init__(self, name, label, font_config, pos_data, layer=1):
		#Note: No actual prototype behaviour from JS
		self.proto = super(text, self)
		self.proto.__init__()
		self.type = "text"
		self.name = name
		self.label = label
		self.conf = font_config
		for attr in ["color", "font", "size",
				"bold", "italics", "underline", "anitalias"]:
			if attr not in self.conf:
				self.conf[attr] = templates.default_font_conf[attr]

		self.conf["size"] = int(self.conf["size"])

		self.layer = layer
		self.renderer = pygame.font.SysFont(self.conf["font"], self.conf["size"],
					bold=self.conf["bold"], italic=self.conf["italics"])
		self.renderer.set_underline(self.conf["underline"])
		self.img = self.render()
		self.pos_data = pos_data
		self.pos = pygame.Rect((0, 0), self.img.get_size())

	def get_size(self):
		return self.renderer.size(self.label)

	def change_text(self, new_text):
		self.label = new_text
		self.render()
		self.pos.size = self.img.get_size()

	def render(self):
		self.img = self.renderer.render(self.label,
						self.conf["anitalias"], self.conf["color"])
		return self.img


class image(templates.element_template, object):

	def __init__(self, name, image_data, pos_data, layer=1):
		#Note: No actual prototype behaviour from JS
		self.proto = super(image, self)
		self.proto.__init__()
		if type(image_data) in [str, file]:
			self.img = pygame.image.load(image_data).convert()
		elif type(image_data) == pygame.Surface:
			self.img = image_data
		self.pos_data = pos_data
		self.layer = layer
		self.type = "image"
		self.name = name
		self.pos = pygame.Rect((0, 0), self.img.get_size())


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
	final = final.convert_alpha()

	pos = pygame.Rect((rect.x - border_size, rect.y - border_size),
			final.get_size())

	return final, pos
