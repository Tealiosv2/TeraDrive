import psycopg2
import random

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

    # Sample data for the 'clients' table
    clients_data = [
        (i, f"client{i}@example.com", f"Client {i}")
        for i in range(1, 16)
    ]

    # Insert sample data into the 'clients' table
    insert_clients_query = """
        INSERT INTO clients (client_email, client_name)
        VALUES (%s, %s);
    """
    cursor.executemany(insert_clients_query, clients_data)

    # Sample data for the 'cases' table
    cases_data = [
        (i, random.randint(1, 15), 'Open', f'Case {i} details')
        for i in range(1, 16)
    ]

    # Insert sample data into the 'cases' table
    insert_cases_query = """
        INSERT INTO cases (client_id, case_status, case_notes)
        VALUES (%s, %s, %s);
    """
    cursor.executemany(insert_cases_query, cases_data)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    print("Sample data inserted successfully.")
except (Exception, psycopg2.Error) as error:
    print("Error inserting sample data:", error)
