import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import uuid  # For generating unique IDs

# Load environment variables from .env file
load_dotenv()

# Dictionary to store table columns
TABLE_COLUMNS = {}

def generate_char12_uid():
    # Generate a UUID4 and take the first 12 characters from its hex representation
    return str(uuid.uuid4().hex)[:12]

def createConnection():
    """
    Establishes a connection to the MySQL database using credentials stored in environment variables.
    Returns a connection object or None if the connection fails.
    """
    connection = None
    try:
        print(f"Attempting to connect to:")
        print(f"Host: {os.getenv('DB_HOST')}")
        print(f"User: {os.getenv('DB_USER')}")
        print(f"Database: {os.getenv('DB_NAME')}")

        # Establish the connection using MySQL credentials from the .env file
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        print("Successfully connected to the database")
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    return connection

# Function to drop (clear) all tables if they exist
def clear_tables(connection):
    tables = ['matches', 'past_shows', 'venues', 'artists']  # List of tables to drop in reverse dependency order
    try:
        with connection.cursor() as cursor:
            for table in tables:
                # Drop each table if it exists
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                print(f"Table '{table}' dropped successfully!")
            connection.commit()
    except Error as e:
        print(f"Error dropping tables: {e}")


def createTables(connection):
    """
    Creates the necessary tables (artists, venues, past_shows, matches) if they do not already exist.
    Defines the structure for each table and also populates the global TABLE_COLUMNS dictionary with column names.
    """
    global TABLE_COLUMNS  # Make the table columns accessible throughout the script

    # Define table columns for each table
    TABLE_COLUMNS = {
        'artists': ['id', 'first_name', 'last_name', 'genre', 'email', 'desired_style', 'desired_capacity', 'keywords', 'other_requests'],
        'venues': ['id', 'name', 'city', 'zipcode', 'phone', 'capacity', 'style', 'keywords'],
        'past_shows': ['show_id', 'venue_id', 'event_name', 'event_artist', 'date', 'audience_size', 'ticket_price', 'revenue', 'genre', 'keywords'],
        'matches': ['id', 'artist_id', 'venue_id', 'match_score']
    }

    # Define the SQL statements to create tables
    tables = {
        'artists': """
            CREATE TABLE IF NOT EXISTS artists (
                id CHAR(12) PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                genre VARCHAR(50),
                email VARCHAR(150),
                desired_style VARCHAR(100),
                desired_capacity BIGINT,
                keywords TEXT,
                other_requests TEXT
            )
        """,
        'venues': """
            CREATE TABLE IF NOT EXISTS venues (
                id CHAR(12) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                city VARCHAR(50),
                zipcode INT,
                phone BIGINT,
                capacity BIGINT,
                style VARCHAR(100),
                keywords TEXT
            )
        """,
        'past_shows': """
            CREATE TABLE IF NOT EXISTS past_shows (
                show_id CHAR(12) PRIMARY KEY,
                venue_id CHAR(12),
                event_name VARCHAR(255) NOT NULL,
                event_artist VARCHAR(255),
                date DATE,
                audience_size BIGINT,
                ticket_price BIGINT,
                revenue BIGINT,
                genre VARCHAR(50),
                keywords TEXT,
                FOREIGN KEY (venue_id) REFERENCES venues(id)
            )
        """,
        'matches': """
            CREATE TABLE IF NOT EXISTS matches (
                id CHAR(12) PRIMARY KEY,
                artist_id CHAR(12),
                venue_id CHAR(12),
                match_score BIGINT,
                FOREIGN KEY (artist_id) REFERENCES artists(id),
                FOREIGN KEY (venue_id) REFERENCES venues(id)
            )
        """
    }

    # Execute the table creation statements
    try:
        with connection.cursor() as cursor:
            for table_name, create_table_query in tables.items():
                cursor.execute(create_table_query)
                connection.commit()
                print(f"Table '{table_name}' created successfully!")
    except Error as e:
        print(f"Error creating table: {e}")

