import psycopg2

# Establish a database connection
connection = psycopg2.connect(
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432",
    database="teradrive"
)

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# Define the SQL command to create the user table
create_user_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    role BOOLEAN NOT NULL DEFAULT FALSE
);
"""

# Execute the SQL command to create the table
cursor.execute(create_user_table)

# Commit the changes to the database
connection.commit()

# Close the cursor and database connection
cursor.close()
connection.close()
