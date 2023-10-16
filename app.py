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
    cases = database_operations.get_cases()

    return render_template('cases.html', cases=cases)

if __name__ == '__main__':
    app.run(debug=True)
