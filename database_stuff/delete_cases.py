import psycopg2

# Database connection parameters
db_params = {
    "user": "postgres",
    "password": "mysecretpassword",  # Replace with your PostgreSQL password
    "host": "localhost",  # Docker container is running on your local machine
    "port": "5432",  # Default PostgreSQL port
    "database": "teradrive"  # Replace with your database name
}

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute the SQL query to delete all rows from the "cases" table
    delete_query = "DELETE FROM cases;"
    cursor.execute(delete_query)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    print("All rows from the 'client' table have been deleted.")
except (Exception, psycopg2.Error) as error:
    print("Error deleting rows from 'cases' table:", error)
