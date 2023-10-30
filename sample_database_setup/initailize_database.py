import subprocess

subprocess.run(["python", "delete_cases.py"])
subprocess.run(["python", "delete_clients.py"])
subprocess.run(["python", "drop_cases.py"])
subprocess.run(["python", "drop_clients.py"])
subprocess.run(["python", "drop_user.py"])
subprocess.run(["python", "create_tables.py"])
subprocess.run(["python", "create_users_table.py"])
subprocess.run(["python", "add_users.py"])
subprocess.run(["python", "seed_data.py"])
subprocess.run(["python", "view_clients.py"])
subprocess.run(["python", "view_cases.py"])
subprocess.run(["python", "view_users.py"])