def add_sample_data(connection):
    """
    Inserts predefined sample data into the artists, venues, past_shows, and matches tables.
    This function uses batch insertions to add multiple rows of data at once.
    """
    # Sample data for artists
    artist_data = [
        (str(generate_char12_uid()), 'John', 'Doe', 'Rock', 'john.doe@example.com', 'Concert', 500, 'rock, loud, energetic', 'No pyrotechnics'),
        (str(generate_char12_uid()), 'Jane', 'Smith', 'Jazz', 'jane.smith@example.com', 'Jazz Club', 200, 'jazz, acoustic, mellow', 'Piano required'),
        (str(generate_char12_uid()), 'Emily', 'Clark', 'Pop', 'emily.clark@example.com', 'Festival', 2000, 'pop, dance, upbeat', 'Stage lighting')
    ]

    # Sample data for venues
    venue_data = [
        (str(generate_char12_uid()), 'The Rock Arena', 'New York', 10001, 1234567890, 5000, 'Concert Hall', 'rock, arena, loud'),
        (str(generate_char12_uid()), 'Jazz Corner', 'Chicago', 60601, 2345678901, 300, 'Jazz Club', 'jazz, intimate, cozy'),
        (str(generate_char12_uid()), 'Pop Fest Grounds', 'Los Angeles', 90001, 3456789012, 10000, 'Festival Grounds', 'pop, festival, outdoor')
    ]

    # Sample data for past shows
    past_show_data = [
        (str(generate_char12_uid()), venue_data[0][0], 'Rock Fest', 'John Doe', '2023-06-15', 4500, 50, 225000, 'Rock', 'energetic, loud'),
        (str(generate_char12_uid()), venue_data[1][0], 'Smooth Jazz Night', 'Jane Smith', '2023-07-20', 250, 75, 18750, 'Jazz', 'mellow, acoustic'),
        (str(generate_char12_uid()), venue_data[2][0], 'Pop Explosion', 'Emily Clark', '2023-09-12', 9500, 60, 570000, 'Pop', 'dance, upbeat')
    ]

    # Sample data for matches
    match_data = [
        (str(generate_char12_uid()), artist_data[0][0], venue_data[0][0], 85),
        (str(generate_char12_uid()), artist_data[1][0], venue_data[1][0], 90),
        (str(generate_char12_uid()), artist_data[2][0], venue_data[2][0], 95)
    ]

    try:
        with connection.cursor() as cursor:
            # Insert sample artists
            artist_query = f"INSERT INTO artists ({', '.join(TABLE_COLUMNS['artists'])}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(artist_query, artist_data)
            
            # Insert sample venues
            venue_query = f"INSERT INTO venues ({', '.join(TABLE_COLUMNS['venues'])}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(venue_query, venue_data)
            
            # Insert sample past shows
            past_show_query = f"INSERT INTO past_shows ({', '.join(TABLE_COLUMNS['past_shows'])}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(past_show_query, past_show_data)

            # Insert sample matches
            match_query = f"INSERT INTO matches ({', '.join(TABLE_COLUMNS['matches'])}) VALUES (%s, %s, %s, %s)"
            cursor.executemany(match_query, match_data)

            connection.commit()
            print("Sample data added successfully!")
    except Error as e:
        print(f"Error inserting sample data: {e}")

def add_item(connection, table):
    """
    Prompts the user to enter values for a specific table and inserts a new row into the database.
    Automatically generates UUIDs for 'id' and 'show_id' columns.
    """
    global TABLE_COLUMNS
    columns = TABLE_COLUMNS.get(table)

    if not columns:
        print(f"Table '{table}' is not defined.")
        return
    
    values = []
    # Loop through columns and prompt for user input
    for column in columns:
        # Auto-generate UUID for primary keys
        if column == 'id' or column == 'show_id':
            values.append(str(uuid.uuid4()))
        else:
            user_input = input(f"Enter value for {column}: ")
            values.append(user_input)
    
    column_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(values))
    insert_query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query, values)
            connection.commit()
            print(f"Item added to table '{table}' successfully!")
    except Error as e:
        print(f"Error adding item to {table}: {e}")

def get_venue_by_id(connection, venue_id):
    """
    Fetches a venue's details from the 'venues' table by its ID.
    
    Parameters:
    - connection: The MySQL database connection object
    - venue_id: The unique ID of the venue to fetch
    
    Returns:
    - Venue details if found, otherwise a message indicating no such venue exists
    """
    try:
        with connection.cursor() as cursor:
            # Query to fetch the venue by its ID
            cursor.execute(f"SELECT * FROM venues WHERE id = %s", (venue_id,))
            venue = cursor.fetchone()
            
            if venue:
                # Print the column names and the venue details
                column_names = TABLE_COLUMNS.get('venues')
                print("\nVenue details:")
                print(" | ".join(column_names))
                print(" | ".join([str(item) for item in venue]))
            else:
                print(f"No venue found with ID: {venue_id}")
    except Error as e:
        print(f"Error fetching venue by ID: {e}")


# Function to view data from any table
def view_data(connection, table):
    try:
        with connection.cursor() as cursor:
            # Select all rows from the specified table
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            if rows:
                # Print the column names and rows
                print(f"\nData from {table}:")
                column_names = TABLE_COLUMNS.get(table)
                if column_names:
                    print(" | ".join(column_names))
                for row in rows:
                    print(" | ".join([str(item) for item in row]))
            else:
                print(f"No data found in table '{table}'.")

    except Error as e:
        print(f"Error fetching data from {table}: {e}")


def main():
    connection = createConnection()
    if connection is None:
        return

    clear_tables(connection)
    # Create all necessary tables
    createTables(connection)

    # Add sample data
    add_sample_data(connection)

    # Optional: You can still use the input functionality to add custom values
    add_custom_data = input("Do you want to add custom data? (yes/no): ").strip().lower()
    if add_custom_data == 'yes':
        table = input("Enter the table name (artists, venues, past_shows, matches): ")
        add_item(connection, table)

    for table in ["artists", "venues", "past_shows", "matches"]:
        view_data(connection, table)

    get_venue_id = input("Do you want to get specific venue details? (yes/no): ").strip().lower()
    if get_venue_id == 'yes':   
        venue_id = input("Enter a venue ID to fetch its details: ").strip()
        get_venue_by_id(connection, venue_id)

if __name__ == "__main__":
    main()
