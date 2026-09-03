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

if __name__ == "__main__":
    test_task = Task("Chemistry - Bonding", "Chemistry", "31/08/2026", 45, confidence_rating=4)
    print(test_task.to_dict())