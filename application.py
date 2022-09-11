"""
The flask app.

This module creates the application and defines the routes.
"""

import scraper

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
	return 'Hello, World!'

@app.route('/players')
def get_player_data():
	player_name = request.args
	player_data = scraper.construct_players_map()

	return jsonify({player_name}: player_data[player_name])
 
@app.route('/tournaments')
def get_tourney_data():
	tourney_data = scraper.process_tournament_history(
		get_history_dataset()
	)

	return jsonify({"tournaments": tourney_data})

@app.route('/years')
def get_years_data():
	years_data = scraper.process_years_history(
		get_history_dataset()
	)

	return jsonify({"years": years_data})

@app.route('/rankings')
def get_rankings_data():
	return jsonify({"rankings": get_rankings_dataset()})

if __name__ == '__main__':
	app.run(debug=True)
