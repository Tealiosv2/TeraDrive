import database_operations


#test get clients
# records = database_operations.get_clients()

#test get_client_cases
# records = database_operations.get_client_cases('aa@aa.aa')

#test get_all_cases
# records = database_operations.get_all_cases()

#test get_client_details
records = database_operations.get_client_details(3)

#test get by user
records = database_operations.get_user_by_username('user')

#test update
# updates = {
#     'username': 'admin',
#     'name': 'adam',
#     'email': 'aa@aa.aa',
#     'role': 'True',
#     'phone': '123456789'
# }
#
# database_operations.update_user_client(**updates)



print(records)


