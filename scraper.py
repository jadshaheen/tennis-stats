"""
The `scraper` module contains methods for retrieving and parsing HTML data from espn.com
"""

import functools
import requests
from utils import types

from bs4 import BeautifulSoup
from collections import defaultdict

HISTORY_SOURCE = "http://espn.com/tennis/history"
RANKINGS_SOURCE = "http://espn.com/tennis/rankings"

@functools.lru_cache(maxsize=2)
def get_html_data(url):
	"""Retrieves the HTML data of the webpage at the supplied URL."""
	html = requests.get(url)
	return html.content

def process_table(webpage):
	"""Processes an HTML table from a webpage into a 2D array of rows and columns."""
	data = []
	soup = BeautifulSoup(webpage, 'html.parser')
	table = soup.find('table')
	rows = table.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		data.append([col.text for col in cols])
	return data

# @functools.lru_cache(maxsize=1)
def construct_players_map():
	"""
	Returns a mapping of player name to a types.Player object, which stores rank and tournament result information.

	The map is of the form: {"playername": types.Player}

	Each row in the history data has the structure: [YEAR, TOURNAMENT, WINNER, RUNNER-UP]
	Each row in the rankings data has the structure: [RANK, DELTA, PLAYER, POINTS, AGE]
	"""
	history_html = get_html_data(HISTORY_SOURCE)
	history_data = process_table(history_html)

	rankings_html = get_html_data(RANKINGS_SOURCE)
	rankings_data = process_table(rankings_html)

	player_map = defaultdict(lambda: types.Player())

	# The first two rows are headings, so we ignore them.
	for row in history_data[2:]:
		year, tourney, winner, runner = row
		winning_player = player_map[winner]
		running_player = player_map[runner]
		winning_player.name = winner
		running_player.name = runner
		winning_player = populate_tournament_win(winning_player, year, tourney)
		running_player = populate_tournament_loss(running_player, year, tourney)

	# go through rankings data and IF the player already exists in the player_map,
	# populate that players Age and Rank data.

	return player_map

def construct_tournament_map():
	"""
	Returns a mapping of tournmaent to a map of years to (winner, runner-up) tuples.

	The map is of the form: {TOURNAMENT: {YEAR: (WINNER, RUNNER-UP),...},...}

	Each row in the data has the structure: [YEAR, TOURNAMENT, WINNER, RUNNER-UP]
	"""
	webpage_html = get_html_data(HISTORY_SOURCE)
	data = process_table(webpage_html)

	tourney_map = defaultdict(dict)

	# The first two rows are headings, so we ignore them.
	for row in data[2:]:
		year, tourney, winner, runner = row
		tourney_map[tourney][year] = (winner, runner)

	return tourney_map

def construct_years_map():
	"""
	Returns a mapping of year to a map of tourneys to (winner, runner-up) tuples.

	The map is of the form: {YEAR: {TOURNAMENT: (WINNER, RUNNER-UP),...},...}

	Each row in the data has the structure: [YEAR, TOURNAMENT, WINNER, RUNNER-UP]
	"""
	webpage_html = get_html_data(HISTORY_SOURCE)
	data = process_table(webpage_html)

	year_map = defaultdict(dict)

	# The first two rows are headings, so we ignore them.
	for row in data[2:]:
		year, tourney, winner, runner = row
		year_map[year][tourney] = (winner, runner)

	return year_map

def populate_tournament_win(player, year, tournament_name):

	if not player.tournaments.get(tournament_name):
		player_tourney = types.PlayerTournament(
			tournament_name,
			player.name,
		)
		player.tournaments[tournament_name] = player_tourney
	tourney = player.tournaments.get(tournament_name)
	tourney.finals_appearances += 1
	tourney.years_won.append(year)
	return tourney

def populate_tournament_loss(player, year, tournament_name):

	if not player.tournaments.get(tournament_name):
		player_tourney = types.PlayerTournament(
			tournament_name,
			player.name,
		)
		player.tournaments[tournament_name] = player_tourney
	tourney = player.tournaments.get(tournament_name)
	tourney.finals_appearances += 1
	tourney.years_runner_up.append(year)
	return player


def main():
	players_data = construct_players_map()
	tournament_data = construct_tournament_map()
	years_data = construct_years_map()
	print("Rafael Nadal French Open Wins: " + str(sum([len(fr["wins"]) for tourney, fr in players_data["Rafael Nadal"].items() if tourney == "French Open"])))
	return players_data, tournament_data, years_data

if __name__ == "__main__":
	main()





