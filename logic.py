"""
The `logic` module houses methods for processing scraped data to send back in the API responses.
"""

import re
import scraper
from utils.types import Table

def retrieve_search_results(search_query):

	if search_query:
		input_type = sanitize_input(search_query.lower())
		if input_type == Table.PLAYER:
			return Table.PLAYER.name, scraper.construct_players_map()[search_query.lower()]
		elif input_type == Table.TOURNAMENT:
			mens, womens = scraper.construct_nested_data_map(Table.TOURNAMENT)
			return Table.TOURNAMENT.name, mens[match_tournament(search_query.lower())], womens[match_tournament(search_query.lower())]
		elif input_type == Table.YEAR:
			mens, womens = scraper.construct_nested_data_map(Table.YEAR)
			return Table.YEAR.name, mens[search_query], womens[search_query]
		elif input_type == Table.RANKINGS:
			return Table.RANKINGS.name, scraper.get_rankings_table()
	return "Input not understood. Please try again."


# method to figure out input type (player name, tournament name or year)
# and normalize the input. Used to determine which logic flow to follow.
def sanitize_input(input):
	if re.fullmatch(r'rank(ing[s]?)?', input):
		return Table.RANKINGS
	elif match_tournament(input):
		return Table.TOURNAMENT
	elif input.isnumeric():
		return Table.YEAR
	# TODO: Figure out case here if not likely player name to return something like,
	# 'input not a recognized player/tournament/year'
	else:
		return Table.PLAYER

def match_tournament(tournament_name):
	tournament_patterns_map = {r'u[.]?s[.]? open': 'U.S. Open', r'wimbledon': 'Wimbledon', r'french open|roland garros': 'French Open', r'aus(tralian|sie) open': 'Australian Open'}
	for pattern in tournament_patterns_map.keys():
		if re.fullmatch(pattern, tournament_name):
			print(tournament_patterns_map[pattern])
			return tournament_patterns_map[pattern]
	return False