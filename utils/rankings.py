import pandas as pd

# Define the CSV file to read
advanced_csv = 'data/Advanced.csv'
allstar_csv = 'data/All-Star Selections.csv'
awards_csv = 'data/End of Season Teams.csv'
player_awards_csv = 'data/Player Award Shares.csv'
per_game_csv = 'data/Player Per Game.csv'

# Read the necessary columns from the CSV
advanced_df = pd.read_csv(advanced_csv, usecols=['player_id', 'player', 'experience', 'g'])
allstar_df = pd.read_csv(allstar_csv, usecols=['player'])
per_game_df = pd.read_csv(per_game_csv, usecols=['player', 'trb_per_game', 'ast_per_game', 'stl_per_game', 'blk_per_game', 'pts_per_game'])

# Aggregate data: max experience and sum of games per player
grouped_df = advanced_df.groupby(['player_id', 'player']).agg({
    'experience': 'max',
    'g': 'sum'
}).reset_index()

# Count all star appearences
player_counts = allstar_df['player'].value_counts().reset_index()
player_counts.columns = ['player', 'mention_count']

grouped_df = grouped_df.merge(player_counts, on='player', how='left')
grouped_df['mention_count'] = grouped_df['mention_count'].fillna(0)

# Count all nba teams
awards_df = pd.read_csv(awards_csv, usecols=['player', 'type', 'number_tm'])
all_nba_df = awards_df[awards_df['type'] == 'All-NBA']
all_defense_df = awards_df[awards_df['type'] == 'All-Defense']
all_nba_count = all_nba_df.groupby(['player', 'number_tm']).size().unstack(fill_value=0).reset_index()
all_nba_count.columns.name = None  # Remove the column index name
all_nba_count = all_nba_count.rename(columns={'1st': 'All-NBA 1st', '2nd': 'All-NBA 2nd', '3rd': 'All-NBA 3rd'})
all_defense_count = all_defense_df.groupby(['player', 'number_tm']).size().unstack(fill_value=0).reset_index()
all_defense_count.columns.name = None  # Remove the column index name
all_defense_count = all_defense_count.rename(columns={'1st': 'All-Defense 1st', '2nd': 'All-Defense 2nd'})
grouped_df = grouped_df.merge(all_nba_count, on='player', how='left').merge(all_defense_count, on='player', how='left')
award_columns = [col for col in grouped_df.columns if 'All-NBA' in col or 'All-Defense' in col]
grouped_df[award_columns] = grouped_df[award_columns].fillna(0)

# Read the Player Awards CSV and count occurrences of each award per player
player_awards_df = pd.read_csv(player_awards_csv, usecols=['player', 'award', 'winner'])
player_awards_df = player_awards_df[player_awards_df['winner'] == True]
award_counts = player_awards_df.groupby(['player', 'award']).size().unstack(fill_value=0).reset_index()
award_counts.columns.name = None  # Remove the column index name
grouped_df = grouped_df.merge(award_counts, on='player', how='left')
grouped_df.fillna(0, inplace=True)

# stats
average_stats = per_game_df.groupby('player')[['trb_per_game', 'ast_per_game', 'stl_per_game', 'blk_per_game', 'pts_per_game']].mean().reset_index()
grouped_df = grouped_df.merge(average_stats, on='player', how='left')


def calculate_score(row):
    score = 0
    
    # Define column-specific scoring logic
    for column in row.index:
        value = row[column]
        if column == 'experience':
            score += value * 50
        elif column == 'g':
            score += value
        elif column == 'mention_count':
            score += value * 500
        elif column == 'All-NBA 1st':
            score += value * 1000
        elif column == 'All-NBA 2nd':
            score += value * 500
        elif column == 'All-NBA 3rd':
            score += value * 200
        elif column == 'All-Defense 1st':
            score += value * 1000
        elif column == 'All-Defense 2nd':
            score += value * 500
        elif column == 'aba mvp':
            score += value * 1500
        elif column == 'aba roy':
            score += value * 700
        elif column == 'clutch_poy':
            score += value * 500
        elif column == 'dpoy':
            score += value * 2000
        elif column == 'mip':
            score += value * 1000
        elif column == 'nba mvp':
            score += value * 5000
        elif column == 'nba roy':
            score += value * 1000
        elif column == 'trb_per_game':
            score += value * 25
        elif column == 'ast_per_game':
            score += value * 25
        elif column == 'stl_per_game':
            score += value * 50
        elif column == 'blk_per_game':
            score += value * 50
        elif column == 'pts_per_game':
            score += value * 50
    return score

grouped_df['score'] = grouped_df.apply(calculate_score, axis=1)
grouped_df['score'] = grouped_df['score'].fillna(0)
grouped_df = grouped_df[['player', 'score']]
grouped_df = grouped_df.sort_values(by='score', ascending=False)

# Display results
# print(grouped_df)

# player_name = "LeBron James"
# player_data = grouped_df[grouped_df['player'] == player_name]
# print(player_data)

# Save to a new CSV file
grouped_df.to_csv('ratings.csv', index=False)
