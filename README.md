# Match Data Collection 

## Overview

This project is a Python-based data collection system that fetches League of Legends match statistics using the Riot Games API. It retrieves match data for a specified player, processes the information, and stores it in a local MySQL database.

# Required Packages
pip install requests python-dotenv sqlalchemy pandas pymysql

# Set up environment variables in the project root
RIOT_API_KEY=your_riot_api_key
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_NAME=your_database_name

## Data Collected 
The following data is collected for each participant in a match:

Champion Name\
Lane\
Kills\
Deaths\
Assists\
Win/Loss\
