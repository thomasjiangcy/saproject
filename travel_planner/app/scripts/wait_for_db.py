"""
Wait for PostgreSQL to be up
"""

import os
import time
import psycopg2


DB_NAME = os.getenv('POSTGRES_DB', 'travel_planner')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_PORT = os.getenv('POSTGRES_PORT', 5432)

# wait while DB is not ready
while True:
    try:
        print(DB_NAME)
        print('Trying to connect to DB...')
        db_connection = psycopg2.connect(dbname=DB_NAME,
                                         user=DB_USER,
                                         password=DB_PASSWORD,
                                         host=DB_HOST,
                                         port=DB_PORT)
        print('DB connection SUCCESS')
        db_connection.close()
        break
    except psycopg2.OperationalError as err:
        print(err)
        print('DB connection FAIL')
        time.sleep(5)
