import requests
import json

with open("jm/monday_api.txt", "r") as f:
    api_key = f.readline().strip()

with open("jm/monday_board_id.txt", "r") as f:
    board_id = f.readline().strip()

apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : api_key}

query = "{boards(ids:" + board_id + ") { name id description items { name column_values{title id type text } } } }"
data = {"query" : query}

r = requests.post(url=apiUrl, json=data, headers=headers)

if r.status_code == 200:
    

    response = r.json()
    for i in range(0, len(response["data"]["boards"][0]["items"])):
        data = response["data"]["boards"][0]["items"][i]
        new_dict = {'name': data['name']}
        new_dict.update({item['id']: item['text'] for item in data['column_values']})
        print(new_dict)
    
