import database_operations



records = database_operations.get_user_by_email('aa@aa.aa')

for r in records:
    print(r)
