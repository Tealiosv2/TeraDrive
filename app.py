from flask import Flask, render_template
import psycopg2

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

if __name__ == '__main__':
    app.run(debug=True)
