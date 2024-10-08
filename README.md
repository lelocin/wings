# Wings of Sound Database

This program is used to create and manage our database of artists (users), venues, venues' past events, and matches/match scores between artists and venues. It allows for creating tables, adding and removing elements, viewing the contents, and updating elements with new information in a MySQL database.

Our team chose SQL because our entities have clear relationships and the data is more structured (e.g. artists fill out information with prompts provided by us). In addition, most of our analyses will be relational, such as matching venues to artists. Therefore, SQL can better help maintain our data integrity and consistency and can better perform the queries for our projects without adding complexity.  

## Features

- INSERT new artists, venues, past events, and match score entries
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
   ```
   cd path/to/wings
   ```
   
3. Create a virtual environment
   ```
   python -m venv venv
   ```

   Activate the Virtual Environment 
   ```
   source venv/bin/activate
   ```

4. Install the required packages
   ```
   pip install -r requirements.txt
   ```
 
5. Set up your .env file
   ```
   touch .env
   ```

## Usage

To run the application:

```
python3 main.py
```
