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

SEASONS = {
    '2021': (datetime.datetime(2021, 10, 19), datetime.datetime(2022, 6, 16)),
    '2022': (datetime.datetime(2022, 10, 18), datetime.datetime(2023, 6, 12)),
    '2023': (datetime.datetime(2023, 10, 24), datetime.datetime(2024, 6, 17)),
    '2024': (datetime.datetime(2024, 10, 22), datetime.datetime(2025, 6, 22)),
}

# games with teams not on this list (like all-star games) are ignored
TEAMS = {
 'Atlanta',
 'Boston',
 'Brooklyn',
 'Charlotte',
 'Chicago',
 'Cleveland',
 'Dallas',
 'Denver',
 'Detroit',
 'Golden State',
 'Houston',
 'Indiana',
 'LA Clippers',
 'LA Lakers',
 'Memphis',
 'Miami',
 'Milwaukee',
 'Minnesota',
 'New Orleans',
 'New York',
 'Oklahoma City',
 'Orlando',
 'Philadelphia',
 'Phoenix',
 'Portland',
 'Sacramento',
 'San Antonio',
 'Toronto',
 'Utah',
 'Washington'
}

START_DATE = datetime.datetime(2024, 10, 22) # start of 2024-25 regular season
END_DATE = datetime.datetime(2025, 4, 13) # end of 2024-25 regular season

def make_yahoo_json_url(game_id):
    return f"https://sports.yahoo.com/site/api/resource/sports.graphite.gameOdds;dataType=graphite;endpoint=graphite;gameIds={game_id}"

def get_some_json(url):
    scraper = cloudscraper.create_scraper()
    some_html = scraper.get(url).text
    parsed = json.loads(some_html)
    return parsed

def make_date_url(nice_date):
    """
    This is the URL for the Yahoo page that shows all NBA scores for a particular date.
    """
    return f"https://sports.yahoo.com/nba/scoreboard/?confId=&dateRange={nice_date}"

def get_yahoo_ids_for_date(nice_date):
    """
    fetches date_url and extracts all game ids out of the HTML. expects
    YYYY-MM-DD format for date.
    """
    scraper = cloudscraper.create_scraper()
    date_url = make_date_url(nice_date)
    date_html = scraper.get(date_url).text
    game_ids = set(re.findall(r"nba\.g\.202[\d]+", date_html))
    return game_ids


def fetch_yahoo_data(dir="yahoo_scrapes/2024", start=START_DATE, end=END_DATE):
    """
    fetches all data from `start` to `end` and saves them as JSON in the `dir` directory.
    """
    date_range = pd.date_range(start, end).strftime("%Y-%m-%d")

    # for each date, get the game ids for that day
    for date in date_range:
        print(f"STARTING {date}")
        yahoo_ids = get_yahoo_ids_for_date(date)
        time.sleep(2) # be polite
        
        # for each game id, fetch and save the game data if we don't already have it
        for yahoo_game_id in yahoo_ids:
            cache_path = f"{dir}/{yahoo_game_id}.json"
            if not os.path.exists(cache_path):
                game_url = make_yahoo_json_url(yahoo_game_id)
                #print(f"fetching url {game_url}")
                try:
                    game_json = get_some_json(game_url)

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

def parse_yahoo_data(json_data, filename=''):
    """
    takes json data from a single game and parses it with the rules in scrape_rules.RULES.

    it returns None for postponed/non-completed games, and games with unrecognized teams (all star games)
    """
    row = {}
    for k,v in scrape_rules.RULES.items():
        jsonpath_expression = parse(v)
        try:
            results = [item.value for item in jsonpath_expression.find(json_data)][0]
            row[k] = results
        except:
            print(f"file: {filename} failed on {jsonpath_expression}")

    if row['home_team'] not in TEAMS:
        print(f"skipping game between {row['home_team']} and {row['away_team']}")
        return None

    if ('total_over_won' in row) and (row['total_over_won'] or row['total_under_won']):
        return row
    else:
        return None # nobody won (postponed game) or yahoo missing data

def get_cached_filenames(cache_dir='yahoo_scrapes/2024'):
    """
    returns all filenames in a particular cache dir.
    """
    return list(glob.glob(f"{cache_dir}/*.json"))

def make_dataframe(json_filenames):
    dataframes = []
    #df = pd.DataFrame(columns=DATAFRAME_CONF.keys())
    parsed_data = None
    for filename in json_filenames:
        with open(filename, 'r') as f:
            json_data = json.load(f)
        parsed_data = parse_yahoo_data(json_data, filename)
        if parsed_data: # skip if bad/no data from this file
            dataframes.append(pd.DataFrame({k:[v] for k,v in parsed_data.items()}))

    return pd.concat(dataframes)

