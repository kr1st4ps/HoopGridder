import pandas as pd

def team(ratings):
    # Load valid team abbreviations from CSV
    teams_df = pd.read_csv('teams.csv', usecols=['team', 'abbreviation'])
    valid_abbreviations = set(teams_df['abbreviation'].dropna().unique())

    while True:
        tm = input("Select team (abbreviation): ").strip().upper()
        if tm in valid_abbreviations:
            break
        else:
            print("Invalid team abbreviation. Please try again.")

    df = pd.read_csv('data/Advanced.csv', usecols=['player_id', 'player', 'tm'])
    df = df[df['tm'] == tm]
    df = df[['player']].drop_duplicates().reset_index(drop=True)

    df = df.merge(ratings, on='player', how='left')
    df = df[['player', 'score']]
    df = df.sort_values(by='score', ascending=False)
    
    return df

def decade(ratings):
    valid_options = ["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"]
    
    while True:
        selected_decade = input("Select decade (e.g. 1990): ").strip()
        if selected_decade in valid_options:
            break
        else:
            print(f"Invalid decade. Choose one of {valid_options}.")

    # Convert to integer range
    start_year = int(selected_decade)
    end_year = start_year + 10

    # Load data and filter by season range
    df = pd.read_csv('data/Advanced.csv', usecols=['player_id', 'player', 'season'])

    # Keep only rows where season is within the selected decade
    df = df[(df['season'] >= start_year) & (df['season'] < end_year)]

    # Drop duplicates and merge with ratings
    df = df[['player']].drop_duplicates().reset_index(drop=True)
    df = df.merge(ratings, on='player', how='left')
    df = df[['player', 'score']]
    df = df.sort_values(by='score', ascending=False)
    
    return df

def teammate(ratings):
    # Load the dataset with required columns
    df = pd.read_csv('data/Advanced.csv', usecols=['player_id', 'player', 'season', 'tm'])

    # Get unique player names for validation
    player_names = df['player'].dropna().unique()

    while True:
        selected_player = input("Enter player name: ").strip()
        if selected_player in player_names:
            break
        else:
            print("Player not found. Try again.")

    # Get all (season, tm) combos the player played in
    player_rows = df[df['player'] == selected_player]
    season_team_pairs = player_rows[['season', 'tm']].drop_duplicates()
    season_team_pairs = season_team_pairs[season_team_pairs['tm'] != "TOT"]

    # Join back to find all players with matching season + team
    teammates = df.merge(season_team_pairs, on=['season', 'tm'])

    # Drop duplicates
    teammates = teammates[['player']].drop_duplicates().reset_index(drop=True)

    # Merge with ratings if available
    teammates = teammates.merge(ratings, on='player', how='left')

    # Sort by score (if present)
    teammates = teammates[['player', 'score']].sort_values(by='score', ascending=False, na_position='last')

    return teammates

def career(ratings, stat):
    # Map user-friendly stat names to actual column names
    stat_map = {
        "points": "pts",
        "assists": "ast",
        "rebounds": "trb",
        "steals": "stl",
        "blocks": "blk",
        "games": "g"
    }

    # Validate stat input
    if stat not in stat_map:
        print(f"Invalid stat. Choose from: {list(stat_map.keys())}")
        return None

    column = stat_map[stat]

    # Ask user for minimum value
    while True:
        try:
            amount = float(input(f"Enter minimum career {stat}: ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")

    # Load stat data
    df = pd.read_csv('data/Player Totals.csv', usecols=['player', column])
    df = df.dropna(subset=[column])

    # Aggregate stat per player
    career_totals = df.groupby('player')[column].sum().reset_index()

    # Filter players who meet the minimum
    result = career_totals[career_totals[column] >= amount]

    # Merge with ratings
    result = result.merge(ratings, on='player', how='left')

    # Sort by score (then stat as tiebreaker)
    result = result.sort_values(by=['score', column], ascending=[False, False]).reset_index(drop=True)

    print(result)
    return result

def season(ratings, stat):
    # Mapping from user-friendly stat names to actual column names
    stat_map = {
        "points": "pts",
        "assists": "ast",
        "rebounds": "trb",
        "steals": "stl",
        "blocks": "blk",
    }

    # Validate stat input
    if stat not in stat_map:
        print(f"Invalid stat. Choose from: {list(stat_map.keys())}")
        return None

    column = stat_map[stat]

    # Ask user for the minimum season average
    while True:
        try:
            amount = float(input(f"Enter minimum season average for {stat}: ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")

    # Load the dataset with relevant columns (per season)
    df = pd.read_csv('data/Player Totals.csv', usecols=['player', 'season', column, 'g'])
    df = df.dropna(subset=[column, 'g'])  # Drop rows where the stat or games played is missing

    # Calculate the season average: total stat / total games
    df['season_avg'] = df[column] / df['g']

    # Filter for players whose season average is greater than or equal to the input amount
    result = df[df['season_avg'] >= amount]

    # Merge with ratings for additional data
    result = result.merge(ratings, on='player', how='left')

    # Sort by score (if available) and the season stat in descending order
    result = result.sort_values(by=['score', 'season_avg'], ascending=[False, False]).reset_index(drop=True)
    result = result[['player', 'season', 'season_avg', 'score']]

    print(result)
    return result