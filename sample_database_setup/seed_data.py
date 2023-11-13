import psycopg2
import random

names = [
    "John Doe",
    "Jane Smith",
    "Alice Johnson",
    "Bob Wilson",
    "Susan White",
    "David Brown",
    "Emily Jackson",
    "Sam Roberts",
    "Lisa Davis",
    "Michael Thomas",
    "Olivia Harris",
    "William Martin",
    "Sophia Lee",
    "James Anderson",
    "Oliver Wright"
]
emails = [
    "john.doe@example.com",
    "jane.smith@gmail.com",
    "alice.johnson@yahoo.com",
    "bob.wilson@hotmail.com",
    "susan.white@outlook.com",
    "david.brown@gmail.com",
    "emily.jackson@example.com",
    "sam.roberts@yahoo.com",
    "lisa.davis@hotmail.com",
    "michael.thomas@example.com",
    "olivia.harris@gmail.com",
    "william.martin@yahoo.com",
    "sophia.lee@outlook.com",
    "james.anderson@gmail.com",
    "oliver.wright@example.com"
]

phone_numbers = [
    "+1 (123) 456-7890",
    "+1 (234) 567-8901",
    "+1 (345) 678-9012",
    "+1 (456) 789-0123",
    "+1 (567) 890-1234",
    "+1 (678) 901-2345",
    "+1 (789) 012-3456",
    "+1 (890) 123-4567",
    "+1 (901) 234-5678",
    "+1 (012) 345-6789",
    "+1 (123) 234-5678",
    "+1 (234) 345-6789",
    "+1 (345) 456-7890",
    "+1 (456) 567-8901",
    "+1 (567) 678-9012"
]
# Database connection parameters
db_params = {
    "user": "postgres",
    "password": "mysecretpassword",  # Replace with your PostgreSQL password
    "host": "localhost",  # Docker container is running on your local machine
    "port": "5432",  # Default PostgreSQL port
    "database": "teradrive"  # Replace with your database name (teradrive)
}


def rand_quote():
    random_number = random.randint(100, 2000)
    rounded_number = round(random_number / 50) * 50
    return rounded_number


try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_params)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Sample data for the 'clients' table
    clients_data = [(email, name, phone_number) for name, email, phone_number in zip(names, emails, phone_numbers)]

    # Insert sample data into the 'clients' table
    insert_clients_query = """
        INSERT INTO clients (client_email, client_name, client_phone)
        VALUES (%s, %s, %s);
    """
    cursor.executemany(insert_clients_query, clients_data)

    case_statuses = ["Confirmed", "Declined", "Quote Sent", "Evaluating", "En Route", "Closed", "Evaluation Complete",
                     "Unrecoverable", "Completed"]

    case_progresses = ["Waiting for parts", "Files sent", "In progress", "Completed", "Closed", "File list sent",
                       "Cloning", "Waiting for drive", "Copying files", "Invoice sent", "Approved", "Paid", "Shipped",
                       "Reasearch", "Super Rush"]

    cases_data = []

    # Sample data for the 'cases' table
    for i in range(25):
        case = (random.choice(emails),
                random.choice(["Vancouver", "Burnaby", "Langley"]),
                random.choice(case_statuses), random.choice(case_progresses),
                random.choice(["Bad heads", "Electrical", "Bad sectors", "Deleted files", "Water damage", "Other"]),
                rand_quote(), random.choice(["HDD", "SSD", "Flash Drive", "SD Card", "Other", "Laptop"]),
                "None",
                random.choice(["1TB", "2TB", "3TB", "4TB", "5TB", "6TB", "7TB", "8TB", "9TB", "10TB", "11TB", "12"]),
                random.choice([True, False]),
                random.choice(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05", "2020-01-06", ]),
                random.choice(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05", "2020-01-06", ]),
                random.choice(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05", "2020-01-06", ]),
                random.choice(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05", "2020-01-06", ]),
                random.choice(["Google", "Yelp", "Facebook", "Friend", "Other"]), "None"
                )
        cases_data.append(case)

    insert_cases_query = """
        INSERT INTO cases ( client_email, case_drop_off, case_status, case_work_progress,
        case_malfunction, case_quote, case_device_type, case_important_folders,
        case_size, case_permissions, case_date_recieved, case_date_quote_approved,
        case_completed_date, case_date_finalized, case_referred_by, case_notes)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
