class Task:
    def __init__(self, title, subject, deadline, duration, confidence_rating=3): #default confidence to 3 so it doesnt crash (middle confidence)
        self.id = None
        self.title = title
        self.subject = subject
        self.deadline = deadline
        self.duration = duration
        self.confidence_rating = confidence_rating
        self.completed = False #defaulted to False becasue it hasnt happened yet
        self.reminder_sent = False #defaulted to False becasue it hasnt happened yet

    def mark_complete(self):
        self.completed = True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "deadline": self.deadline,
            "duration": self.duration,
            "confidence_rating": self.confidence_rating,
            "completed": self.completed,
            "reminder_sent": self.reminder_sent
        }

class Settings: #simple version to be reference from user
    def __init__(self):
        self.theme = "light"
        self.font_size = "medium"
        self.high_contrast = False
        self.reminders_enabled = True
        self.reminder_days = 3

    def to_dict(self):
        return {
            "theme": self.theme,
            "font_size": self.font_size,
            "high_contrast": self.high_contrast,
            "reminders_enabled": self.reminders_enabled,
            "reminder_days": self.reminder_days
        }


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []
        self.settings = Settings()

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "tasks": [task.to_dict() for task in self.tasks],
            "settings": self.settings.to_dict()
        }

if __name__ == "__main__":
    test_user = User("user123", "testpassword123")
    test_task = Task("Chemistry - Bonding", "Chemistry", "31/08/2026", 45, confidence_rating=4)
    test_user.add_task(test_task)
    print(test_user.to_dict())