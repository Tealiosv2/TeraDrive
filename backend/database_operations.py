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
