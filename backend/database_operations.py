import psycopg2
import requests
import json
#Question for Wyman: Shouldn't the queries use placeholders instead of string concatenation to prevent SQL injection?

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


def create_user(username, name, email, password_hash, phone):
    connection = connect()
    cursor = connection.cursor()

    # Use a SQL query to insert a new user into the "users" table
    insert_query = """
    INSERT INTO users (username, name, email, password_hash, phone)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """

    try:
        cursor.execute(insert_query, (username, name, email, password_hash, phone))
        user_id = cursor.fetchone()[0]  # Get the ID of the newly created user
        connection.commit()
        return user_id
    except psycopg2.Error as e:
        print("Error creating a new user:", e)
        return None
    finally:
        cursor.close()
        connection.close()


def get_user_by_email(email):
    select_query = "SELECT id, username, email, role FROM users WHERE email = %s"
    user = None

    try:
        with psycopg2.connect('postgresql://postgres:mysecretpassword@localhost:5432/teradrive') as connection:
            with connection.cursor() as cursor:
                cursor.execute(select_query, (email,))
                user = cursor.fetchone()
    except psycopg2.Error as e:
        print("Error retrieving user by username:", e)

    return user


def get_user_by_id(user_id):
    select_query = "SELECT id, username, name, email, phone, role FROM users WHERE id = %s"
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
    select_query = "SELECT id, username, name, email, password_hash, phone, role FROM users WHERE username = %s"
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
    select_query = "SELECT id, username, name, email, phone, role FROM users ORDER BY id ASC"
    cursor.execute(select_query)
    records = []
    for row in cursor.fetchall():
        record = {
            'id': row[0],
            'username': row[1],
            'name': row[2],
            'email': row[3],
            'phone': row[4],
            'role': row[5]

        }
        records.append(record)

    cursor.close()
    connection.close()
    return records


def get_client_cases(client_email):
    connection = connect()
    cursor = connection.cursor()
    select_query = "SELECT case_id, case_status, case_work_progress, case_quote, case_notes" \
                   " FROM cases WHERE cases.client_email = '" + client_email + "' ORDER BY case_id ASC;"
    cursor.execute(select_query)
    records = cursor.fetchall()

    select_client_name = "SELECT name FROM users WHERE users.email = '" + client_email + "';"
    cursor.execute(select_client_name)
    client_name = cursor.fetchone()

    records.insert(0, client_name)

    cursor.close()
    connection.close()
    return records


def get_all_cases():
    conn = connect()
    cursor = conn.cursor()

    # Execute the SQL query to retrieve case information with client email
    query = """
        SELECT case_id, client_email, case_status, case_work_progress, case_quote, case_notes FROM cases;
        """
    cursor.execute(query)
    cases = cursor.fetchall()

    cursor.close()
    conn.close()
    return cases


def get_case_details(case_id):
    conn = connect()
    cursor = conn.cursor()

    query = """ SELECT * FROM cases WHERE case_id = %s; """
    cursor.execute(query, (case_id,))
    case = cursor.fetchall()

    cursor.close()
    conn.close()
    return case


def get_case_columns():
    conn = connect()
    cursor = conn.cursor()

    query = """
     SELECT column_name
     FROM information_schema.columns
      WHERE table_name = 'cases'
       ORDER BY ordinal_position ASC;
        """
    cursor.execute(query)
    columns = [column[0] for column in cursor.fetchall()]

    cursor.close()
    conn.close()
    return columns


def get_client_details(client_id):
    conn = connect()
    cursor = conn.cursor()

    query = """ SELECT id, username, name, email, phone, role FROM users WHERE id = %s; """

    cursor.execute(query, (client_id,))
    client_details = cursor.fetchall()
    cursor.close()
    conn.close()
    return client_details


def update_user_client(**kwargs):
    user_details = get_user_by_email(kwargs['email'])
    user_id = user_details[0]
    update_user(user_id, **kwargs)


