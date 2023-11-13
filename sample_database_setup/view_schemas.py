import psycopg2

# Database connection parameters
db_params = {
    "user": "postgres",
    "password": "mysecretpassword",  # Replace with your PostgreSQL password
    "host": "localhost",  # Docker container is running on your local machine
    "port": "5432",  # Default PostgreSQL port
    "database": "teradrive"  # Replace with your database name (teradrive)
}

# Specify the table for which you want to view the schema
table_to_view = "cases"

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute the SQL query to view the schema of the table
    view_table_schema_query = f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = '{table_to_view}'
        ORDER BY ordinal_position ASC;
    """
    cursor.execute(view_table_schema_query)

    # Fetch and print the results
    table_schema = cursor.fetchall()
    for column in table_schema:
        print(f"Column: {column[0]}, Data Type: {column[1]}, Nullable: {column[2]}")

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print(f"Error viewing schema of '{table_to_view}' table:", error)
