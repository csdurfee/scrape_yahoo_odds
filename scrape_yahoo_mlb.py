from scrape_yahoo import *

import datetime

class ScrapeYahooMLB(ScrapeYahoo):
    BASE_DIR = "mlb_scrapes"
    LEAGUE = "mlb"

    START_DATE = datetime.datetime(2026, 3, 25)
    END_DATE = datetime.datetime(2026, 6, 12) # yesterday

    SEASONS = {
        '2026': (datetime.datetime(2026, 3, 25), datetime.datetime(2026, 6, 12)), 
    }


    def get_yahoo_ids_for_date(self, nice_date):
        """
        fetches date_url and extracts all game ids out of the HTML. expects
        YYYY-MM-DD format for date.
        """
        date_url = self.make_date_url(nice_date)
        date_html = self.get_scraper().get(date_url).text
        game_ids = set(re.findall(r"mlb\.g\.4[\d]+", date_html))
        return game_ids
    
    def log_parse_error(self, filename, jsonpath_expression):
        # suppress logging any parsing errors.. they are a lot due to lack of data
        # for most MLB games before a certain point.
        ...

if __name__ == '__main__':
    # hacky manual fetching
    # START_CHUNK =  datetime.datetime(2026, 3, 25)
    # END_CHUNK = datetime.datetime(2026, 6, 12)

    # scraper = ScrapeYahooMLB()
    # scraper.fetch_yahoo_data(fetch_dir="mlb_scrapes/2026",
    #                          start=START_CHUNK, 
    #                          end=END_CHUNK)

    # I don't think there's any useful data in previous seasons, but 
    # it's worth a shot.

    START_CHUNK =  datetime.datetime(2025, 6, 10)
    END_CHUNK = datetime.datetime(2025, 6, 12)

    scraper = ScrapeYahooMLB()
    scraper.fetch_yahoo_data(fetch_dir="mlb_scrapes/2025",
                             start=START_CHUNK, 
                             end=END_CHUNK) 