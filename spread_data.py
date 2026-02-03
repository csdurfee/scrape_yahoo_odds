import scrape_utils
import pandas as pd

def add_spread_columns(df):
    """
    adds additional columns related to betting against the spread
    from calculated results not in the original yahoo API
    """
    ## convert fields that need to be numeric
    df = scrape_utils.numericize(df)

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
