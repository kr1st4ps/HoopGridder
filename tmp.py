import pandas as pd

# Load the CSV
df = pd.read_csv('data/Team Abbrev.csv', usecols=['team', 'abbreviation'])

# Drop duplicate combinations of team and abbreviation
unique_teams = df.drop_duplicates(subset=['team', 'abbreviation']).reset_index(drop=True)

# Display the result
# print(unique_teams)
unique_teams.to_csv('teams.csv', index=False)