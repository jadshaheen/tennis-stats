"""
The `logic` module houses methods for processing scraped data to send back in the API responses.
"""

import re
import scraper

PLAYER_TYPE = "player"
TOURNAMENT_TYPE = "tournament"
YEAR_TYPE = "year"

def retrieve_search_results(search_query):

	input_type = sanitize_input(search_query)
	if input_type == PLAYER_TYPE:
		return PLAYER_TYPE, scraper.construct_players_map()[search_query.lower()]
	elif input_type == TOURNAMENT_TYPE:
		return TOURNEAMENT_TYPE, scraper.construct_tournament_map()[match_tournament(search_query.lower())]
	elif input_type == YEAR_TYPE:
		return YEAR_TYPE, scraper.construct_years_map()[int(search_query)]
	else:
		return "Input not understood. Please try again."


# def get_history_dataset():
# 	return scraper.process_table(
# 		scraper.get_html_data(scraper.HISTORY_SOURCE)
# 	)

# def get_rankings_dataset():
# 	return scraper.process_table(
# 		scraper.get_html_data(scraper.RANKINGS_SOURCE)
# 	)


# method to figure out input type (player name, tournament name or year)
# and normalize the input. Used to determine which logic flow to follow.
def sanitize_input(input):
	if match_tournament(input):
		return TOURNAMENT_TYPE
	elif input.isnumeric():
		return YEAR_TYPE
	# TODO: Figure out case here if not likely player name to return something like,
	# 'input not a recognized player/tournament/year'
	else:
		return PLAYER_TYPE

def match_tournament(tournament_name):
	tournament_patterns_map = {r'u[.]?s[.]? open': 'u.s. open', r'wimbledon': 'wimbledon', r'french open|roland garros': 'french open', r'aus(tralian|sie) open'}
	for pattern in tournament_patterns_map.keys():
		if re.fullmatch(pattern, tournament_name):
			return tournament_patterns_map[pattern]
	return False