from datetime import datetime, timedelta


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

    @staticmethod #means this method belongs to the class itself, not to any particular object
    def from_dict(data):
        task = Task(data["title"], data["subject"], data["deadline"], data["duration"], data["confidence_rating"])
        task.id = data["id"]
        task.completed = data["completed"]
        task.reminder_sent = data["reminder_sent"]
        return task

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

    @staticmethod
    def from_dict(data):
        settings = Settings()
        settings.theme = data["theme"]
        settings.font_size = data["font_size"]
        settings.high_contrast = data["high_contrast"]
        settings.reminders_enabled = data["reminders_enabled"]
        settings.reminder_days = data["reminder_days"]
        return settings


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []
        self.sessions = [] #somewhere to store sessions
        self.settings = Settings()

    def add_task(self, task):
        self.tasks.append(task)

    def add_session(self, session): #method to record sessions
        self.sessions.append(session)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "tasks": [task.to_dict() for task in self.tasks],
            "sessions": [session.to_dict() for session in self.sessions], #update to include sessions
            "settings": self.settings.to_dict()
        }

    @staticmethod
    def from_dict(data):
        user = User(data["username"], data["password"])
        user.tasks = [Task.from_dict(t) for t in data["tasks"]]
        user.sessions = [StudySession.from_dict(s) for s in data["sessions"]]
        user.settings = Settings.from_dict(data["settings"])
        return user

class StudySession:
    def __init__(self, task_id, start_time, end_time):
        self.id = None
        self.task_id = task_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = self.calculate_duration()

    def calculate_duration(self):
        return int((self.end_time - self.start_time).total_seconds() // 60) #makes it a whole number

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "start_time": self.start_time.isoformat(), #save times in a format fromisoformaat can read (it's a method on Python's datetime objects that converts a date/time into a standard text format like "2026-08-31T14:23:05.123456")
            "end_time": self.end_time.isoformat(),
            "duration": self.duration
        }

    @staticmethod
    def from_dict(data):
        session = StudySession(
            task_id=data["task_id"],
            start_time=datetime.fromisoformat(data["start_time"]), #needs to convert the time strings into real datetime objects
            end_time=datetime.fromisoformat(data["end_time"])
        )
        session.id = data["id"]
        return session

if __name__ == "__main__":
    test_user = User("alex123", "revisegood2026")
    test_task = Task("Chemistry - Bonding", "Chemistry", "31/08/2026", 45, confidence_rating=4)
    test_user.add_task(test_task)

    start = datetime.now()
    end = start + timedelta(minutes=42)
    test_session = StudySession(task_id=test_task.id, start_time=start, end_time=end)
    test_user.add_session(test_session)

    print(test_user.to_dict())