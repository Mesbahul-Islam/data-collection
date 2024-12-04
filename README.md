  Match Data Collection

Match Data Collection
=====================

Overview
--------

This project is a Python-based data collection system that fetches League of Legends match statistics using the Riot Games API. It retrieves match data for a specified player provided through a csv file, then spiders out to collect other player's data from all players present in the first 3 matches of the first player. Running the script again increments this counter by 3 and upon reaching the end of the match list, the script moves onto the next player in the list provided. The script also formats the data for aggregation, and stores it in a local MySQL database. This process is automated using Apache Airflow.

Required Packages
-----------------

To install the required packages, run:

    pip install requests python-dotenv sqlalchemy pandas pymysql apache-airflow

Environment Variables
---------------------

Set up the following environment variables in the `.env` file located in the project root:

    
    RIOT_API_KEY=your_riot_api_key
    DB_USER=your_database_username
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port
    DB_NAME=your_database_name
    GAME_NAME=your_riot_id
    TAG_LINE=your_tag_line
    REGION=your_region
    FLAG=True
    START_INDEX=0
        

File Structure
--------------

Here is the file structure of the project:

    
    project_root/
    │
    ├── api_handling/
    │   ├── transform.py
    │   ├── fetch.py
    │   ├── request.py
    │   ├── main.py
    │   └── .env
    │
    ├── riot_id_list/
    │   └── player_id_list.csv
    │
    ├── dag_cfg/
    │   └── dag_main.py
    |   └── collection_dag.py
    |   └── collection.log
    │
    ├── README.md
    └── .gitignore
        

Data Collected
--------------

The following data is collected for each participant in a match:

*   Champion Name
*   Lane
*   Kills
*   Deaths
*   Assists
*   Win/Loss

How to Run
----------

### Step 1: Fetch Data

The data fetching process is handled by the `fetch.py` script. This script updates the `.env` file with the next player's game name and tag line if the flag is set to `False`.

### Step 2: Transform Data

The `transform.py` script contains functions to transform the fetched data into the desired format.

### Step 3: Main Function

The `main.py` script orchestrates the data fetching and transformation process and stores the data in the MySQL database.

To run the main function, execute:

    python main.py

### Step 4: Airflow DAG

The `collection_dag.py` script defines an Airflow DAG that schedules the data collection process to run daily.

To run the Airflow DAG, follow these steps:

1.  Start the Airflow web server:
    
        airflow webserver -p 8080
    
2.  Start the Airflow scheduler:
    
        airflow scheduler
    
3.  Access the Airflow web interface at `http://localhost:8080` and trigger the `data_collection_dag`.

Logging
-------

Logs are stored in the `collection.log` file for debugging and monitoring purposes.