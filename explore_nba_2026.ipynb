{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "a5ea2b17",
   "metadata": {},
   "source": [
    "I have scraped odds data for the first half of the 2025-26 NBA season up to the all star break.\n",
    "\n",
    "Let's see what's been happening this year."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "7b4ed27f",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "plt.style.use('dark_background')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "9c52fd96",
   "metadata": {},
   "outputs": [],
   "source": [
    "import scrape_yahoo_nba\n",
    "import spread_data\n",
    "import money_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "ae265020",
   "metadata": {},
   "outputs": [],
   "source": [
    "scraper = scrape_yahoo_nba.ScrapeYahooNBA()\n",
    "\n",
    "df = scraper.load_summary_csv()\n",
    "\n",
    "df = spread_data.add_spread_columns(df)\n",
    "df = money_data.add_money_columns(df)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "749ae5d1",
   "metadata": {},
   "outputs": [],
   "source": [
    "this_season = df[df.game_date > '2025-09-01']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3a099c66",
   "metadata": {},
   "source": [
    "Let's see how teams have been doing against the spread this year."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "fe0c21ab",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "|               |   count |\n",
      "|:--------------|--------:|\n",
      "| Phoenix       |   0.636 |\n",
      "| Charlotte     |   0.6   |\n",
      "| Philadelphia  |   0.574 |\n",
      "| San Antonio   |   0.574 |\n",
      "| Denver        |   0.574 |\n",
      "| Miami         |   0.564 |\n",
      "| Boston        |   0.556 |\n",
      "| New York      |   0.556 |\n",
      "| LA Lakers     |   0.547 |\n",
      "| Portland      |   0.545 |\n",
      "| Utah          |   0.545 |\n",
      "| New Orleans   |   0.536 |\n",
      "| Detroit       |   0.519 |\n",
      "| Brooklyn      |   0.5   |\n",
      "| Toronto       |   0.5   |\n",
      "| LA Clippers   |   0.5   |\n",
      "| Indiana       |   0.5   |\n",
      "| Oklahoma City |   0.473 |\n",
      "| Atlanta       |   0.464 |\n",
      "| Golden State  |   0.455 |\n",
      "| Milwaukee     |   0.453 |\n",
      "| Chicago       |   0.453 |\n",
      "| Memphis       |   0.453 |\n",
      "| Dallas        |   0.444 |\n",
      "| Minnesota     |   0.436 |\n",
      "| Houston       |   0.434 |\n",
      "| Orlando       |   0.42  |\n",
      "| Washington    |   0.404 |\n",
      "| Cleveland     |   0.385 |\n",
      "| Sacramento    |   0.382 |\n"
     ]
    }
   ],
   "source": [
    "num_games = this_season.spread_winner_team_name.value_counts() + this_season.spread_loser_team_name.value_counts()\n",
    "win_pcts_ats = (this_season.spread_winner_team_name.value_counts() / num_games)\n",
    "print(win_pcts_ats.sort_values(ascending=False).round(3).to_markdown())"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4c00cb67",
   "metadata": {},
   "source": [
    "The Wizards have lost almost 60% of their games against the spread this year, which is remarkable considering they've lost 56% of their games against the spread over the previous four seasons. They have been incredibly consistent in their badness."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "249b0693",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'2021': (datetime.datetime(2021, 10, 19, 0, 0),\n",
       "  datetime.datetime(2022, 6, 16, 0, 0)),\n",
       " '2022': (datetime.datetime(2022, 10, 18, 0, 0),\n",
       "  datetime.datetime(2023, 6, 12, 0, 0)),\n",
       " '2023': (datetime.datetime(2023, 10, 24, 0, 0),\n",
       "  datetime.datetime(2024, 6, 17, 0, 0)),\n",
       " '2024': (datetime.datetime(2024, 10, 22, 0, 0),\n",
       "  datetime.datetime(2025, 6, 22, 0, 0)),\n",
       " '2025': (datetime.datetime(2025, 10, 21, 0, 0),\n",
       "  datetime.datetime(2026, 2, 12, 0, 0))}"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "scraper.SEASONS"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "2d11634b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# lazy copy-pasting\n",
    "s_2021 = df[(df.game_date > '2021-10-18') & (df.game_date < '2022-06-17')]\n",
    "s_2022 = df[(df.game_date > '2022-10-17') & (df.game_date < '2023-06-13')]\n",
    "s_2023 = df[(df.game_date > '2023-10-18') & (df.game_date < '2024-06-18')]\n",
    "s_2024 = df[(df.game_date > '2024-10-18') & (df.game_date < '2025-06-23')]\n",
    "s_2025 = df[df.game_date > '2025-10-20']\n",
    "\n",
    "def ats_report(this_season):\n",
    "    num_games = this_season.spread_winner_team_name.value_counts() + this_season.spread_loser_team_name.value_counts()\n",
    "    win_pcts_ats = (this_season.spread_winner_team_name.value_counts() / num_games)\n",
    "    print(win_pcts_ats.sort_values(ascending=False).round(3).to_markdown())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "86f9987d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "|               |   count |\n",
      "|:--------------|--------:|\n",
      "| Oklahoma City |   0.628 |\n",
      "| Memphis       |   0.626 |\n",
      "| Charlotte     |   0.588 |\n",
      "| Dallas        |   0.582 |\n",
      "| Toronto       |   0.57  |\n",
      "| Boston        |   0.567 |\n",
      "| Golden State  |   0.554 |\n",
      "| San Antonio   |   0.55  |\n",
      "| Miami         |   0.543 |\n",
      "| Detroit       |   0.543 |\n",
      "| Phoenix       |   0.532 |\n",
      "| Chicago       |   0.518 |\n",
      "| Minnesota     |   0.506 |\n",
      "| New Orleans   |   0.494 |\n",
      "| New York      |   0.488 |\n",
      "| Cleveland     |   0.488 |\n",
      "| LA Clippers   |   0.488 |\n",
      "| Indiana       |   0.481 |\n",
      "| Sacramento    |   0.475 |\n",
      "| Philadelphia  |   0.472 |\n",
      "| Milwaukee     |   0.465 |\n",
      "| Atlanta       |   0.447 |\n",
      "| Denver        |   0.44  |\n",
      "| Orlando       |   0.438 |\n",
      "| LA Lakers     |   0.43  |\n",
      "| Utah          |   0.427 |\n",
      "| Houston       |   0.425 |\n",
      "| Brooklyn      |   0.423 |\n",
      "| Portland      |   0.38  |\n",
      "| Washington    |   0.375 |\n",
      ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n",
      "|               |   count |\n",
      "|:--------------|--------:|\n",
      "| Philadelphia  |   0.589 |\n",
      "| Oklahoma City |   0.588 |\n",
      "| Utah          |   0.584 |\n",
      "| Orlando       |   0.562 |\n",
      "| Boston        |   0.56  |\n",
      "| New York      |   0.552 |\n",
      "| Sacramento    |   0.547 |\n",
      "| Cleveland     |   0.537 |\n",
      "| Denver        |   0.536 |\n",
      "| Toronto       |   0.532 |\n",
      "| Chicago       |   0.526 |\n",
      "| LA Lakers     |   0.516 |\n",
      "| Phoenix       |   0.511 |\n",
      "| Indiana       |   0.506 |\n",
      "| Brooklyn      |   0.506 |\n",
      "| Washington    |   0.5   |\n",
      "| Milwaukee     |   0.488 |\n",
      "| LA Clippers   |   0.482 |\n",
      "| Portland      |   0.481 |\n",
      "| Memphis       |   0.476 |\n",
      "| New Orleans   |   0.474 |\n",
      "| Golden State  |   0.467 |\n",
      "| Minnesota     |   0.463 |\n",
      "| Charlotte     |   0.456 |\n",
      "| Atlanta       |   0.44  |\n",
      "| Miami         |   0.44  |\n",
      "| Detroit       |   0.434 |\n",
      "| Houston       |   0.413 |\n",
      "| San Antonio   |   0.405 |\n",
      "| Dallas        |   0.4   |\n",
      ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n",
      "|               |   count |\n",
      "|:--------------|--------:|\n",
      "| Houston       |   0.651 |\n",
      "| Orlando       |   0.629 |\n",
      "| Dallas        |   0.593 |\n",
      "| Philadelphia  |   0.586 |\n",
      "| Indiana       |   0.566 |\n",
      "| Boston        |   0.562 |\n",
      "| Oklahoma City |   0.536 |\n",
      "| Minnesota     |   0.532 |\n",
      "| San Antonio   |   0.532 |\n",
      "| Miami         |   0.529 |\n",
      "| Sacramento    |   0.508 |\n",
      "| New Orleans   |   0.507 |\n",
      "| New York      |   0.507 |\n",
      "| Golden State  |   0.5   |\n",
      "| LA Lakers     |   0.493 |\n",
      "| Denver        |   0.486 |\n",
      "| Chicago       |   0.484 |\n",
      "| Portland      |   0.484 |\n",
      "| Memphis       |   0.475 |\n",
      "| Brooklyn      |   0.475 |\n",
      "| Detroit       |   0.469 |\n",
      "| Milwaukee     |   0.453 |\n",
      "| Washington    |   0.45  |\n",
      "| Utah          |   0.443 |\n",
      "| Phoenix       |   0.439 |\n",
      "| Charlotte     |   0.429 |\n",
      "| Toronto       |   0.422 |\n",
      "| Cleveland     |   0.413 |\n",
      "| LA Clippers   |   0.408 |\n",
      "| Atlanta       |   0.375 |\n",
      ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n",
      "|               |   count |\n",
      "|:--------------|--------:|\n",
      "| Toronto       |   0.622 |\n",
      "| Oklahoma City |   0.619 |\n",
      "| Cleveland     |   0.582 |\n",
      "| LA Clippers   |   0.562 |\n",
      "| Portland      |   0.561 |\n",
      "| LA Lakers     |   0.552 |\n",
      "| Houston       |   0.539 |\n",
      "| Chicago       |   0.53  |\n",
      "| Brooklyn      |   0.524 |\n",
      "| Detroit       |   0.523 |\n",
      "| Milwaukee     |   0.523 |\n",
      "| Utah          |   0.512 |\n",
      "| Memphis       |   0.511 |\n",
      "| Orlando       |   0.5   |\n",
      "| Golden State  |   0.495 |\n",
      "| Denver        |   0.49  |\n",
      "| Miami         |   0.489 |\n",
      "| Atlanta       |   0.488 |\n",
      "| Minnesota     |   0.485 |\n",
      "| New York      |   0.48  |\n",
      "| Dallas        |   0.476 |\n",
      "| Indiana       |   0.476 |\n",
      "| Boston        |   0.473 |\n",
      "| San Antonio   |   0.469 |\n",
      "| Charlotte     |   0.463 |\n",
      "| Sacramento    |   0.434 |\n",
      "| New Orleans   |   0.427 |\n",
      "| Washington    |   0.427 |\n",
      "| Phoenix       |   0.378 |\n",
      "| Philadelphia  |   0.354 |\n",
      ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n",
      "|               |   count |\n",
      "|:--------------|--------:|\n",
      "| Phoenix       |   0.636 |\n",
      "| Charlotte     |   0.6   |\n",
      "| Philadelphia  |   0.574 |\n",
      "| San Antonio   |   0.574 |\n",
      "| Denver        |   0.574 |\n",
      "| Miami         |   0.564 |\n",
      "| Boston        |   0.556 |\n",
      "| New York      |   0.556 |\n",
      "| LA Lakers     |   0.547 |\n",
      "| Portland      |   0.545 |\n",
      "| Utah          |   0.545 |\n",
      "| New Orleans   |   0.536 |\n",
      "| Detroit       |   0.519 |\n",
      "| Brooklyn      |   0.5   |\n",
      "| Toronto       |   0.5   |\n",
      "| LA Clippers   |   0.5   |\n",
      "| Indiana       |   0.5   |\n",
      "| Oklahoma City |   0.473 |\n",
      "| Atlanta       |   0.464 |\n",
      "| Golden State  |   0.455 |\n",
      "| Milwaukee     |   0.453 |\n",
      "| Chicago       |   0.453 |\n",
      "| Memphis       |   0.453 |\n",
      "| Dallas        |   0.444 |\n",
      "| Minnesota     |   0.436 |\n",
      "| Houston       |   0.434 |\n",
      "| Orlando       |   0.42  |\n",
      "| Washington    |   0.404 |\n",
      "| Cleveland     |   0.385 |\n",
      "| Sacramento    |   0.382 |\n",
      ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
     ]
    }
   ],
   "source": [
    "for s in [s_2021, s_2022, s_2023, s_2024, s_2025]:\n",
    "    ats_report(s)\n",
    "    print(\">\" * 40)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b4fba8dc",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
