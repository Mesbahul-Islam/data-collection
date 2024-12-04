from sqlalchemy import create_engine
from request import *
from transform import *
import pandas as pd

start_index = read_start_index() # for initial call to get_matches_by_puuid

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4')
champion_stats_df = create_champion_stats_df(game_name, tag_line)

items_url = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json'
response = session.get(items_url)
response.raise_for_status()
items = response.json()

items_id = json_extract(items, 'id')
items_name = json_extract(items, 'name')

item_dict = create_mapped_dict(items_id, items_name)

champion_stats_df.replace(item_dict, inplace=True)

# Use a connection to execute SQL commands
with engine.connect() as connection:
    champion_stats_df.to_sql('champion_stats', connection, if_exists='append', index=False)
    logger.info('champion_stats table updated')

