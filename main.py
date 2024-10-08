import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def createConnection():
    connection = None
    try:
        print(f"Attempting to connect to:")
        print(f"Host: {os.getenv('DB_HOST')}")
        print(f"User: {os.getenv('DB_USER')}")
        print(f"Database: {os.getenv('DB_NAME')}")
        
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        print("Successfully connected to the database")
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        print(f"Error Code: {e.errno}")
        print(f"SQL State: {e.sqlstate}")
        print(f"Error Message: {e.msg}")
    return connection

def createArtistTable(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS artist (
        id uuid PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50),
        genre VARCHAR(50),
        email VARCHAR(150),
        desired_style VARCHAR(100),
        desired_capacity BIGINT,
        keywords TEXT,
        other_requests TEXT
    )
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'artist' created successfully!")
    except Error as e:
        print(f"Error creating table: {e}")

def createVenueTable(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS venue (
        id uuid PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        city VARCHAR(50),
        zipcode INT,
        phone BIGINT,
        capacity BIGINT,
        style VARCHAR(100),
        keywords TEXT
    )
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'venue' created successfully!")
    except Error as e:
        print(f"Error creating table: {e}")

def createPastShowTable(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS past_show (
        show_id uuid PRIMARY KEY,
        FOREIGN KEY (venue_id) REFERENCES venue(id),
        event_name VARCHAR(255) NOT NULL,
        event_artist VARCHAR(255),
        date DATE,
        audience_size BIGINT,
        ticket_price BIGINT,
        revenue BIGINT,
        genre VARCHAR(50),
        keywords TEXT
    )
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'past_show' created successfully!")
    except Error as e:
        print(f"Error creating table: {e}")

def createMatchTable(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS match (
        id uuid PRIMARY KEY,
        FOREIGN KEY (artist_id) REFERENCES artist(id),
        FOREIGN KEY (venue_id) REFERENCES artist(id),
        match_score BIGINT
    )
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'match' created successfully!")
    except Error as e:
        print(f"Error creating table: {e}")

def view_table(connection, table):
    if table not in ['artist', 'venue', 'past_show', 'match']:
        print("The table value you referenced is not one of the tables.")
        return
    query = f"SELECT * FROM {table}"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if not results:
                print("No entries found in the database.")
            else:
                if table == "artist":
                    for artist in results:
                        print(f"\nID: {artist[0]}")
                        print(f"Artist Name: {artist[1]} {artist[2]}")
                        print(f"Genre: {artist[3]}")
                        print(f"Email: {artist[4]}")
                        print(f"Desired Style: {artist[5]}")
                        print(f"Desired Capacity: {artist[6]}")
                        print(f"Keywords: {artist[7]}")
                        print(f"Other Requests: {artist[8]}")
                if table == "venue":
                    for venue in results:
                        print(f"\nID: {venue[0]}")
                        print(f"Venue Name: {venue[1]}")
                        print(f"City: {venue[2]}")
                        print(f"Zip Code: {venue[3]}")
                        print(f"Phone Number: {venue[4]}")
                        print(f"Capacity: {venue[5]}")
                        print(f"Style: {venue[6]}")
                        print(f"Keywords: {venue[7]}")
                if table == "past_show":
                    for show in results:
                        print(f"\nID: {show[0]}")
                        print(f"Venue ID: {show[1]}")
                        print(f"Artist: {show[2]}")
                        print(f"Event Date: {show[3]}")
                        print(f"Audience Size: {show[4]}")
                        print(f"Typical Ticket Price: {show[5]}")
                        print(f"Show Revenue: {show[6]}")
                        print(f"Show Genre: {show[7]}")
                        print(f"Keywords: {show[8]}")
                if table == "match":
                    for match in results:
                        print(f"\nID: {match[0]}")
                        print(f"Artist ID: {match[1]}")
                        print(f"Venue ID: {match[2]}")
                        print(f"Match Score: {match[3]}")
    except Error as e:
        print(f"Error retrieving entries: {e}")

def main():
    connection = createConnection()
    if connection is None:
        return
    createArtistTable(connection)
    createVenueTable(connection)
    createPastShowTable(connection)
    createMatchTable(connection)

if __name__ == "__main__":
    main()