def numericize(df):
    """
    Converts columns that should be numeric/boolean
    """
    points = df.columns[df.columns.str.contains('points')]
    percentages = df.columns[df.columns.str.contains('percentage')]
    to_numeric = list(points) + list(percentages)
    df[to_numeric] = df[to_numeric].apply(pd.to_numeric)

    # this is a wacky thing with pandas I just discovered
    # if a Series is an object datatype but contains boolean values,
    # eldritch horrors emerge if you do a ~ on it, 
    # eg ~(pd.Series([True, False, True, False]).astype(object))
    to_bools = df.columns[df.columns.str.contains('won')]
    for col in to_bools:
        df[col] = df[col].astype(bool)

    return df

def add_spread_columns(df):
    """
    adds additional columns related to betting against the spread
    from calculated results not in the original yahoo API
    """
    ## convert fields that need to be numeric
    df = numericize(df)

    ## parse the date as actual datetime
    df['game_date'] = pd.to_datetime(df['game_date'])

    ## was the HOME or AWAY team the underdog against the spread?
    df['spread_dog'] = None
    # away underdogs
    df.loc[df.spread_away_points > 0, 'spread_dog'] = 'AWAY'
    # away favorites => home underdogs
    df.loc[df.spread_away_points < 0, 'spread_dog'] = 'HOME'

    ## did the HOME or AWAY team win against the spread?
    df['spread_winner'] = None
    df.loc[df.spread_away_won==True, 'spread_winner'] = "AWAY"
    df.loc[df.spread_away_won==False, 'spread_winner'] = "HOME"

    ## did the underdog win against the spread? T/F
    df['spread_dog_won'] = False
    # home dogs that won ATS
    df.loc[(df.spread_dog == 'HOME') & (df.spread_winner == 'HOME'), 'spread_dog_won'] = True
    # away dogs that won ATS
    df.loc[(df.spread_dog == 'AWAY') & (df.spread_winner == 'AWAY'), 'spread_dog_won'] = True

    ## which team got more bets placed on them, HOME or AWAY?
    df['spread_most_popular'] = None
    df.loc[df.spread_away_wager_percentage >= 50, 'spread_most_popular'] = 'AWAY'
    df.loc[df.spread_away_wager_percentage < 50, 'spread_most_popular'] = 'HOME'

    ## did the most popular team (by wager percentage) win against the spread?
    df['spread_popular_won'] = False
    df.loc[df.spread_most_popular == df.spread_winner, 'spread_popular_won'] = True

    ## when was the underdog against the spread the most popular team with bettors?
    df['spread_popular_underdog'] = False
    df.loc[df.spread_most_popular == df.spread_dog, 'spread_popular_underdog'] = True

    ## sometimes wager_percentage and stake_percentage are significantly different.
    ## might as well do the above for stake as well.
    df['spread_stake_popular'] = None
    df.loc[df.spread_away_stake_percentage >= 50, 'spread_stake_popular'] = 'AWAY'
    df.loc[df.spread_away_stake_percentage < 50, 'spread_stake_popular'] = 'HOME'

    ## did the most popular team (by wager percentage) win against the spread?
    df['spread_stake_won'] = False
    df.loc[df.spread_stake_popular == df.spread_winner, 'spread_stake_won'] = True

    ## when was the underdog against the spread the most popular team with bettors?
    df['spread_stake_underdog'] = False
    df.loc[df.spread_stake_popular == df.spread_dog, 'spread_stake_underdog'] = True

    ## add team names for various conditions

    ## spread favorite/underdog team name
    df['spread_favorite_team_name'] = None
    df['spread_dog_team_name'] = None
    # home favorites

    # the home team was the favorite on the line, so should be `spread_favorite_team_name`
    home_favorites = (df.spread_dog == "AWAY")
    df.loc[home_favorites, "spread_favorite_team_name"] = df.loc[home_favorites, "home_team"]
    df.loc[home_favorites, "spread_dog_team_name"] = df.loc[home_favorites, "away_team"]

    # away team was the favorited
    away_favorites = (df.spread_dog == "HOME")
    df.loc[away_favorites, "spread_favorite_team_name"] = df.loc[away_favorites, "away_team"]
    df.loc[away_favorites, "spread_dog_team_name"] = df.loc[away_favorites, "home_team"]

    # spread winner/loser team names
    df['spread_winner_team_name'] = None
    df['spread_loser_team_name']  = None

    spread_home_winners = (df.spread_home_won == True)
    spread_home_losers = (df.spread_home_won == False)

    df.loc[spread_home_winners, 'spread_winner_team_name'] = df.loc[spread_home_winners, 'home_team']
    df.loc[spread_home_winners, 'spread_loser_team_name'] = df.loc[spread_home_winners, 'away_team']


    df.loc[spread_home_losers, 'spread_winner_team_name'] = df.loc[spread_home_losers, 'away_team']
    df.loc[spread_home_losers, 'spread_loser_team_name'] = df.loc[spread_home_losers, 'home_team']

    # popular teams by name
    df['spread_popular_team_name'] = None
    popular_home = (df.spread_most_popular == "HOME")

    df.loc[popular_home, 'spread_popular_team_name'] = df.loc[popular_home, 'home_team']
    df.loc[~popular_home, 'spread_popular_team_name'] = df.loc[~popular_home, 'away_team']

    return df

