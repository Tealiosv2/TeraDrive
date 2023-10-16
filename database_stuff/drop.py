import psycopg2

# Database connection parameters
db_params = {
    "user": "postgres",
    "password": "mysecretpassword",  # Replace with your PostgreSQL password
    "host": "localhost",  # Docker container is running on your local machine
    "port": "5432",  # Default PostgreSQL port
    "database": "teradrive"  # Replace with your database name (teradrive)
}

# Specify the table to drop
table_to_drop = "clients"

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute the SQL query to drop the table
    drop_table_query = f"DROP TABLE IF EXISTS {table_to_drop};"
    cursor.execute(drop_table_query)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    print(f"Table '{table_to_drop}' dropped (if it existed).")
except (Exception, psycopg2.Error) as error:
    print(f"Error dropping '{table_to_drop}' table:", error)
