"""
The flask app.
"""

import scraper

from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
	return 'Hello, World!'

def get_history_dataset():
	return scraper.process_table(
		scraper.get_html_data(scraper.HISTORY_SOURCE)
	)

def get_rankings_dataset():
	return scraper.process_table(
		scraper.get_html_data(scraper.RANKINGS_SOURCE)
	)

@app.route('/players')
def get_player_data():
	player_data = scraper.process_players_history(
		get_history_dataset()
	)

	return jsonify({"players": player_data})

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

