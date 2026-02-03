from scrape_yahoo import *

class ScrapeYahooNFL(ScrapeYahoo):
    SEASONS = {
        '2021': None,
        '2022': None,
        '2023': None,
        '2024': None,
        '2025': None
    }


    def make_date_url(week, year):
        return f"https://sports.yahoo.com/nfl/scoreboard/?confId=&dateRange={week}&schedState=2&scoreboardSeason={year}"

    def get_yahoo_ids_for_date(self, week, year):
        """
        NFL VERSION

        fetches date_url and extracts all game ids out of the HTML. takes week and year as args
        """
        date_url = self.make_date_url(week, year)
        date_html = self.scraper.get(date_url).text
        game_ids1 = set(re.findall(f"nfl\.g\.{year}[\d]+", date_html))
        ## some games take place in the next calendar year
        game_ids2 = set(re.findall(f"nfl\.g\.{year + 1}[\d]+", date_html))

        return game_ids1.union(game_ids2)


    def fetch_yahoo_data(self, dir, year):
        """
        NFL version

        fetches all data from `start` to `end` and saves them as JSON in the `dir` directory.

        TODO: need to refactor this
        """
        for week in range(1, 19):
            yahoo_ids = self.get_yahoo_ids_for_date(week, year)
            time.sleep(2)

            for yahoo_game_id in yahoo_ids:
                cache_path = f"{dir}/{yahoo_game_id}.json"
                if not os.path.exists(cache_path):
                    game_url = self.make_yahoo_json_url(yahoo_game_id)
                    #print(f"fetching url {game_url}")
                    try:
                        game_json = self.get_some_json(game_url)

                        with open(cache_path, "w") as f:
                            json.dump(game_json, f)
                    except:
                        print(f"failed on {game_url}")
                        # I'm not sure if it's hitting rate limits or what, but might as well
                        # take a little break.
                        time.sleep(10)
                    time.sleep(1) # be polite

            print(f"DONE WITH week {week}")
