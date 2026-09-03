import json
import os
from models import User, Task, StudySession, Settings
from datetime import datetime, timedelta

DATA_FILE = "data/users.json"


def save_users(users):
    data = [user.to_dict() for user in users]
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4) #makes the JSON file easier to read


def load_users():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    return [User.from_dict(user_data) for user_data in data]

if __name__ == "__main__":
    test_user = User("user123", "testpassword123")
    test_task = Task("Chemistry - Bonding", "Chemistry", "31/08/2026", 45, confidence_rating=4)
    test_user.add_task(test_task)

    start = datetime.now()
    end = start + timedelta(minutes=42)
    test_session = StudySession(task_id=test_task.id, start_time=start, end_time=end)
    test_user.add_session(test_session)

    save_users([test_user])
    loaded = load_users()
    print(loaded[0].to_dict())