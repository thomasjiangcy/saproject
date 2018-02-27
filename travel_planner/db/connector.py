import os
import psycopg2


USER = os.getenv('DB_USER')
HOST = os.getenv('DB_HOST')
PASSWORD = os.getenv('DB_PASSWORD')

class Connector:

    def __init__(self):
        if USER is None or HOST is None or PASSWORD is None:
            raise ValueError(
                'Make sure all values are set for environment variables: '
                'DB_USER, DB_HOST and DB_PASSWORD'
            )

        self.connection = psycopg2.connect(
            dbname='social',
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=5432
        )
        self.cursor = self.connection.cursor()
    
    def close(self):
        # Close connection with DB
        self.connection.close()

    def fetch_venue_ids(self):
        self.cursor.execute('SELECT id FROM venue;')
        try:
            res = self.cursor.fetchall()
            return [r[0] for r in res]  # Parse results into a flat list
        except Exception as err:
            print('Something went wrong while trying to fetch venue IDs: ' % err)
        
    
