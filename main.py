import pandas as pd
from utils.data import options
from utils.queries import team, decade, teammate, career, season


ratings = pd.read_csv('ratings.csv')

while True:
    print("Choose first option:")
    for i, opt in enumerate(options):
        print(f"\t{i}.) {opt}")
    
    a = input("Which is it: ").strip()
    
    if len(a) > 0:
        try:
            a_int = int(a)
            if 0 <= a_int < len(options):
                break  # valid input, exit loop
        except ValueError:
            pass  # invalid input, keep looping

a_df: pd.DataFrame
match a_int:
    case 0:
        a_df = team(ratings)
    case 1:
        a_df = decade(ratings)
    case 2:
        a_df = teammate(ratings)
    case 3:
        a_df = career(ratings, "points")
    case 4:
        a_df = career(ratings, "assists")
    case 5:
        a_df = career(ratings, "rebounds")
    case 6:
        a_df = career(ratings, "steals")
    case 7:
        a_df = career(ratings, "blocks")
    case 8:
        a_df = career(ratings, "games") 
    case 9:
        a_df = season(ratings, "points") 
    case 10:
        a_df = season(ratings, "assists")
    case 11:
        a_df = season(ratings, "rebounds")
    case 12:
        a_df = season(ratings, "steals")
    case 13:
        a_df = season(ratings, "blocks")
    

# 
while True:
    print("Choose second option:")
    for i, opt in enumerate(options):
        print(f"\t{i}.) {opt}")
    
    b = input("Which is it: ").strip()
    
    if len(b) > 0:
        try:
            b_int = int(b)
            if 0 <= b_int < len(options):
                break  # valid input, exit loop
        except ValueError:
            pass  # invalid input, keep looping

b_df: pd.DataFrame
match b_int:
    case 0:
        b_df = team(ratings)
    case 1:
        b_df = decade(ratings)
    case 2:
        b_df = teammate(ratings)
    case 3:
        b_df = career(ratings, "points")
    case 4:
        b_df = career(ratings, "assists")
    case 5:
        b_df = career(ratings, "rebounds")
    case 6:
        b_df = career(ratings, "steals")
    case 7:
        b_df = career(ratings, "blocks")
    case 8:
        b_df = career(ratings, "games") 
    case 9:
        b_df = season(ratings, "points") 
    case 10:
        b_df = season(ratings, "assists")
    case 11:
        b_df = season(ratings, "rebounds")
    case 12:
        b_df = season(ratings, "steals")
    case 13:
        b_df = season(ratings, "blocks")

merged_df = pd.merge(a_df, b_df, on='player', how='inner')
pd.set_option('display.max_rows', None)
print(merged_df)
