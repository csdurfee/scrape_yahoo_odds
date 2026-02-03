THE_GAME = '$.data.games[0]'

OVER_UNDER = THE_GAME + '.gameLineSixPack[?type = "OVER_UNDER" & period = "FULL_GAME" & eventState = "PREGAME"]'
OVER_INFO = OVER_UNDER + '.options[0]'
UNDER_INFO = OVER_UNDER + '.options[1]'

MONEY_LINE = THE_GAME + '.gameLineSixPack[?type = "MONEY_LINE" & period = "FULL_GAME" & eventState = "PREGAME"]'
MONEY_AWAY_INFO = MONEY_LINE + '.options[0]'
MONEY_HOME_INFO = MONEY_LINE + '.options[1]'

SPREAD = THE_GAME + '.gameLineSixPack[?type = "SPREAD" & period = "FULL_GAME" & eventState = "PREGAME"]'
SPREAD_AWAY_INFO = SPREAD + '.options[0]'
SPREAD_HOME_INFO = SPREAD + '.options[1]'

RULES = {
    'game_id': THE_GAME + '.gameId',
    'game_date': THE_GAME + '.startDate',

    'away_team': THE_GAME + '.awayTeam.displayName',
    'home_team': THE_GAME + '.homeTeam.displayName',

    # this contains both spread and total info.
    # I believe this is the opening line, but haven't verified that
    'pregame_odds': THE_GAME + '.gameOddsSummary.pregameOddsDisplay',

    # totals. over/under data
    'total_over_points': OVER_INFO + '.optionDetails[0].value',
    'total_over_stake_percentage': OVER_INFO + '.stakePercentage',
    'total_over_wager_percentage': OVER_INFO + '.wagerPercentage',
    'total_over_odds': OVER_INFO + '.americanOdds',
    'total_over_decimal_odds': OVER_INFO + '.decimalOdds',
    'total_over_won': OVER_INFO + '.isCorrect',

    'total_under_points': UNDER_INFO + '.optionDetails[0].value',
    'total_under_stake_percentage': UNDER_INFO + '.stakePercentage',
    'total_under_wager_percentage': UNDER_INFO + '.wagerPercentage',
    'total_under_odds': UNDER_INFO + '.americanOdds',
    'total_under_decimal_odds': UNDER_INFO + '.decimalOdds',
    'total_under_won': UNDER_INFO + '.isCorrect',


    # money line data
    'money_away_odds': MONEY_AWAY_INFO + '.americanOdds',
    'money_away_decimal_odds': MONEY_AWAY_INFO + '.decimalOdds',
    'money_away_stake_percentage': MONEY_AWAY_INFO + '.stakePercentage',
    'money_away_wager_percentage': MONEY_AWAY_INFO + '.wagerPercentage',
    'money_away_won': MONEY_AWAY_INFO + '.isCorrect',

    'money_home_odds': MONEY_HOME_INFO + '.americanOdds',
    'money_home_decimal_odds': MONEY_HOME_INFO + '.decimalOdds',
    'money_home_stake_percentage': MONEY_HOME_INFO + '.stakePercentage',
    'money_home_wager_percentage': MONEY_HOME_INFO + '.wagerPercentage',
    'money_home_won': MONEY_HOME_INFO + '.isCorrect',

    # spread data
    'spread_away_points': SPREAD_AWAY_INFO + '.optionDetails[0].value',
    'spread_away_odds': SPREAD_AWAY_INFO + '.americanOdds',
    'spread_away_decimal_odds': SPREAD_AWAY_INFO + '.decimalOdds',
    'spread_away_stake_percentage': SPREAD_AWAY_INFO + ".stakePercentage",
    'spread_away_wager_percentage': SPREAD_AWAY_INFO + ".wagerPercentage",
    'spread_away_won': SPREAD_AWAY_INFO + ".isCorrect",

    'spread_home_points': SPREAD_HOME_INFO + '.optionDetails[0].value',
    'spread_home_odds': SPREAD_HOME_INFO + '.americanOdds',
    'spread_home_decimal_odds': SPREAD_HOME_INFO + ".decimalOdds",
    'spread_home_stake_percentage': SPREAD_HOME_INFO + ".stakePercentage",
    'spread_home_wager_percentage': SPREAD_HOME_INFO + ".wagerPercentage",
    'spread_home_won': SPREAD_HOME_INFO + '.isCorrect',
}