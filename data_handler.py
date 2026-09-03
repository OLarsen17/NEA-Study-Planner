import json
import os
from models import User, Task, StudySession, Settings

DATA_FILE = "data/users.json"


def save_users(users):
    data = [user.to_dict() for user in users]
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4) #makes the JSON file easier to read


def load_users(): #just empty simplified version
    if not os.path.exists(DATA_FILE): #checks wether JSON file exists so it doesnt crash first time run
        return []

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    users = []
    for user_data in data:
        user = User(user_data["username"], user_data["password"])
        users.append(user)

    return users

if __name__ == "__main__":
    test_user = User("user123", "testpassword123")
    save_users([test_user])

    loaded = load_users()
    print(loaded[0].to_dict())