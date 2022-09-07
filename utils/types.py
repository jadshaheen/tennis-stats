"""
A library module containing custom types for use throughout the repo.
"""

import collections
import dataclasses
import typing as t

class Player(t.NamedTuple):
	name: str
	age: int
	rank: int
	tournaments: map(str, Tournament)
	

class Tournament(t.NamedTuple)
	name: str
	finals_appearances: int
	years_won: list(int)
	years_runner_up: list(int)

'''
EXAMPLE

fed = Player("Roger Federer", 41, -1, [])
...
wimbledon = Tournament("Wimbledon", 12, [...], [...])
fed.tournaments["Wimbledon"] = wimbledon
'''
