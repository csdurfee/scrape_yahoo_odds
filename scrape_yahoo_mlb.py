from scrape_yahoo import *

import datetime

class ScrapeYahooMLB(ScrapeYahoo):
    LEAGUE = "mlb"

    START_DATE = datetime.datetime(2026, 3, 25)
    END_DATE = datetime.datetime(2026, 6, 12) # yesterday

    def get_yahoo_ids_for_date(self, nice_date):
        """
        fetches date_url and extracts all game ids out of the HTML. expects
        YYYY-MM-DD format for date.
        """
        date_url = self.make_date_url(nice_date)
        date_html = self.scraper.get(date_url).text
        game_ids = set(re.findall(r"mlb\.g\.46[\d]+", date_html))
        return game_ids