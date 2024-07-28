import os
import pandas as pd


def write_to_flag(value: str):
    """
    If the flag is false, fetch from csv file and update the GAME_NAME and TAG_LINE in the .env file = current game_name + 1.
    else update the FlAG = value in the .env file.
    """
    flag = str_to_bool(value)
    if not flag:
        player_list_df = pd.read_csv("data_collection/riot_id_list/your_file.csv")
        initial_game_name = os.getenv('GAME_NAME')
        initial_tag_line = os.getenv('TAG_LINE')
        index = player_list_df[(player_list_df['riotIdGameName'] == initial_game_name) & 
                               (player_list_df['riotIdTagline'] == initial_tag_line)].index
        if not index.empty and index[0] + 1 < len(player_list_df):
            next_row = player_list_df.iloc[index[0] + 1]
            next_game_name = next_row['riotIdGameName']
            next_tag_line = next_row['riotIdTagline']
            update_env_file(next_game_name, next_tag_line)
    with open('data_collection/.env', 'r') as f:
        lines = f.readlines()
    with open('data_collection/.env', 'w') as f:
        for line in lines:
            if 'FLAG' in line:
                f.write(f'FLAG={value}\n')
            else:
                f.write(line)

def update_env_file(game_name: str, tag_line: str):
    """
    Update the GAME_NAME and TAG_LINE in the .env file.
    """
    with open('data_collection/.env', 'r') as file:
        lines = file.readlines()

    with open('data_collection/.env', 'w') as file:
        for line in lines:
            if line.startswith('GAME_NAME='):
                file.write(f'GAME_NAME={game_name}\n')
            elif line.startswith('TAG_LINE='):
                file.write(f'TAG_LINE={tag_line}\n')
            else:
                file.write(line)

def read_flag() -> bool:
    """
    Read the flag value from the .env file
    """
    with open('data_collection/.env', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'FLAG' in line:
            return bool(line.split('=')[1].strip())
    return False

def str_to_bool(value: str) -> bool:
    return value in ("True")