"""
A library module containing custom types for use throughout the repo.
"""

import collections
import dataclasses
import typing as t

class Player:
	def __init__(self):
		self.name = None
		self.age = None
		self.rank = None
		self.tournaments = dict()
	

class PlayerTournament:
	'''
	A representation of the Grand Slam Final results for a particular
	tournament for the player at self.player_name.
	'''
	def __init__(self, name, player_name):
		self.name = name
		self.player_name = player_name
		self.finals_appearnaces = 0
		self.years_won = list()
		self.years_runner_up = list()

'''
EXAMPLE

fed = Player("Roger Federer", 41, -1, [])
...
wimbledon = Tournament("Wimbledon", 12, [...], [...])
fed.tournaments["Wimbledon"] = wimbledon
'''