def convert_line(line):
    """
    convert American style money line to the implied probability

    -400 implies you will win 4 out of 5 bets
    >>> convert_line(-400)
    0.8
    """
    if line < 0:
        return abs(line)/(abs(line)+100)
    else:
        return 100/(100+line)
    
def payout(line):
    """
    calculates amount of profit from taking an American style money line (risking $100)
    
    the 2 times you win a -200 bet covers the 1 time you lose it, so payout should be $50.0
    >>> payout(-200)
    50.0

    a +300 bet should payout $300
    >>> payout(300)
    300.0
    """
    return (100/convert_line(line)) - 100

def add_money_columns(df):
    """
    adds more data about money line bets. 


    """
    # drop any games that are ties or don't have money line wager percentage data.
    df = df.dropna(subset=['money_home_won', 'money_home_odds', 'money_away_odds',
                            'money_home_wager_percentage'])
    
    # money line fields
    # was home or away more popular with gamblers?
    df['money_popular'] = None
    df.loc[df.money_home_wager_percentage > 50, 'money_popular'] = 'HOME'
    df.loc[df.money_home_wager_percentage <= 50, 'money_popular'] = 'AWAY'

    # did the popular side of the money line bet win?
    df['money_popular_won'] = False
    df.loc[(df.money_popular == 'HOME') & (df.money_home_won), 'money_popular_won'] = True
    df.loc[(df.money_popular == 'AWAY') & (df.money_away_won), 'money_popular_won'] = True

    # did the public back the favorite or the dog on the money line?
    df['money_fave_dog'] = 'DOG'
    # the public backed a home favorite
    df.loc[(df.money_popular == 'HOME') & (df.money_home_odds < 0), 'money_fave_dog'] = 'FAVE'
    # the public backed an away favorite
    df.loc[(df.money_popular == 'AWAY') & (df.money_away_odds < 0), 'money_fave_dog'] = 'FAVE'

    # what were the odds taken by the more popular side?
    df['money_popular_odds']  = None
    df.loc[(df.money_popular == 'HOME'), 'money_popular_odds'] = df.loc[(df.money_popular == 'HOME'), 'money_home_odds']
    df.loc[(df.money_popular == 'AWAY'), 'money_popular_odds'] = df.loc[(df.money_popular == 'AWAY'), 'money_away_odds']

    # what is the overround (profit margin for sportsbook)?
    df['money_overround'] = df.money_away_odds.map(convert_line) + df.money_home_odds.map(convert_line)

    # what would be the payout on a $100 bet, if it won?
    df['money_away_payout'] = df.money_away_odds.map(payout)
    df['money_home_payout'] = df.money_home_odds.map(payout)

    # the payout on the popular side
    df['money_popular_payout'] = df.money_popular_odds.map(payout)

    return df


def load_summary_csv():
    dataframes = []
    for year in SEASONS.keys():
        df = pd.read_csv(f"yahoo_scrapes/{year}/odds.csv")
        dataframes.append(df.set_index('game_id'))
    return pd.concat(dataframes)
    # df = pd.read_csv("yahoo/2024_odds.csv")
    # return df


if __name__ == '__main__':
    SCRAPE_PAGES = False
    REBUILD_SUMMARY_CSV = False

    if SCRAPE_PAGES:
        for (season_name, season_range) in SEASONS.items():
            base_dir = f"yahoo_scrapes/{season_name}"
            fetch_yahoo_data(base_dir, season_range[0], season_range[1])

    if REBUILD_SUMMARY_CSV:        
        for year in SEASONS.keys():
            print(f"doing {year}")
            _start = time.time()

            base_dir = f"yahoo_scrapes/{year}"

            filenames = get_cached_filenames(base_dir)
            df = make_dataframe(filenames)

            df.to_csv(f"{base_dir}/odds.csv")
            print(f"took {time.time() - _start}")# in practice, about 2 seconds per game