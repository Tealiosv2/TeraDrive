import psycopg2


def connect():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="teradrive",
            user="postgres",
            password="mysecretpassword",
            port=5432)

        # Create a cursor object to interact with the database

        return connection

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)


def create_user(username, email, password_hash, phone):
    connection = connect()
    cursor = connection.cursor()

    # Use a SQL query to insert a new user into the "users" table
    insert_query = """
    INSERT INTO users (username, email, password_hash, phone)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """

    try:
        cursor.execute(insert_query, (username, email, password_hash, phone))
        user_id = cursor.fetchone()[0]  # Get the ID of the newly created user
        connection.commit()
        return user_id
    except psycopg2.Error as e:
        print("Error creating a new user:", e)
        return None
    finally:
        connection.close()


def get_user_by_id(user_id):
    select_query = "SELECT id, username, role FROM users WHERE id = %s"
    user = None

    try:
        with psycopg2.connect('postgresql://postgres:mysecretpassword@localhost:5432/teradrive') as connection:
            with connection.cursor() as cursor:
                cursor.execute(select_query, (user_id,))
                user = cursor.fetchone()
    except psycopg2.Error as e:
        print("Error retrieving user by ID:", e)

    return user  # Returns the user's information if found, or None if not found


def get_user_by_username(username):
    select_query = "SELECT id, username, password_hash, role FROM users WHERE username = %s"
    user = None

    try:
        with psycopg2.connect('postgresql://postgres:mysecretpassword@localhost:5432/teradrive') as connection:
            with connection.cursor() as cursor:
                cursor.execute(select_query, (username,))
                user = cursor.fetchone()
    except psycopg2.Error as e:
        print("Error retrieving user by username:", e)

    return user



def get_clients():
    connection = connect()
    cursor = connection.cursor()
    select_query = "SELECT * FROM clients ORDER BY client_id ASC"
    cursor.execute(select_query)
    records = []
    for row in cursor.fetchall():
        record = {
            'client_email': row[0],
            'client_id': row[1],
            'client_name': row[2],
            'client_phone': row[3]
        }
        records.append(record)
    connection.close()
    return records


def get_client_cases(client_email):
    connection = connect()
    cursor = connection.cursor()
    select_query = "SELECT case_id, case_status, case_work_progress, case_quote, case_notes" \
                   " FROM cases WHERE cases.client_email = '" + client_email + "' ORDER BY case_id ASC;"
    cursor.execute(select_query)
    records = cursor.fetchall()

    select_client_name = "SELECT client_name FROM clients WHERE clients.client_email = '" + client_email + "';"
    cursor.execute(select_client_name)
    client_name = cursor.fetchone()

    records.insert(0, client_name)

    connection.close()
    return records


def get_all_cases():
    conn = connect()
    cursor = conn.cursor()

    # Execute the SQL query to retrieve case information with client email
    query = """
        SELECT case_id, client_email case_status, case_work_progress, case_quote, case_notes FROM cases;
        """
    cursor.execute(query)
    cases = cursor.fetchall()

    conn.close()
    return cases


def get_case_details(case_id):
    return 0


def create_case(client_id, case_status, case_notes):
    conn = connect()
    cursor = conn.cursor()

    # Execute the SQL query to insert a new case
    query = f"""
        INSERT INTO cases (client_id, case_status, case_notes)
        VALUES ({client_id}, '{case_status}', '{case_notes}')
        """
    cursor.execute(query)
    conn.commit()

    conn.close()
