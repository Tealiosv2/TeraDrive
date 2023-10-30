import psycopg2

# Database connection parameters
db_params = {
    "user": "postgres",
    "password": "mysecretpassword",  # Replace with your PostgreSQL password
    "host": "localhost",  # Docker container is running on your local machine
    "port": "5432",  # Default PostgreSQL port
    "database": "teradrive"  # Replace with your database name (teradrive)
}

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute the SQL query to select all rows from the "clients" table
    cursor.execute("SELECT * FROM users")

    # Fetch and print the results
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print("Error:", error)
