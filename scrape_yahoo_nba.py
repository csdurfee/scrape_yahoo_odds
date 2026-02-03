from scrape_yahoo import *

class ScrapeYahooNBA(ScrapeYahoo):
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

    def parse_yahoo_data(self, json_data, filename=''):
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

        if row['home_team'] not in self.TEAMS:
            print(f"skipping game between {row['home_team']} and {row['away_team']}")
            return None

        if ('total_over_won' in row) and (row['total_over_won'] or row['total_under_won']):
            return row
        else:
            return None # nobody won (postponed game) or yahoo missing data