def update_user(user_id, **kwargs):
    conn = connect()
    cursor = conn.cursor()

    update_query = f"""
            UPDATE users
            SET
                username = '{kwargs['username']}',
                password_hash = '{kwargs['password_hash']}',
                email = '{kwargs['email']}',
                phone = '{kwargs['phone']}',
                name = '{kwargs['name']}',
                role = {kwargs['role']}
            WHERE id = {user_id};
        """

    cursor.execute(update_query)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_monday():
    with open("jm/monday_api.txt", "r") as f:
        api_key = f.readline().strip()

    with open("jm/monday_board_id.txt", "r") as f:
        board_id = f.readline().strip()

    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization" : api_key}

    query = "{boards(ids:" + board_id + ") { name id description items { name column_values{title id type text } } } }"
    data = {"query" : query}

    r = requests.post(url=apiUrl, json=data, headers=headers)
    monday_data = []
    
    if r.status_code == 200:
        response = r.json()
        for i in range(0, len(response["data"]["boards"][0]["items"])):
            data = response["data"]["boards"][0]["items"][i]
            new_dict = {'name': data['name']}
            new_dict.update({item['id']: item['text'] for item in data['column_values']})
            temp = format_dict(**new_dict)
            monday_data.append(temp) 
        return monday_data
    else:
        print(f"Error: {r.status_code} - {r.text}")

def format_dict(**dict):
    perms = None

    if dict['permission_to_open'] == 'yes':
        perms = True
    
    if dict['email'] == '':
        placeholder = 'test@test.test'
    else:
        placeholder = dict['email']

    case = (
        placeholder,
        dict['drop_off'],
        dict['case_status'],
        dict['work_progress'],
        dict['malfunction'],
        dict['quote'],
        dict['type_of_device'],
        dict['important_folders'],
        dict['size'],
        perms,
        dict['date_received'],
        dict['date_quote_approved'],
        dict['date_completed'],
        dict['date_finalized'],
        dict['referred_by'],
        dict['notes']
    )

    # Replace empty strings with None
    case = tuple(None if value == '' else value for value in case)

    return case


def clear_cases():
    conn = connect()
    cursor = conn.cursor()

    delete_query = f"""
        DELETE FROM cases;
    """

    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()

def create_from_monday():
    #list of monday data
    monday_data = fetch_monday()
    clear_cases()
    conn = connect()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO cases (client_email, case_drop_off, case_status, case_work_progress,
            case_malfunction, case_quote, case_device_type, case_important_folders,
            case_size, case_permissions, case_date_recieved, case_date_quote_approved,
            case_completed_date, case_date_finalized, case_referred_by, case_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
    cursor.executemany(insert_query, monday_data)
    conn.commit()
    cursor.close()
    conn.close()

def create_case(cases_data):
    conn = connect()
    cursor = conn.cursor()

    # Execute the SQL query to insert a new case
    insert_cases_query = """
            INSERT INTO cases (client_email, case_drop_off, case_status, case_work_progress,
            case_malfunction, case_quote, case_device_type, case_important_folders,
            case_size, case_permissions, case_date_recieved, case_date_quote_approved,
            case_completed_date, case_date_finalized, case_referred_by, case_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    cursor.execute(insert_cases_query, cases_data)
    conn.commit()
    cursor.close()
    conn.close()


def update_case(**kwargs):
    conn = connect()
    cursor = conn.cursor()

    update_query = f"""
        UPDATE cases 
        SET 
            client_email = '{kwargs['client_email']}',
            case_drop_off = '{kwargs['case_drop_off']}',
            case_status = '{kwargs['case_status']}',
            case_work_progress = '{kwargs['case_work_progress']}',
            case_malfunction = '{kwargs['case_malfunction']}',
            case_quote = {kwargs['case_quote']},
            case_device_type = '{kwargs['case_device_type']}',
            case_important_folders = '{kwargs['case_important_folders']}',
            case_size = '{kwargs['case_size']}',
            case_permissions = {kwargs['case_permissions']},
            case_date_recieved = '{kwargs['case_date_recieved']}',
            case_date_quote_approved = '{kwargs['case_date_quote_approved']}',
            case_completed_date = '{kwargs['case_completed_date']}',
            case_date_finalized = '{kwargs['case_date_finalized']}',
            case_referred_by = '{kwargs['case_referred_by']}',
            case_notes = '{kwargs['case_notes']}'
        WHERE case_id = {kwargs['case_id']};
    """

    cursor.execute(update_query)
    conn.commit()
    cursor.close()
    conn.close()


def delete_case(case_id):
    conn = connect()
    cursor = conn.cursor()

    delete_query = f"""
        DELETE FROM cases
        WHERE case_id = {case_id};
    """

    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()
