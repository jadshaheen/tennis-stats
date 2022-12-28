"""
The `logic` module houses methods for processing scraped data to send back in the API responses.
"""

import re
import scraper
from utils.types import Table

def retrieve_search_results(search_query):

	if search_query:
		input_type, sanitized_input = sanitize_input(search_query)
		if input_type == Table.PLAYER:
			return Table.PLAYER.name, scraper.construct_players_map()[sanitized_input]
		elif input_type == Table.TOURNAMENT:
			mens, womens = scraper.construct_nested_data_map(Table.TOURNAMENT)
			return Table.TOURNAMENT.name, mens[match_tournament(sanitized_input)], womens[match_tournament(sanitized_input)]
		elif input_type == Table.YEAR:
			mens, womens = scraper.construct_nested_data_map(Table.YEAR)
			return Table.YEAR.name, mens[sanitized_input], womens[sanitized_input]
		elif input_type == Table.RANKINGS:
			return Table.RANKINGS.name, scraper.get_rankings_table()
	return "Input not understood. Please try again."


# method to figure out input type (player name, tournament name or year)
# and normalize the input. Used to determine which logic flow to follow.
def sanitize_input(input):
	input_type = None
	sanitized_input = input.lower()
	matched_tournament = match_tournament(input)
	if re.fullmatch(r'rank(ing[s]?)?', sanitized_input):
		input_type = Table.RANKINGS
	elif matched_tournament:
		input_type = Table.TOURNAMENT
		sanitized_input = matched_tournament
	elif sanitized_input.isnumeric():
		input_type = Table.YEAR
	# TODO: Figure out case here if not likely player name to return something like,
	# 'input not a recognized player/tournament/year'
	else:
		input_type = Table.PLAYER
	return input_type, sanitized_input

def match_tournament(tournament_name):
	tournament_patterns_map = {r'u[.]?s[.]? open': 'U.S. Open', r'wimbledon': 'Wimbledon', r'french open|roland garros': 'French Open', r'aus(tralian|sie) open': 'Australian Open'}
	for pattern in tournament_patterns_map.keys():
		if re.fullmatch(pattern, tournament_name):
			return tournament_patterns_map[pattern]
	return False