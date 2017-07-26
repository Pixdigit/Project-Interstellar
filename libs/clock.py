import time


class timer():

	"""
		A simple timer class for not-so-accurate time measurements.

		When initialized timer is in stopped state.
		Use stop() pause() and start() to control the timer.
		get_time() returns the time since start() was called minus paused time.
		Calling start() mulitple times has no effect if state has not changed.
	"""
	
	def __init__(self):
		self.start_time = time.time()
		self.paused_start = self.start_time
		self.status = "stopped"

	def start(self):
		"""Starts or unpauses the timer"""
		if self.status in ["stopped", "paused"]:
			self.start_time += time.time() - self.paused_start
		self.status = "running"

	def pause(self):
		"""Pauses the timing momentarily until timer.start() is called"""
		self.paused_start = time.time()
		self.status = "paused"

	def stop(self):
		"""Resets the timer"""
		self.start_time = time.time()
		self.paused_start = self.start_time
		self.status = "stopped"

	def get_time(self):
		"""Get the current time since start"""
		if self.status == "running":
			return time.time() - self.start_time
		elif self.status == "paused":
			return self.paused_start - self.start_time
		elif self.status == "stopped":
			return 0
		else:
			raise RuntimeError("A timer object has an invalid timer.status: " + str(self.status) + "\n" +
					"Status must be in [\"running\", \"paused\", \"stopped\"]")


class schedule():

	"""
	   A manager to call a function in a given schedule

	   ACCURATE_MODE means that missed calls will be called later so that on
	                 average the interval is met. This is default
	   REALTIME_MODE means that missed calls will not be executed later
	                 This is useful if you do not care about exact timing but speed.
	"""

	ACCURATE_MODE = 1
	REALTIME_MODE = 2

	def __init__(self, caller, interval, **kwargs):
		"""
		   Initialize a new schedule

		   caller type(func) is the function to be called on schedule
		   interval type(int) the interval between calls in milliseconds

		   **kwargs
		   mode type(str) either schedule.ACCURATE_MODE or schedule.REALTIME_MODE
		   time_authority type(obj) an object responsible for tracking time.
		                  See timer for an example implementation.
		"""
		self.interval = interval
		self.caller = caller

		if "mode" in kwargs:
			if kwargs["mode"] in [schedule.ACCURATE_MODE, schedule.REALTIME_MODE]:
				self.mode = kwargs["mode"]
		else:
			self.mode = schedule.ACCURATE_MODE

		if "time_authority" in kwargs:
			try:
				assert hasattr(kwargs["time_authority"], "start")
				assert hasattr(kwargs["time_authority"], "get_time")
				assert hasattr(kwargs["time_authority"], "pause")
				self.time_authority = kwargs["time_authority"]
			except AssertionError:
				self.time_authority = timer()
		else:
			self.time_authority = timer()

		self.time_authority.start()
		self.last_updated = self.time_authority.get_time()
		self.countdown = interval

	def update(self):
		"""Updates the internal timer and if needed executes the given function"""
		self.countdown -= self.time_authority.get_time() - self.last_updated
		if self.countdown <= 0:
			self.caller()

			if self.mode == schedule.ACCURATE_MODE:
				self.countdown += self.interval
			elif self.mode == schedule.REALTIME_MODE:
				self.countdown = self.interval

		self.last_updated = self.time_authority.get_time()


def init():
	global global_timer

	global_timer = timer()
	global_timer.start()

	physics_scheduler = schedule(lambda: 0, 1)
