import sqlite3



# sqlite database to store the data
def create_database():
    connection = sqlite3.connect("flights.db")
    cursor = connection.cursor()
    cursor.execute('''
        "CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Depart_date TEXT,
            Return_date TEXT,
            Origin TEXT,
            Destination TEXT,
            Departure time TEXT,
            Arrival time TEXT,
            Duration TEXT,
            Price TEXT
        )
        ''')
    # saves the changes to the database
    connection.commit()
    # close the connection to the database
    connection.close()
    
    
# function to insert data into the database
def insert_data(flight_data):
    connection = sqlite3.connect("flights.db")
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO flights (
            Depart_date,
            Return_date,
            Origin,
            Destination,
            Departure time,
            Arrival time,
            Duration,
            Price
        )
        VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
         )''',
         # the data to be inserted
          (flight_data['Depart date'],
           flight_data['Return date'],
           flight_data['Origin'],
           flight_data['Destination'],
           flight_data['Departure time'],
           flight_data['Arrival time'],
           flight_data['Duration'],
           flight_data['Price'])
    )
    
    connection.commit()
    connection.close()