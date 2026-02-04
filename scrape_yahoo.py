"""
Scrapes NBA betting line data from Yahoo's internal API.

This fetches all NBA games from the 2021-22 thru 2024-25 seasons (all the data Yahoo has)
By default, this contains all regular season and playoff games, and the Emirates NBA Cup
championship game (which doesn't count as either).

The rules for extracting each field are found in the `scrape_rules.py` file.

"""

import datetime
import glob
import json
import os
import re
import time

import pandas as pd

import cloudscraper
# cloudscraper can get around some basic anti-bot detection vs using requests library.
# I didn't encounter any errors or rate limiting when scraping the data at a very slow rate, though,
# so this may be an unneeded dependency.
#
# I did encounter problems using playwright to scrape yahoo (the first request 
# would go through fine, subsequent ones would time out) but was able to figure out
# how to get the data without a headless browser by using the backend url in `make_json_yahoo_url`

from jsonpath_ng.ext import parse

import scrape_rules


class ScrapeYahoo:
    START_DATE = datetime.datetime(2024, 10, 22) # start of 2024-25 regular season
    END_DATE = datetime.datetime(2025, 4, 13) # end of 2024-25 regular season

    SEASONS = {
        '2021': (datetime.datetime(2021, 10, 19), datetime.datetime(2022, 6, 16)),
        '2022': (datetime.datetime(2022, 10, 18), datetime.datetime(2023, 6, 12)),
        '2023': (datetime.datetime(2023, 10, 24), datetime.datetime(2024, 6, 17)),
        '2024': (datetime.datetime(2024, 10, 22), datetime.datetime(2025, 6, 22)),
    }

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.cache_dir = 'yahoo_scrapes/2024'

    def make_yahoo_json_url(self, game_id):
        return f"https://sports.yahoo.com/site/api/resource/sports.graphite.gameOdds;dataType=graphite;endpoint=graphite;gameIds={game_id}"

    def get_some_json(self, url):
        scraper = cloudscraper.create_scraper()
        some_html = scraper.get(url).text
        parsed = json.loads(some_html)
        return parsed

    def make_date_url(self, yyyy_mm_dd):
        """
        This is the URL for the Yahoo page that shows all NBA scores for a particular date.
        """
        return f"https://sports.yahoo.com/nba/scoreboard/?confId=&dateRange={yyyy_mm_dd}"

    def get_yahoo_ids_for_date(self, nice_date):
        """
        fetches date_url and extracts all game ids out of the HTML. expects
        YYYY-MM-DD format for date.
        """
        date_url = self.make_date_url(nice_date)
        date_html = self.scraper.get(date_url).text
        game_ids = set(re.findall(r"nba\.g\.202[\d]+", date_html))
        return game_ids

    def fetch_yahoo_data(self, dir="yahoo_scrapes/2024", start=START_DATE, end=END_DATE):
        """
        fetches all data from `start` to `end` and saves them as JSON in the `dir` directory.
        """
        date_range = pd.date_range(start, end).strftime("%Y-%m-%d")

        # for each date, get the game ids for that day
        for date in date_range:
            print(f"STARTING {date}")
            yahoo_ids = self.get_yahoo_ids_for_date(date)
            time.sleep(2) # be polite
            
            # for each game id, fetch and save the game data if we don't already have it
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
                        # this condition happened 3 times in the course of scraping all 
                        # 4 seasons. I didn't investigate why, and rerunning those days
                        # was successful.
                        print(f"failed on {game_url}")
                        # I'm not sure if it's hitting rate limits or what, but might as well
                        # take a little break.
                        time.sleep(10)
                    time.sleep(2) # be polite

            print(f"DONE WITH {date}")

    def preparse_rules(self):
        """
        turning the JSONPath expression into a function is costly, so it is
        important to cache it.
        """
        parsed = {}
        for k, v in scrape_rules.RULES.items():
            jsonpath_expression = parse(v)
            parsed[k] = jsonpath_expression
        return parsed

    def parse_yahoo_data(self, json_data, filename='', parsed_rules=None):
        """
        takes json data from a single game and parses it
        """
        row = {}
        if not parsed_rules:
            parsed_rules = self.preparse_rules()

        for k, jsonpath_expression in parsed_rules.items():
            try:
                results = [item.value for item in jsonpath_expression.find(json_data)][0]
                row[k] = results
            except:
                print(f"file: {filename} failed on {jsonpath_expression}")
        return row

    def get_cached_filenames(self, cache_dir):
        """
        returns all filenames in a particular cache dir.
        """
        return list(glob.glob(f"{cache_dir}/*.json"))

    def make_dataframe(self, json_filenames):
        """
        For each file in json_filenames, it parses the raw JSON data and applies scrape_rules, then returns
        a pandas dataframe.
        """
        dataframes = []
        parsed_data = None
        parsed_rules = self.preparse_rules()

        for filename in json_filenames:
            with open(filename, 'r') as f:
                json_data = json.load(f)
            parsed_data = self.parse_yahoo_data(json_data, filename, parsed_rules)
            if parsed_data: # skip if bad/no data from this file
                dataframes.append(pd.DataFrame({k:[v] for k,v in parsed_data.items()}))

        return pd.concat(dataframes)

    def load_summary_csv(self):
        dataframes = []
        for year in self.SEASONS.keys():
            df = pd.read_csv(f"yahoo_scrapes/{year}/odds.csv")
            dataframes.append(df.set_index('game_id'))
        return pd.concat(dataframes)

    def scrape_pages(self):
        for (season_name, season_range) in self.SEASONS.items():
            base_dir = f"yahoo_scrapes/{season_name}"
            self.fetch_yahoo_data(base_dir, season_range[0], season_range[1])      


    def rebuild_summary_csv(self):
        """
        Re-generate data year by year, and save each year as a CSV file.
        """
        all_years = []
        for year in self.SEASONS.keys():
            print(f"doing {year}")
            _start = time.time()

            base_dir = f"yahoo_scrapes/{year}"

            filenames = self.get_cached_filenames(base_dir)
            df = self.make_dataframe(filenames)
            df.to_csv(f"{base_dir}/odds.csv")

            all_years.append(df.copy())

            print(f"took {time.time() - _start}")# in practice, about 2 seconds per game

    def get_all_data(self):
        dataframes = []
        for year in self.SEASONS.keys():
            filenames = self.get_cached_filenames(f"nfl_scrapes/{year}")
            df = self.make_dataframe(filenames)
            df['season'] = year
            dataframes.append(df)

        return pd.concat(dataframes)