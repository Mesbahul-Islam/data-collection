import requests
import requests
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

#checking for environment variables
required_env_vars = [api_key, db_user, db_password, db_host, db_port, db_name]
if not all(required_env_vars):
    raise EnvironmentError("Some environment variables are missing. Please check your .env file.")

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=3))

def get_puuid(game_name: str, tag_line: str) -> str:
    """
    Get the puuid of the player
    """

    api_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}" + '?api_key=' + api_key
    try:
        response = session.get(api_url)
        response.raise_for_status()
        player = response.json()
        return player['puuid']
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
    return ""

def get_matches_by_puuid(puuid: str) -> List[str]:
    """
    Get the matches of the player by their puuid
    """
    matches_by_puuid_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/' + 'ids?start=0&count=20' + '&api_key=' + api_key 
    try:
        response = session.get(matches_by_puuid_url)
        response.raise_for_status()
        matches = response.json()
        return matches[:3]
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
    return []

def get_match_data_by_id(match_ids: List[str]) -> Tuple[List[Dict], List[List[str]]]:
    """
    Get the match data by the match id
    """
    match_data = []
    player_info = []
    for i in range(len(match_ids)):
        matches_by_matchID_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_ids[i]}?api_key=" + api_key
        try:
            response = session.get(matches_by_matchID_url)
            response.raise_for_status()
            data = response.json()
            metadata = data['metadata']
            info = data['info']
            match_data.append(info)
            player_info.append(metadata['participants'])
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"Other error occurred: {err}")
    return match_data, player_info


def get_player_data(player_info_list: List[str]) -> List[Dict]:
    selective_data = []
    for players in player_info_list:
        for player in players:
            player_matches = get_matches_by_puuid(player)
            match_data, player_info = get_match_data_by_id(player_matches)
            selective_data.append(get_selective_data(match_data))
    return selective_data


def get_selective_data(match_data: List[Dict]) -> List[Dict]:
    """
    Get the selected data from the participants
    """

    champion_stats = []
    for match in match_data:
        participants = match['participants']
        for participant in participants:
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
    return champion_stats