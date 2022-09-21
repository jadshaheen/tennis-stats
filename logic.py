"""
The `logic` module houses methods for processing scraped data to send back in the API responses.
"""

import re
import scraper

PLAYER_TYPE = "player"
TOURNAMENT_TYPE = "tournament"
YEAR_TYPE = "year"
RANKINGS_TYPE = "rankings"

def retrieve_search_results(search_query):

	input_type = sanitize_input(search_query.lower())
	if input_type == PLAYER_TYPE:
		return PLAYER_TYPE, scraper.construct_players_map()[search_query.lower()]
	elif input_type == TOURNAMENT_TYPE:
		return TOURNAMENT_TYPE, scraper.construct_tournament_map()[match_tournament(search_query.lower())]
	elif input_type == YEAR_TYPE:
		return YEAR_TYPE, scraper.construct_years_map()[search_query]
	elif input_type == RANKINGS_TYPE:
		return RANKINGS_TYPE, scraper.get_rankings_table()
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