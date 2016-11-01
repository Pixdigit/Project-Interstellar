# -*- coding: utf-8 -*-

"""File wrapper for tygamusic.
Use print tygamusic.CreateQueue.__doc__ for usage.

Warning: Wrong usage of multiple objects may lead to:
	ERRORS!!!!!!
	UNEXPECTED BEHAVIOUR!!!!!!!
So please be carefull…
"""

import os
import pygame
from pygame.locals import USEREVENT
import random


class CreateQueue():
	"""Initizalize a new Playlist-like object.

usage:
object = CreateQueue(path, exceptbegin, endevent=USEREVENT+100)

path (string)
	is the path tygamusic should search for availible music.
exceptbegin (string)
	is used to have music in path wich shouldn't be read.
	E.g. when "TEST" is passed,
	all files beginning with TEST will be ignored.
endevent (int, default = USEREVENT+100)
	is an internal value what eventnumber should be posted
	if no music stream is playing.
	Only to be used to avoid other custom events in pygame.


To find out what variables there are check
	tygamusic.CreateQueue.__init__.__doc__
"""

	def __init__(self, path, exceptbegin, endevent=USEREVENT + 100):
		"""Create variables and initialize system

self.files (list)
	A list of all files for possible playback.
self.playlist (list)
	A list containing the filenames of the songs.
self.volume (float)
	A value from 0 to 1 for playback volume.
	Volume gets updated if self.update is called.

These are internal values that should not be modified unless
	you are 100% sure what you do.

self._endeventnum (int)
	An int used for defining the event when music playback has stopped.
	Changing this after creating the object has no effect.
self._path (str)
	This contains the path to from where music should be loaded.
self._pauselevel (int)
	An int representing how many songs have been paused
	while an other song was already paused.
self._playing (bool)
	Determines wether a song is currently loaded (aka "playing")
self._timeplayed (dict)
	A dictionary with entrys looking like this:
	self._timeplayed[filename] = current_playing_pos
	A value for current_playing_pos is only set when
	music gets paused.
"""
		self._endeventnum = endevent
		pygame.mixer.music.set_endevent(self._endeventnum)
		self.__endevent = pygame.event.Event(self._endeventnum)
		self.playlist = []
		self._timeplayed = {}
		self.volume = 0.5
		self._pauselevel = 0
		self._playing = False
		self._path = path
		self.__exception = exceptbegin
		self.files = self.get_music()
		if len(self.files) == 0:
			print(("Warning: Playlist Empty !"))
			self.files = [None]
		while len(self.playlist) < len(self.files) - 1 and self.files != [None]:
			self.add_random(0)
			self.remove_dublicates()

	def get_music(self):
		"""Return all files with given conditions."""
		# Look up tygamusic.CreateQueue.__init__.__doc__ for more info
		files = []
		# Runs through all files and checks for filetype
		for filename in os.listdir(self._path):
			supportedmusic = [
				filename.endswith(".ogg") or filename.endswith(".mp3")
				or filename.endswith(".mid") or filename.endswith(".midi")
				or filename.endswith(".wav")]

			# Adds file if it is supported format
			#    and doesn't begin with specified beinning
			if (supportedmusic[0] and
			filename[0:len(self.__exception)] != self.__exception):
				files.append(filename)
		return files

	def update(self, events=False, shouldplaynextsong=False):
		"""Update variables and process events.

Usage:
self.update(events=true, shouldplaynextsong=True)

If no arguments are passed the event queue will be read
	and a new song will be played, if the current has ended.

events (list)
	A list containing events
		(you will need this if you want to get other user inputs).
shouldplaynextsong (bool)
	Set this to False if you don't want a new song to be played
		if music has ended
"""

		# Adjust volume to its own volume.
		pygame.mixer.music.set_volume(self.volume)
		# Adds a random song to playlist
		#    if it is smaller than the amount of music provided
		if len(self.playlist) < len(self.files) - 1 and self.files != [None]:
			self.add_random("end")
		# If no events are specified pygame.event.get()
		#    will be called.
		if type(events) == bool:
			if events:
				events = pygame.event.get()
				# Playes next song if the previous one has ended.
				if self.__endevent in events and shouldplaynextsong:
					self.playlist.pop(0)
					self._playing = False
					self.play("play", 0)
		elif type(events) == list:
			if self.__endevent in events and shouldplaynextsong:
				self.playlist.pop(0)
				self._playing = False
				self.play("play", 0)

	def play(self, *options):
		"""Control music playback.

Usage:
self.play(operation, *options)
Operations:
"play" (amount of replays can be defined optionally)
"next" (amount of replays can be defined optionally)
"loop"
"pause"
"unpause"
"stop"

Look up individual options's comments below for an in depth explanation.
"""
		options = list(options)
		if options[0] == "play" and len(self.playlist) != 0:
			# first song of playlist is played if none is playing
			if len(options) == 1:
				options.append(0)
			if len(options) == 2:
				# Playes new song or loads it, if neccessary.
				if not self._playing:
					pygame.mixer.music.load(self._path + self.playlist[0])
					pygame.mixer.music.play(options[1], 0)
					# Add new song to dict
					self._timeplayed[self.playlist[0]] = 0
				if self._playing:
					pygame.mixer.music.play(options[1], 0)
				self._playing = True

		if options[0] == "next":
			# remove old song
			self._timeplayed[self.playlist[0]] = 0
			self.playlist.pop(0)
			self._playing = False
			# add second option if not given
			if len(options) == 1:
				options.append(0)
			self.play("play", options[1])

		if options[0] == "pause" and len(self.playlist) != 0:
			# Pauses current music and saves its position.
			# The -1000 makes it more natural because resuming
			#    can only be done in whole seconds
			#    and makes it easier to recognize position.
			currentpos = int(pygame.mixer.music.get_pos() / 1000.0 - 1000)
			# When song just started negative results may possible.
			if currentpos <= 0:
				currentpos += 1000
			try:  # try is cheaper than if
				self._timeplayed[self.playlist[self._pauselevel]] += currentpos
			except:
				self._timeplayed[self.playlist[self._pauselevel]] = currentpos
			self._playing = False
			self._pauselevel += 1
			pygame.mixer.music.pause()

		if options[0] == "unpause" and len(self.playlist) != 0:
			# Restarts music and removes previous music if it hasnt been paused yet.
			# the check is needed if someone unpauses more than pauses
			if self._pauselevel > 0:
				self._pauselevel -= 1
			while self._timeplayed[self.playlist[0]] == 0 and len(self.playlist) > 1:
				self.playlist.pop(0)
			pygame.mixer.music.load(self._path + self.playlist[0])
			pygame.mixer.music.play(0, self._timeplayed[self.playlist[0]])
			self._playing = True

		if options[0] == "stop":
			# Stops current song.
			pygame.mixer.music.stop()
			self._timeplayed[self.playlist[0]] = 0
			self._playing = False

		if options[0] == "loop":
			# Playes current song in a loop.
			self._timeplayed[self.playlist[0]] = 0
			pygame.mixer.music.load(self._path + self.playlist[0])
			self.play("play", -1)

	def add_random(self, pos):
		"""Adds random song to playlist.

Usage: self.add_random(pos)
pos (int)
	Position where to place new song.
	Alternativly "end" can be passed too
	to add a song to the end.
"""
		# Makes it easier to add song at end by using "end" as pos.
		if type(pos) is str:
			if pos == "end" and len(self.playlist) != 0:
				pos = len(self.playlist)
			else:
				pos = 0

		# Ensures that we actually have songs to load.
		if self.files != [None]:
			# Selects a new song and ensures that never two songs are directly
			#    after each other.
			newsong = self.files[random.randint(0, len(self.files) - 1)]
			result = False
			if len(self.playlist) != 0:
				while not result:
					newsong = self.files[random.randint(0, len(self.files) - 1)]
					try:
						# checks right neighbor is diffrent
						right = not (newsong == self.playlist[pos + 1])
					except:
						# if has no neighbor, left decides
						# (if left is true then end result is true
						#  if left is false then end result is false)
						right = True
					try:
						# checks left neighbor if diffrent and decides
						# if one of both partner is diffrent as newsong
						result = right and not (newsong == self.playlist[pos])
					except:
						# if no left neighbor right decides
						result = right
			else:
				# If it is only song, there are no neighbours to check.
				newsong = self.files[random.randint(0, len(self.files) - 1)]

			# Adds song at pos to playlist.
			self.queue(newsong, pos)

	def remove_dublicates(self):
		"""Removes dublicate songs whilst preserving order."""
		# These three lines werent done by me
		# and only slightly modified
		# Thanks to http://www.peterbe.com/plog/uniqifiers-benchmark
		# for creating them (i think he did it but im not sure)
		seen = set()
		seen_add = seen.add
		self.playlist = [x for x in self.playlist if not (x in seen or seen_add(x))]

	def queue(self, song, pos):
		"""Queues the new song at position.

Usage: self.queue(pos)
pos (int)
	Position where to place new song.
	Alternativly "end" can be passed too
	to add a song to the end.
"""
		# makes it easier to add song at end by using "end" as pos
		if type(pos) is str:
			if pos == "end":
				pos = len(self.playlist)
			else:
				pos = 0

		# adds song at pos to playlist
		self.playlist.insert(pos, song)
