# -*- coding: utf-8 -*-
import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN, USEREVENT, QUIT, KEYDOWN
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

	def __init__(self, name, rel_x, x, rel_y, y, ref, content_in, typeface,
			size, ratio, color, button_designs):
		"""Initalises with x and y as center point"""
		# basic font and then everything should be clear
		# three different instances of create_outline!
		# this way three images can be generated

		# This prepares button for either to contain text or an image
		self.isimage = False
		if content_in != name:  # True = Image
			if type(content_in) == pygame.Surface:  # Surf already exists
				content = content_in
				contentpos = content.get_rect()
				self.isimage = True
			elif type(content_in) == str:  # Only string is provided image needs loading
				content = pygame.image.load(content_in).convert_alpha()
				contentpos = content.get_rect()
				self.isimage = True
		else:  # False = Font/Text
			# Loads the font
			self.font = pygame.font.SysFont(typeface, int(size))

			# renders the text and creates a rect
			content = self.font.render(name, True, color)
			contentpos = content.get_rect()

			# creating emtpy surface that is the size of the desired button
			self.ratio = ratio
			tmp_centertext_image = pygame.Surface((contentpos.h * ratio,
						contentpos.h)).convert_alpha()
			tmp_centertext_image.fill((0, 0, 0, 0))
			tmp_center_pos = tmp_centertext_image.get_rect()

			# bliting the text onto the surface
			contentpos.center = tmp_center_pos.center
			tmp_centertext_image.blit(content, contentpos)

			# Adding image to interface
			content = tmp_centertext_image
			contentpos = content.get_rect()
			# saving typeface for later use
			self.typeface = typeface

		# creating ouline templates
		normal = create_outline(button_designs[0])
		hover = create_outline(button_designs[0])
		klick = create_outline(button_designs[0])
		self.buttons = [normal, hover, klick]
		self.state = 0
		self.name = name
		self.klicked = False
		# calcualte absolute position
		# and define rect
		x = x + rel_x * float(ref.w)
		y = y + rel_y * float(ref.h)
		self.pos = pygame.Rect((x, y), contentpos.size)
		self.move(x, y)
		# move buttons and create images
		# also adds content inside button
		for num in range(len(self.buttons)):
			self.buttons[num].create_box(num, self.pos)
			# defines position in the middle of button
			contentpos.centerx = self.buttons[num].pos.centerx - self.buttons[num].pos.x
			contentpos.centery = self.buttons[num].pos.centery - self.buttons[num].pos.y
			# blits content centered in button
			self.buttons[num].box.blit(content, contentpos)
		self.pos.size = self.buttons[0].pos.size

	def center(self):
		"""Moves position so that the position is now the center position"""
		self.move(self.pos.x - self.pos.w / 2,
			self.pos.y - self.pos.h / 2)

	def changetext(self, text, color, ratio):
		"""Changes the text inside the button"""
		# renders the text and creates a rect
		content = self.font.render(text, True, color)
		contentpos = content.get_rect()

		# creating emtpy surface that is the size of the desired button
		tmp_centertext_image = pygame.Surface((contentpos.h * ratio,
					contentpos.h)).convert_alpha()
		tmp_centertext_image.fill((0, 0, 0, 0))
		tmp_center_pos = tmp_centertext_image.get_rect()

		# bliting the text onto the surface
		contentpos.center = tmp_center_pos.center
		tmp_centertext_image.blit(content, contentpos)
		content = tmp_centertext_image
		for num in range(len(self.buttons)):
			self.buttons[num].create_box(num, contentpos)
			contentpos.center = self.buttons[num].pos.center
			self.buttons[num].box.blit(content, contentpos)

	def move(self, x, y):
		"""Moves the button to topleft = x, y"""
		self.pos.topleft = (0, 0)
		self.pos = self.pos.move(x, y)

	def update(self, events):
		# changes image when hovered over or being clicked
		# also posts a menu event to show that a button has been clicked
		if self.pos.collidepoint(pygame.mouse.get_pos()) and not self.klicked:
			self.state = 1
			for event in events:
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					menue = pygame.event.Event(USEREVENT, code="MENU")
					pygame.fastevent.post(menue)
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

	def __init__(self, name, default_value, size, ratio, typeface, color, box,
		rel_x, x, rel_y, y, ref, options_list=False):
		"""Creates a new slider"""
		self.value = default_value
		self.box = create_outline(box[0])
		self.dragged = False
		self.typeface = pygame.font.SysFont(typeface, size)
		self.color = color
		self.options_list = options_list
		self.name = name
		self.borderoff = box[3]
		self.state = 1
		self.ratio = ratio
		self.knob_pos = pygame.Rect(0, 0, 0, 0)

		self.pos = pygame.Rect(0, 0, 0, 0)
		self.update([])
		rel_x *= float(ref.w)
		rel_y *= float(ref.h)
		x += rel_x
		y += rel_y
		tmp_size = (self.render_text.get_size()[1])
		self.pos.size = (self.ratio * tmp_size, tmp_size)
		self.box.create_box(0, self.pos)
		self.pos.size = self.box.box.get_size()
		self.pos.topleft = (x, y)
		self.knob = pygame.transform.scale(pygame.image.load(box[1]),
					(self.pos.w / 15, self.pos.h))
		self.knob_pos = self.knob.get_rect()
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * self.value)
		self.scale = 1.0 / self.pos.w

	def center(self):
		"""Centeres itself around its x and y position"""
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

		if type(self.options_list) == bool:
			# adding a "." to the end to ensure at least one is included
			text = str(self.value * 100)[:3] + "."
			# removes "." and everything behind it
			text = text[:text.index(".")]
			# Adds the description and the % at the end
			text = self.name + ": " + text + "%"
			# Turns text into a pygame.Surface
			self.render_text = self.typeface.render(text, True, self.color)
			self.is_defined_list = False
		else:
			steps = 1.0 / len(self.options_list)
			for area in range(len(self.options_list)):
				area += 1
				if self.value <= steps * area and self.value >= steps * (area - 1):
					break
			text = self.name + ": " + self.options_list[area - 1]
			self.state = area - 1
			self.render_text = self.typeface.render(text, True, self.color)
			self.is_defined_list = True

	def blit(self, screen):
		"""Blits the slider"""
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center
		screen.blit(self.box.box, self.pos)
		screen.blit(self.knob, self.knob_pos)
		screen.blit(self.render_text, self.textpos)


class create_outline():

	def __init__(self, template_file):
		self.resources = {}
		self.read_file(template_file)
		self.modes = {}
		for a in range(3):
			self.modes[a] = self.create_template(a)

	def read_file(self, template_file):
		def split(line, splitter):
			rline = line[line.index(splitter) + 1:].strip()
			lline = line[:line.index(splitter)].strip()
			return lline, rline

		with open(template_file) as conf_file:
			for line in conf_file:
				if line[0] != "#":
					option, var = split(line, "=")
					self.resources[option] = var

	def create_template(self, pos):
		from creator import convert2list
		design = self.resources["design"]
		design = pygame.image.load(design)
		self.color = None

		# gets selected background color
		if "inner_color" in self.resources:
			color = convert2list(self.resources["inner_color"])
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
		line_string.blit(design, (0, 0), pygame.Rect(pos, 0, 1, size))
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
