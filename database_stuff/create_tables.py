import psycopg2

# Database connection parameters
db_params = {
    "user": "postgres",
    "password": "mysecretpassword",  # Replace with your PostgreSQL password
    "host": "localhost",  # Docker container is running on your local machine
    "port": "5432",  # Default PostgreSQL port
    "database": "teradrive"  # Replace with your database name
}

# SQL query to create the "clients" table (if it doesn't exist)
create_clients_table_query = """
    CREATE TABLE IF NOT EXISTS clients (
        client_id serial PRIMARY KEY,
        client_email VARCHAR (255),
        client_name VARCHAR (255),
        client_phone INT,
        client_cases INT[]
    );
"""

# SQL query to create the "cases" table (if it doesn't exist)
create_cases_table_query = """
    CREATE TABLE cases (
        case_id serial PRIMARY KEY,
        client_id INT,
        case_status VARCHAR (255),
        case_notes TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (client_id)
    );
"""

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute the SQL query to create the "clients" table (if it doesn't exist)
    cursor.execute(create_clients_table_query)

    # Execute the SQL query to create the "cases" table (if it doesn't exist)
    cursor.execute(create_cases_table_query)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    print("Tables 'clients' and 'cases' created (if they didn't exist).")
except (Exception, psycopg2.Error) as error:
    print("Error creating tables:", error)
