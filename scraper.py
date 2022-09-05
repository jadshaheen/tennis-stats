"""
The `scraper` module contains methods for retrieving and parsing HTML data from espn.com
"""

import functools
import requests

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
def process_players_history(data):
	"""
	Returns a mapping of player name to grand slam year and result data for slams
	in which the player appeared in a final.

	The map is of the form: {PLAYER: {TOURNAMENT: {"wins": [YEAR,...], "runner-ups": [YEAR,...]},...},...}

	Each row in the data has the structure: [YEAR, TOURNAMENT, WINNER, RUNNER-UP]
	"""
	player_map = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

	# The first two rows are headings, so we ignore them.
	for row in data[2:]:
		year, tourney, winner, runner = row
		player_map[winner][tourney]["wins"].append(year)
		player_map[runner][tourney]["runner-ups"].append(year)

	return player_map

def process_tournament_history(data):
	"""
	Returns a mapping of tournmaent to a map of years to (winner, runner-up) tuples.

	The map is of the form: {TOURNAMENT: {YEAR: (WINNER, RUNNER-UP),...},...}

	Each row in the data has the structure: [YEAR, TOURNAMENT, WINNER, RUNNER-UP]
	"""
	tourney_map = defaultdict(dict)

	# The first two rows are headings, so we ignore them.
	for row in data[2:]:
		year, tourney, winner, runner = row
		tourney_map[tourney][year] = (winner, runner)

	return tourney_map

def process_years_history(data):
	"""
	Returns a mapping of year to a map of tourneys to (winner, runner-up) tuples.

	The map is of the form: {YEAR: {TOURNAMENT: (WINNER, RUNNER-UP),...},...}

	Each row in the data has the structure: [YEAR, TOURNAMENT, WINNER, RUNNER-UP]
	"""
	year_map = defaultdict(dict)

	# The first two rows are headings, so we ignore them.
	for row in data[2:]:
		year, tourney, winner, runner = row
		year_map[year][tourney] = (winner, runner)

	return year_map

def main():
	webpage = get_html_data(HISTORY_SOURCE)
	table = process_table(webpage)
	players_data = process_players_history(table)
	tournament_data = process_tournament_history(table)
	years_data = process_years_history(table)
	print("Rafael Nadal French Open Wins: " + str(sum([len(fr["wins"]) for tourney, fr in players_data["Rafael Nadal"].items() if tourney == "French Open"])))
	return players_data, tournament_data, years_data

if __name__ == "__main__":
	main()





