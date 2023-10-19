import database_operations

records = database_operations.get_client_cases("john.doe@example.com")

for r in records:
    print(r)