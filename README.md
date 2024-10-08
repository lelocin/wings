# Wings of Sound Database

This program is used to create and manage our database of artists (users), venues, venues' past events, and matches/match scores between artists and venues. It allows for creating tables, adding and removing elements, viewing the contents, and updating elements with new information in a MySQL database.

## Features

- INSERT new artists, venues, past events, and math score entries
- VIEW all items in each of the four tables
- UPDATE information in an existing entry to one of the four tables
- DELETE entries from the database

## Prerequisites

- Python 3.11 or higher
- MySQL server, with appropriate host, username, password, database name
- pip (Python package manager)

## Setup

1. Clone the repository or download the source code.
   ```
   git clone https://github.com/projects-in-programming-f24/campy.git
   ```
   
2. Navigate to the project's directory
   (For Mac)
   ```
   cd path/to/wings
   ```
   (For Windows) 
   ```
   cd path\to\wings
   ```


3. Create a virtual environment
   ```
   python -m venv venv
   ```

4. Activate the Virtual Environment 
   (For Mac)
   ```
   source venv/bin/activate
   ```
   (For Windows)
   ```
   venv\Scripts\activate
   ```

5. Install the required packages
   ```
   pip install -r requirements.txt
   ```
 
6. Set up your .env file
  6a. Create a new .env file in the project root directory
  (For Mac)
  
   ```
   touch .env
   ```
   (For Windows)
   ```
   type nul > .env
   ```
   6b. Open the '.env' file in a text editor
   6c. Add the following your '.env' file and replace the placeholders with your actual MySQL connection details: 
   ```
   DB_HOST=my_mysql_host
   DB_USER=myuser
   DB_PASS=mypassword
   DB_NAME=my_database_name
   ```
   6d. Save and close the '.env' file 

   Note: Note: The `.env` file contains sensitive information. Make sure it's included in your `.gitignore` file to prevent it from being committed to version control.
 
## Usage

To run the application:

```
python3 main.py
```