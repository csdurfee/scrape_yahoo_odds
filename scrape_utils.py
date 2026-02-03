import pandas as pd

def numericize(df):
    """
    Converts columns that should be numeric/boolean
    """
    points = df.columns[df.columns.str.contains('points')]
    percentages = df.columns[df.columns.str.contains('percentage')]
    to_numeric = list(points) + list(percentages)
    df[to_numeric] = df[to_numeric].apply(pd.to_numeric)

    # if a Series is an object datatype but contains boolean values,
    # eldritch horrors emerge if you do a ~ on it, 
    # eg ~(pd.Series([True, False, True, False]).astype(object))
    to_bools = df.columns[df.columns.str.contains('won')]
    for col in to_bools:
        df[col] = df[col].astype(bool)

    return df

def convert_line(line):
    """
    convert American style money line to the implied probability

    -400 implies you will win 4 out of 5 bets
    >>> convert_line(-400)
    0.8
    >>> convert_line(+300)
    0.25
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
