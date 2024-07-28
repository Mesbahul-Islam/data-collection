import requests
import pandas as pd
import fetch
from time import sleep
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os
import logging
from typing import List, Dict, Tuple


load_dotenv()

#logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv('RIOT_API_KEY')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
game_name = os.getenv('GAME_NAME')
tag_line = os.getenv('TAG_LINE')
region = os.getenv('REGION') #europe, americas, asia
flag = bool(os.getenv('FLAG')) #True or False

#checking for environment variables
required_env_vars = [api_key, db_user, db_password, db_host, db_port, db_name, game_name, tag_line, region, flag]
if not all(required_env_vars):
    raise EnvironmentError("Some environment variables are missing. Please check your .env file.")

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=3))

def get_puuid(game_name: str, tag_line: str) -> str:
    """
    Get the puuid of the player
    """

    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}" + '?api_key=' + api_key
    try:
        response = session.get(api_url)
        response.raise_for_status()
        player = response.json()
        return player['puuid']
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        fetch.write_to_flag("False")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
    return ""

def write_start_index(start_index: int):
    """
    Write the start index to the .env file
    """
    with open('data_collection/.env', 'r') as f:
        lines = f.readlines()
    with open('data_collection/.env', 'w') as f:
        for line in lines:
            if 'START_INDEX' in line:
                f.write(f'START_INDEX={start_index}\n')
            else:
                f.write(line)

def read_start_index() -> int:
    """
    Read the start index from the .env file
    """
    with open('data_collection/.env', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'START_INDEX' in line:
            return int(line.split('=')[1].strip())
    return 0

def get_matches_by_puuid(puuid: str, start_index: int) -> List[str]:
    """
    Get the matches of the player by their puuid
    If there are no matches, set FLAG = False and START_INDEX = 0 and return empty list 
    """
    matches_by_puuid_url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/' + f'ids?start={start_index}&count=3' + '&api_key=' + api_key 
    try:
        response = session.get(matches_by_puuid_url)
        response.raise_for_status()
        matches = response.json()
        if not matches:
            logger.info("I am going in")
            fetch.write_to_flag("False")
            write_start_index(0)
            return []
        return matches
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
    return []


def get_match_data_by_id(match_ids: List[str], api_key: str, region: str) -> Tuple[List[Dict], List[List[str]]]:
    """
    Get the match data by the match id
    """
    base_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/"
    match_data = []
    player_info = []

    for match_id in match_ids:
        url = f"{base_url}{match_id}?api_key={api_key}"
        try:
            response = session.get(url)
            response.raise_for_status()
            data = response.json()
            metadata = data['metadata']
            info = data['info']
            match_data.append(info)
            player_info.append(metadata['participants'])
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred for match ID {match_id}: {http_err}")
        except Exception as err:
            logger.error(f"Other error occurred for match ID {match_id}: {err}")
        else:
            pass
        sleep(1)  # Respect API rate limits

    return match_data, player_info


def get_player_data(player_info_list: List[str]) -> List[Dict]:
    """
    Get match data for each player in the player_info_list and increase start_index by 3 (Default value) after each call
    """
    selective_data = []
    start_index = read_start_index()
    for players in player_info_list:
        for player in players:
            player_matches = get_matches_by_puuid(player,start_index)
            match_data, player_info = get_match_data_by_id(player_matches, api_key, region)
            selective_data.append(get_selective_data(match_data))
    if selective_data:
        write_start_index((start_index+3))
    return selective_data


def get_selective_data(match_data: List[Dict]) -> List[Dict]:
    """
    Get the selected data from the participants
    """
    champion_stats = []
    for match in match_data:
        participants = match['participants']
        for participant in participants:
            try:
                data = {
                    'championName': participant['championName'],
                    'lane': participant['lane'],
                    'deaths': participant['deaths'],
                    'kills': participant['kills'],
                    'assists': participant['assists'],
                    'win': participant['win'],
                    'riotIdGameName': participant['riotIdGameName'],
                    'riotIdTagline': participant['riotIdTagline'],
                    'item0': participant['item0'],
                    'item1': participant['item1'],
                    'item2': participant['item2'],
                    'item3': participant['item3'],
                    'item4': participant['item4'],
                    'item5': participant['item5'],
                    'item6': participant['item6']
                }
                champion_stats.append(data)
            except KeyError as e:
                # Handle missing keys in participant data
                print(f"Missing key {e} in participant data, skipping {participant}.")
    return champion_stats

def create_champion_stats_df(game_name: str, tag_line: str) -> pd.DataFrame:
    """
    Main function to fetch the data from the API and create a dataframe of the champion stats
    """
    if fetch.read_flag():
        start_index = read_start_index()
        puuid = get_puuid(game_name, tag_line)
        matches = get_matches_by_puuid(puuid, start_index)
        match_data, player_info = get_match_data_by_id(matches, api_key, region)
        champion_stats = get_player_data(player_info)
        champion_stats_df = pd.DataFrame(champion for match in champion_stats for champion in match).drop_duplicates()
        fetch.write_to_flag("True")
        return champion_stats_df
    else:
        logger.info("No new matches to fetch.")