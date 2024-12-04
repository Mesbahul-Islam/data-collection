import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PLAYER_LIST_CSV_PATH = os.getenv('PLAYER_LIST_CSV_PATH')

def write_to_flag(value: str):
    """
    If the flag is false, fetch from csv file and update the GAME_NAME and TAG_LINE in the api_handling/.env file = current game_name + 1.
    else update the FLAG = value in the api_handling/.env file.
    """
    flag = str_to_bool(value)
    if not flag:
        player_list_df = pd.read_csv(PLAYER_LIST_CSV_PATH)
        initial_game_name = os.getenv('GAME_NAME')
        initial_tag_line = os.getenv('TAG_LINE')
        index = player_list_df[(player_list_df['riotIdGameName'] == initial_game_name) &
                               (player_list_df['riotIdTagline'] == initial_tag_line)].index
        if not index.empty and index[0] + 1 < len(player_list_df):
            next_row = player_list_df.iloc[index[0] + 1]
            next_game_name = next_row['riotIdGameName']
            next_tag_line = next_row['riotIdTagline']
            update_env_file(next_game_name, next_tag_line)
    with open('api_handling/.env', 'r') as f:
        lines = f.readlines()
    with open('api_handling/.env', 'w') as f:
        for line in lines:
            if 'FLAG' in line:
                f.write(f'FLAG={value}\n')
            else:
                f.write(line)

def update_env_file(game_name: str, tag_line: str):
    """
    Update the GAME_NAME and TAG_LINE in the api_handling/.env file.
    """
    with open('api_handling/.env', 'r') as file:
        lines = file.readlines()

    with open('api_handling/.env', 'w') as file:
        for line in lines:
            if line.startswith('GAME_NAME='):
                file.write(f'GAME_NAME={game_name}\n')
            elif line.startswith('TAG_LINE='):
                file.write(f'TAG_LINE={tag_line}\n')
            else:
                file.write(line)

def get_env_variable(key: str) -> str:
    """
    Get the value of an environment variable from the api_handling/.env file
    """
    with open('api_handling/.env', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith(key):
            return line.split('=')[1].strip()
    return ''

def read_flag() -> bool:
    """
    Read the flag value from the api_handling/.env file
    """
    with open('api_handling/.env', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'FLAG' in line:
            return bool(line.split('=')[1].strip())
    return False

def str_to_bool(value: str) -> bool:
    return value in ("True")
