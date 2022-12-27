"""
The `logic` module houses methods for processing scraped data to send back in the API responses.
"""

import re
import scraper
from utils.types import Table

def retrieve_search_results(search_query):

	if search_query:
		input_type = sanitize_input(search_query.lower())
		if Table(input_type) == Table.PLAYER:
			return Table.PLAYER.name, scraper.construct_players_map()[search_query.lower()]
		elif Table(input_type) == Table.TOURNAMENT:
			return Table.TOURNAMENT.name, scraper.construct_nested_data_map(Table.TOURNAMENT)[match_tournament(search_query.lower())]
		elif Table(input_type) == Table.YEAR:
			return Table.YEAR.name, scraper.construct_years_map(Table.YEAR)[search_query]
		elif Table(input_type) == Table.RANKINGS:
			return Table.RANKINGS.name, scraper.get_rankings_table()
	return "Input not understood. Please try again."


# method to figure out input type (player name, tournament name or year)
# and normalize the input. Used to determine which logic flow to follow.
def sanitize_input(input):
	if re.fullmatch(r'rank(ing[s]?)?', input):
		return RANKINGS_TYPE
	elif match_tournament(input):
		return TOURNAMENT_TYPE
	elif input.isnumeric():
		return YEAR_TYPE
	# TODO: Figure out case here if not likely player name to return something like,
	# 'input not a recognized player/tournament/year'
	else:
		return PLAYER_TYPE

def match_tournament(tournament_name):
	print("\nSTARTING TOURNAMENT STRING MATCH")
	tournament_patterns_map = {r'u[.]?s[.]? open': 'U.S. Open', r'wimbledon': 'Wimbledon', r'french open|roland garros': 'French Open', r'aus(tralian|sie) open': 'Australian Open'}
	for pattern in tournament_patterns_map.keys():
		if re.fullmatch(pattern, tournament_name):
			print("\nMATCH FOUND!")
			print(tournament_patterns_map[pattern])
			return tournament_patterns_map[pattern]
	return False