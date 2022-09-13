"""
A library module containing custom types for use throughout the repo.
"""

import collections
import dataclasses
import typing as t
from json import JSONEncoder

class Player():
	def __init__(self, name):
		self.name = name
		self.age = None
		self.rank = None
		self.tournaments = dict()

	def asdict(self):
		return {
			'name': self.name,
			'age': self.age,
			'rank': self.rank,
			'tournaments': self.tournaments
		}
	

class PlayerTournament():
	'''
	A representation of the Grand Slam Final results for a particular
	tournament for the player at self.player_name.
	'''
	def __init__(self, name, player_name):
		self.name = name
		self.player_name = player_name
		self.finals_appearances = 0
		self.years_won = list()
		self.years_runner_up = list()

	def asdict(self):
		return {
			'name': self.name,
			'player_name': self.player_name,
			'finals_appearances': self.finals_appearances,
			'years_won': self.years_won,
			'years_runner_up': self.years_runner_up
		}

class TypeEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__

'''
EXAMPLE

fed = Player("Roger Federer", 41, -1, [])
...
wimbledon = Tournament("Wimbledon", 12, [...], [...])
fed.tournaments["Wimbledon"] = wimbledon
'''
