"""
The `scraper` module contains methods for retrieving and parsing HTML data from espn.com
"""

import functools
import requests
from tennis_stats.utils import types

from bs4 import BeautifulSoup
from collections import defaultdict

HISTORY_SOURCE = "http://espn.com/tennis/history"
RANKINGS_SOURCE = "http://espn.com/tennis/rankings"
WOMENS_HISTORY_SUFFIX = "/_/type/women"
WOMENS_RANKING_SUFFIX = "/_/type/wta"

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
	womens_history_html = get_html_data(HISTORY_SOURCE + WOMENS_HISTORY_SUFFIX)
	# The first two rows are headings, so we ignore them.
	history_data = process_table(history_html)[2:]
	history_data += process_table(womens_history_html)[2:]

	rankings_html = get_html_data(RANKINGS_SOURCE)
	womens_rankings_html = get_html_data(RANKINGS_SOURCE + WOMENS_RANKING_SUFFIX)
	rankings_data = process_table(rankings_html)[1:]
	rankings_data += process_table(womens_rankings_html)[1:]

	player_map = dict()

	# TODO: Migrate to logic.py module
	for row in history_data:
		year, tourney, winner, runner = row
		tourney, winner, runner = tourney.lower(), winner.lower(), runner.lower()
		winning_player = player_map.get(winner) or types.Player(winner)
		running_player = player_map.get(runner) or types.Player(runner)
		winning_player = populate_tournament_win(winning_player, year, tourney)
		running_player = populate_tournament_loss(running_player, year, tourney)
		player_map[winner] = winning_player
		player_map[runner] = running_player

	# TODO: Migrate to logic.py module
	# go through rankings data and IF the player already exists in the player_map,
	# populate that players Age and Rank data.
	for row in rankings_data:
		rank, delta, player, points, age = row
		player = player.lower()
		if not player_map.get(player):
			player_map[player] = types.Player(player)
		player_map[player].age = age
		player_map[player].rank = rank

	return player_map


def construct_nested_data_map(outer):
	"""
	Returns a mapping of OUTER data type to a map of INNER data type to (winner, runner-up) tuples.

	The 'outer' parameter can either have the value types.Table.YEAR or types.Table.TOURNAMENT, 
	leaving inner to implicity be the other. This allows us to either get tournament finalist 
	pairs grouped by year, or year finalist pairs grouped by tournament, depending on the table 
	the client has requested.

	if outer is types.Table.YEAR:
		The map is of the form: {YEAR: {TOURNAMENT: (WINNER, RUNNER-UP),...},...}
	if outer is types.Table.TOURNAMENT:
		The map is of the form: {TOURNAMENT: {YEAR: (WINNER, RUNNER-UP),...},...}

	Each row in the data has the structure: [YEAR, TOURNAMENT, WINNER, RUNNER-UP]
	"""
	history_html = get_html_data(HISTORY_SOURCE)
	womens_history_html = get_html_data(HISTORY_SOURCE + WOMENS_HISTORY_SUFFIX)
	# The first two rows are headings, so we ignore them.
	history_data = process_table(history_html)[2:]
	womens_history_data = process_table(womens_history_html)[2:]

	mens_map = defaultdict(dict)
	womens_map = defaultdict(dict)

	for row in history_data:
		year, tourney, winner, runner = row
		if outer == types.Table.YEAR:
			mens_map[year][tourney] = (winner, runner)
		elif outer == types.Table.TOURNAMENT:
			mens_map[tourney][year] = (winner, runner)

	for row in womens_history_data:
		year, tourney, winner, runner = row
		if outer == types.Table.YEAR:
			womens_map[year][tourney] = (winner, runner)
		elif outer == types.Table.TOURNAMENT:
			womens_map[tourney][year] = (winner, runner)

	return mens_map, womens_map


def get_rankings_table():
	"""
	Return the current rankings as a processed table.
	"""
	rankings_html = get_html_data(RANKINGS_SOURCE)
	rankings_data = process_table(rankings_html)
	womens_rankings_html = get_html_data(RANKINGS_SOURCE + WOMENS_RANKING_SUFFIX)
	womens_rankings_data = process_table(womens_rankings_html)

	return rankings_data[1:], womens_rankings_data[1:]


# TODO: Migrate to logic.py module
def populate_tournament_win(player, year, tournament_name):

	if not player.tournaments.get(tournament_name):
		player_tourney = types.PlayerTournament(
			tournament_name,
			player.name,
		)
		player.tournaments[tournament_name] = player_tourney
	tourney = player.tournaments[tournament_name]
	tourney.finals_appearances += 1
	tourney.years_won.append(year)
	tourney = player.tournaments.get(tournament_name)
	player.tournaments[tournament_name] = tourney
	return player


# TODO: Migrate to logic.py module
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





