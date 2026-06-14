from scrape_yahoo_mlb import *
scraper = ScrapeYahooMLB()

filename = "test/fixtures/fixture1.json"

with open(filename, 'r') as f:
    json_data = json.load(f)

parsed = scraper.parse_yahoo_data(json_data)

massaged = scraper.massage_yahoo_data(parsed, drop=False)

## this file has the money and spread teams in different order

assert massaged['money_home_team_id'] == massaged['home_team_id']
assert massaged['money_home_odds'] == massaged['money_two_odds']

assert massaged['spread_home_team_id'] == massaged['home_team_id']
assert massaged['spread_home_odds'] == massaged['spread_one_odds']