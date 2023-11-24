import psycopg2
from werkzeug.security import generate_password_hash

# Database connection parameters
db_params = {
    "user": "postgres",
    "password": "mysecretpassword",  # Replace with your PostgreSQL password
    "host": "localhost",  # Docker container is running on your local machine
    "port": "5432",  # Default PostgreSQL port
    "database": "teradrive"  # Replace with your database name
}

# Admin user details
admin_username = "admin"
admin_email = "aa@aa.aa"
name = "admin"
admin_password_hash = generate_password_hash("P@$$w0rd")  # Hash the admin's password
phone = "1234567890"
admin_role = True  # Assuming role is a boolean field

# SQL query to insert the admin user
insert_query = """
INSERT INTO users (username, name, email, password_hash, phone, role)
VALUES (%s, %s,%s, %s,%s, %s);
"""

# Connect to the database and execute the query
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    cursor.execute(insert_query, (admin_username, name, admin_email, admin_password_hash,phone, admin_role))
    connection.commit()
    cursor.close()
    connection.close()
    print("Admin user added successfully.")
except psycopg2.Error as e:
    print("Error adding admin user:", e)

