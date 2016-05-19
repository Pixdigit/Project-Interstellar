# -*- coding: utf-8 -*-

import READ_BEFORE_START
permission = READ_BEFORE_START.allow_data_collection
if permission not in [1, -1]:
	print(("Please read the READ_BEFORE_START.py"))
	print(("It can be opend by any normal text editor."))
	raw_input()
	exit()
if permission == 1:
	print(("Thank you for helping us making this less buggy."))
if permission == -1:
	print(("Error reporting disabled :("))


if permission == 1:
	try:
		import telegram
	except:
		print(("Telegram not installed. Errors can not be reported."))
		raw_input()


def send(message):
	if "telegram" in globals():
		import data as get_data
		bot = telegram.Bot(token=get_data.token)
		bot.sendMessage(chat_id=158887423, text=message)
	else:
		pass
#TODO: deliver with api preinstalled