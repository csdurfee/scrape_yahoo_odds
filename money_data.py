import scrape_utils

def add_money_columns(df):
    """
    adds more data about money line bets. 
    """
    # drop any games that are ties or don't have money line wager percentage data.
    df = df.copy().dropna(subset=['money_home_won', 'money_home_odds', 'money_away_odds',
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
    df['money_overround'] = df.money_away_odds.map(scrape_utils.convert_line) + df.money_home_odds.map(scrape_utils.convert_line)

    # what would be the payout on a $100 bet, if it won?
    df['money_away_payout'] = df.money_away_odds.map(scrape_utils.payout)
    df['money_home_payout'] = df.money_home_odds.map(scrape_utils.payout)

    # the payout on the popular side
    df['money_popular_payout'] = df.money_popular_odds.map(scrape_utils.payout)

    return df

