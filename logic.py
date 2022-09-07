import scraper

def get_history_dataset():
	return scraper.process_table(
		scraper.get_html_data(scraper.HISTORY_SOURCE)
	)

def get_rankings_dataset():
	return scraper.process_table(
		scraper.get_html_data(scraper.RANKINGS_SOURCE)
	)


