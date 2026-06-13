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
        date_html = self.get_scraper().get(date_url).text
        game_ids = set(re.findall(r"mlb\.g\.4[\d]+", date_html))
        return game_ids
    

if __name__ == '__main__':
    # TODO: this is hacky, remove
    START_CHUNK =  datetime.datetime(2026, 5, 16)
    END_CHUNK = datetime.datetime(2026, 6, 12)

    scraper = ScrapeYahooMLB()
    scraper.fetch_yahoo_data(fetch_dir="mlb_scrapes/2026",
                             start=START_CHUNK, 
                             end=END_CHUNK)