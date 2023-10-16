from flask import Flask, render_template
import psycopg2
from backend import database_operations

app = Flask(__name__)

def get_db_connection():
    connection = psycopg2.connect(
        user="postgres",
        password="mysecretpassword",  # Use the password you set for the PostgreSQL container
        host="localhost",  # Docker container is running on your local machine
        port="5432",  # Default PostgreSQL port
        database="teradrive"  # Replace with your database name
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clients')
def get_cases():
    clients_records = database_operations.get_clients()
    return render_template('clients.html', records=clients_records)

@app.route('/cases')
def display_cases():
    conn = database_operations.connect()
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

    return render_template('cases.html', cases=cases)

if __name__ == '__main__':
    app.run(debug=True)
