from sqlalchemy import create_engine
from request import *
import pandas as pd


engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
game_name = 'hahamarakha'
tag_line = '9960'
puuid = get_puuid(game_name, tag_line)
matches = get_matches_by_puuid(puuid)
match_data, player_info = get_match_by_id(matches)
champion_stats = get_selective_data(match_data)

champion_stats_df = pd.DataFrame(champion_stats)
champion_stats_df.to_sql('champion_stats', engine, if_exists='replace', index = False)

