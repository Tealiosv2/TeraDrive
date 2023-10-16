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
        (f"joltik@unova.com", "Jol Tik"),
        (f"flittle@paldea.com", "Flit Tle"),
        (f"krabby@kanto.com", "Krab By"),
        (f"fuecoco@paldea.com", "Fue Coco"),
        (f"metang@hoenn.com", "Met Ang"),
    ]

    # Insert sample data into the 'clients' table
    insert_clients_query = """
        INSERT INTO clients (client_email, client_name)
        VALUES (%s, %s);
    """
    cursor.executemany(insert_clients_query, clients_data)

    # Sample data for the 'cases' table
    cases_data = [
        (1, "Open", "Joltik is a tiny arachnid Pokémon"), #1
        (1, "Closed", "It has four legs tipped with blue, conical feet."),#2
        (2, "Open", "Flittle is a small Pokémon resembling a bird chick"),#3
        (4, "Open", "Fuecoco is a bipedal crocodilian Pokémon with a mostly red body and a white stomach and face."),#4
        (4, "Open", "Its body contains a small flame sac, which constantly leaks fire energy due to its size."),#5
        (4, "Closed", "The energy releases in the form of two bright yellow tufts of flame on top of its head"),#6
        (5, "Open", "Metang is a robotic Pokémon with teal, metallic skin")#7
    ]

    insert_cases_query = """
        INSERT INTO cases (client_id, case_status, case_notes)
        VALUES (%s, %s, %s);
    """

    cursor.executemany(insert_cases_query, cases_data)

    client_case_data = {
        1: [1,2],
        2: [3],
        4:[4,5,6],
        5:[7]
        # Add more clients and their respective case IDs as needed
    }

    for client_id, case_ids_to_add in client_case_data.items():
        update_query = """
            UPDATE clients 
            SET client_cases = client_cases || %s
            WHERE client_id = %s;
            """
        data_to_update = (case_ids_to_add, client_id)
        cursor.execute(update_query, data_to_update)

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()

    print("Sample data inserted successfully.")
except (Exception, psycopg2.Error) as error:
    print("Error inserting sample data:", error)
