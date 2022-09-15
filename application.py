"""
The flask app.

This module creates the application and defines the routes.
"""

import logic
import scraper
from utils import types

import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
	return 'Hello, World!'

@app.route('/search')
def get_search_results():
	search_query =  request.args.to_dict().get('query')
	query_type, search_result = logic.retrieve_search_results(search_query)

	return json.dumps({query_type: search_result}, cls=types.TypeEncoder)

@app.route('/players')
def get_player_data():
	player_name = request.args.to_dict().get('name')
	if not player_name:
		return "ERROR: Pass player name as a query param to retrieve data (eg 'players?name=Roger%20Federer')"

	player_data = scraper.construct_players_map()

	return json.dumps(player_data[player_name.lower()], cls=types.TypeEncoder)
 
@app.route('/tournaments')
def get_tourney_data():
	tourney_data = scraper.construct_tournament_map()

	return jsonify({"tournaments": tourney_data})

@app.route('/years')
def get_years_data():
	years_data = scraper.construct_years_map()

	return jsonify({"years": years_data})

# @app.route('/rankings')
# def get_rankings_data():
# 	return jsonify({"rankings": get_rankings_dataset()})

if __name__ == '__main__':
	app.run(debug=True)
