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
	try:
		player_data = scraper.process_players_history(
			get_history_dataset()
		)

		return jsonify({"players": player_data})
	except Exception as e:
		return e
 
@app.route('/tournaments')
def get_tourney_data():
	try:
		tourney_data = scraper.process_tournament_history(
			get_history_dataset()
		)

		return jsonify({"tournaments": tourney_data})
	except Exception as e:
		return e

@app.route('/years')
def get_years_data():
	try:
		years_data = scraper.process_years_history(
			get_history_dataset()
		)

		return jsonify({"years": years_data})
	except Exception as e:
		return e 

@app.route('/rankings')
def get_rankings_data():
	return jsonify({"rankings": get_rankings_dataset()})

if __name__ == '__main__':
	app.run(debug=True)
