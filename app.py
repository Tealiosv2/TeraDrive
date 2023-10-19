from flask import Flask, render_template, request
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
def get_clients():
    clients_records = database_operations.get_clients()
    return render_template('clients.html', records=clients_records)

@app.route('/client_cases')
def get_client_cases():
    client_email = request.args.get('client_email')

    client_case_data = database_operations.get_client_cases(client_email)
    return render_template('client_cases.html', client_case_data=client_case_data)


@app.route('/cases')
def display_cases():
    cases = database_operations.get_all_cases()

    return render_template('cases.html', cases=cases)

@app.route('/case_details')
def display_case_details():
    case_id = request.args.get('case_id')

    case_details = database_operations.get_case_details(case_id)

    return render_template('case_details.html', case_details=case_details)

if __name__ == '__main__':
    app.run(debug=True)
