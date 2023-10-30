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
    print(f"{'Name':<15} {'Case Number':<15} {'Phone':<15} {'Email':<25} {'Drop off':<15} {'Case Status':<15} {'Work Progress':<15}")
    print("=" * 120)

    response = r.json()
    for item in response["data"]["boards"][0]["items"]:
        case_number = ""
        phone_number = ""
        email = ""
        drop_off = ""
        case_status = ""
        work_progress = ""
        for column in item["column_values"]:
            if column["title"] == "Case Number":
                case_number = column["text"] if column["text"] else "None"
            if column["title"] == "Phone Number":
                phone_number = column["text"] if column["text"] else "None"
            if column["title"] == "Email":
                email = column["text"] if column["text"] else "None"
            if column["title"] == "Drop off":
                drop_off = column["text"] if column["text"] else "None"
            if column["title"] == "Case Status":
                case_status = column["text"] if column["text"] else "None"
            if column["title"] == "Work Progress":
                work_progress = column["text"] if column["text"] else "None"
        print(f"{item['name'][:15]:<15} {case_number[:15].ljust(15)} {phone_number[:15].ljust(15)} {email[:25].ljust(25)} {drop_off[:15].ljust(15)} {case_status[:15].ljust(15)} {work_progress[:15].ljust(15)}")
else:
    print(f"Error: {r.status_code} - {r.text}")