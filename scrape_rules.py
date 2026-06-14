THE_GAME = '$.data.games[0]'

OVER_UNDER = THE_GAME + '.gameLineSixPack[?type = "OVER_UNDER" & period = "FULL_GAME" & eventState = "PREGAME"]'
OVER_INFO = OVER_UNDER + '.options[0]'
UNDER_INFO = OVER_UNDER + '.options[1]'

MONEY_LINE = THE_GAME + '.gameLineSixPack[?type = "MONEY_LINE" & period = "FULL_GAME" & eventState = "PREGAME"]'
MONEY_ONE_INFO= MONEY_LINE + '.options[0]'
MONEY_TWO_INFO = MONEY_LINE + '.options[1]'

SPREAD = THE_GAME + '.gameLineSixPack[?type = "SPREAD" & period = "FULL_GAME" & eventState = "PREGAME"]'
SPREAD_ONE_INFO = SPREAD + '.options[0]'
SPREAD_TWO_INFO = SPREAD + '.options[1]'

RULES = {
    'game_id': THE_GAME + '.gameId',
    'game_date': THE_GAME + '.startDate',

    'away_team': THE_GAME + '.awayTeam.displayName',
    'home_team': THE_GAME + '.homeTeam.displayName',

    'away_team_id': THE_GAME + '.awayTeam.teamId',
    'home_team_id': THE_GAME + '.homeTeam.teamId',

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
    'money_one_odds': MONEY_ONE_INFO + '.americanOdds',
    'money_one_decimal_odds': MONEY_ONE_INFO + '.decimalOdds',
    'money_one_stake_percentage': MONEY_ONE_INFO + '.stakePercentage',
    'money_one_wager_percentage': MONEY_ONE_INFO + '.wagerPercentage',
    'money_one_won': MONEY_ONE_INFO + '.isCorrect',
    'money_one_team_id': MONEY_ONE_INFO + '.teamIds[0]',

    'money_two_odds': MONEY_TWO_INFO + '.americanOdds',
    'money_two_decimal_odds': MONEY_TWO_INFO + '.decimalOdds',
    'money_two_stake_percentage': MONEY_TWO_INFO + '.stakePercentage',
    'money_two_wager_percentage': MONEY_TWO_INFO + '.wagerPercentage',
    'money_two_won': MONEY_TWO_INFO + '.isCorrect',
    'money_two_team_id': MONEY_TWO_INFO + '.teamIds[0]',

    # spread data
    'spread_one_points': SPREAD_ONE_INFO + '.optionDetails[0].value',
    'spread_one_odds': SPREAD_ONE_INFO + '.americanOdds',
    'spread_one_decimal_odds': SPREAD_ONE_INFO + '.decimalOdds',
    'spread_one_stake_percentage': SPREAD_ONE_INFO + ".stakePercentage",
    'spread_one_wager_percentage': SPREAD_ONE_INFO + ".wagerPercentage",
    'spread_one_won': SPREAD_ONE_INFO + ".isCorrect",
    'spread_one_team_id': SPREAD_ONE_INFO + '.teamIds[0]',

    'spread_two_points': SPREAD_TWO_INFO + '.optionDetails[0].value',
    'spread_two_odds': SPREAD_TWO_INFO + '.americanOdds',
    'spread_two_decimal_odds': SPREAD_TWO_INFO + ".decimalOdds",
    'spread_two_stake_percentage': SPREAD_TWO_INFO + ".stakePercentage",
    'spread_two_wager_percentage': SPREAD_TWO_INFO + ".wagerPercentage",
    'spread_two_won': SPREAD_TWO_INFO + '.isCorrect',
    'spread_two_team_id': SPREAD_TWO_INFO + '.teamIds[0]',
}