import database_operations

case_data = ("david.brown@gmail.com", "2021-04-01", "In Progress", "In Progress",
             "No Power", 100, "MacBook Pro", "No", "1TB", True, "2021-04-01", "2021-04-01",
             "2021-04-01", "2021-04-01", "Google", "No Notes")

database_operations.create_case(case_data)

records = database_operations.get_all_cases()

for r in records:
    print(r)
