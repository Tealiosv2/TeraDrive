import database_operations

records = database_operations.get_all_cases()

for r in records:
    print(r)