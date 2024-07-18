from sqlalchemy import create_engine
from request import *
import pandas as pd

start_index = int(os.getenv('START_INDEX'))
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4')
puuid = get_puuid(game_name, tag_line)
matches = get_matches_by_puuid(puuid, start_index)
match_data, player_info = get_match_data_by_id(matches)
champion_stats = get_player_data(player_info, start_index)
champion_stats_df = pd.DataFrame(champion for match in champion_stats for champion in match)
champion_stats_df.to_sql('champion_stats', engine, if_exists='append', index = False)


