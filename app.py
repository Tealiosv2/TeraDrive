from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    connection = psycopg2.connect(
        user="postgres",
        password="mysecretpassword",  # Use the password you set for the PostgreSQL container
        host="localhost",  # Docker container is running on your local machine
        port="5432",  # Default PostgreSQL port
        database="mydatabase"  # Replace with your database name
    )
    return connection

@app.route('/')
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM your_table")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return str(data)
    except (Exception, psycopg2.Error) as error:
        return str(error)

if __name__ == '__main__':
    app.run(debug=True)
