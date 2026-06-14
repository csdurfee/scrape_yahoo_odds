import json
import pytest
from scrape_yahoo_mlb import ScrapeYahooMLB

@pytest.fixture
def scraper():
    return ScrapeYahooMLB()

@pytest.fixture
def fixture1():
    with open("test/fixtures/fixture1.json", "r") as f:
        return json.load(f)


def test_massage_yahoo_data(scraper, fixture1):
    # fixture1 has money and spread teams in different order
    parsed = scraper.parse_yahoo_data(fixture1)
    massaged = scraper.massage_yahoo_data(parsed, drop=False)

    assert massaged["money_home_team_id"] == massaged["home_team_id"]
    assert massaged["money_home_odds"] == massaged["money_two_odds"]

    assert massaged["spread_home_team_id"] == massaged["home_team_id"]
    assert massaged["spread_home_odds"] == massaged["spread_one_odds"]
