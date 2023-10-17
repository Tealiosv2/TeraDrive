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
            'client_id': row[0],
            'client_email': row[1],
            'client_name': row[2],
            'client_cases': row[3]
        }
        records.append(record)
    connection.close()
    return records

def get_cases():
    conn = connect()
    cursor = conn.cursor()

    # Execute the SQL query to retrieve case information with client email
    query = """
        SELECT c.case_id, c.case_status, c.case_notes, cl.client_email
        FROM cases c
        JOIN clients cl ON c.client_id = cl.client_id
        """
    cursor.execute(query)
    cases = cursor.fetchall()

    conn.close()
    return cases

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
