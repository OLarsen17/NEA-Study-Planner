import tkinter as tk
from tkinter import messagebox

from data_handler import load_users, save_users
from models import User, Task

from datetime import datetime

from tkinter import ttk




class RevisionPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Revision Planner")
        self.root.geometry("500x400")

        self.show_welcome_screen()

    def clear_screen(self): #removes current screen so user can move onto next
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_screen()

        title_label = tk.Label(self.root, text="Revision Planner", font=("Segoe UI", 20))
        title_label.pack(pady=20) #spacing

        subtitle_label = tk.Label(self.root, text="Study Smarter")
        subtitle_label.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.show_login_screen)
        login_button.pack(pady=10)

        create_account_button = tk.Button(self.root, text="Create Account", command=self.show_create_account_screen)
        create_account_button.pack(pady=5)

    def show_login_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Login", font=("Segoe UI", 16))
        label.pack(pady=10)

        username_label = tk.Label(self.root, text="Username")
        username_label.pack()

        self.username_entry = tk.Entry(self.root) #reads whatever user entered
        self.username_entry.pack(pady=5)

        continue_button = tk.Button(self.root, text="Continue", command=self.check_username)
        continue_button.pack(pady=10)

    def check_username(self):
        entered_username = self.username_entry.get()

        if entered_username == "":
            messagebox.showerror("Login Error", "Username cannot be blank.") #brings up a new window for errors
            return

        users = load_users()
        matched_user = None

        for user in users:
            if user.username == entered_username:
                matched_user = user

        if matched_user is None:
            messagebox.showerror("Login Error", "No account was found with that username. Check your spelling or create a new account.")
            return

        self.pending_user = matched_user
        self.show_password_screen()

    def show_password_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text=f"Welcome back, {self.pending_user.username}", font=("Segoe UI", 16))
        label.pack(pady=10)

        password_label = tk.Label(self.root, text="Password")
        password_label.pack()

        self.password_entry = tk.Entry(self.root, show="*") #make sure password is not shown and shows * instead
        self.password_entry.pack(pady=5)

        continue_button = tk.Button(self.root, text="Continue", command=self.check_password)
        continue_button.pack(pady=10)

    def check_password(self):
        entered_password = self.password_entry.get()

        if entered_password == self.pending_user.password:
            self.show_dashboard()
        else:
            messagebox.showerror("Login Error", "That password isn't right. Please try again.")

    def show_create_account_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Create Account", font=("Segoe UI", 16))
        label.pack(pady=10)

        username_label = tk.Label(self.root, text="Username")
        username_label.pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack(pady=5)

        password_label = tk.Label(self.root, text="Password")
        password_label.pack()
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack(pady=5)

        confirm_label = tk.Label(self.root, text="Confirm Password")
        confirm_label.pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.pack(pady=5)

        create_button = tk.Button(self.root, text="Create Account", command=self.create_account)
        create_button.pack(pady=10)

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Account Error", "Username and password cannot be blank.")
            return

        if len(password) < 8: #has to be longer than 8 for security
            messagebox.showerror("Account Error", "Password must be at least 8 characters.")
            return

        if password != confirm_password:
            messagebox.showerror("Account Error", "Passwords do not match.")
            return

        users = load_users()
        for user in users:
            if user.username == username:
                messagebox.showerror("Account Error", "That username is already taken. Please choose another.")
                return

        new_user = User(username, password)
        users.append(new_user)
        save_users(users)

        messagebox.showinfo("Account Created", "Account created successfully! You can now log in.")
        self.show_welcome_screen()

    def show_dashboard(self):
        self.clear_screen()

        welcome_label = tk.Label(self.root, text=f"Welcome back, {self.pending_user.username}", font=("Segoe UI", 16))
        welcome_label.pack(pady=10)

        subtitle_label = tk.Label(self.root, text="Here's what's coming up")
        subtitle_label.pack()

        deadlines_label = tk.Label(self.root, text="Upcoming Deadlines", font=("Segoe UI", 12))
        deadlines_label.pack(pady=10)

        upcoming_tasks = self.get_upcoming_tasks()

        if not upcoming_tasks: #makes sure it doesnt crash if user has no tasks
            no_tasks_label = tk.Label(self.root, text="No upcoming deadlines")
            no_tasks_label.pack()
        else:
            for task, days_remaining in upcoming_tasks:
                if days_remaining < 0:
                    urgency_text = "Overdue"
                elif days_remaining == 0:
                    urgency_text = "Due today"
                elif days_remaining == 1:
                    urgency_text = "Due tomorrow"
                else:
                    urgency_text = f"{days_remaining} days left"

                task_text = f"{task.title} — Due {task.deadline} — {urgency_text}"
                task_label = tk.Label(self.root, text=task_text)
                task_label.pack()

        add_task_button = tk.Button(self.root, text="+ Add new task", command=self.show_add_task_screen) #add task button
        add_task_button.pack(pady=10)

        view_tasks_button = tk.Button(self.root, text="View all tasks", command=self.show_task_list_screen)
        view_tasks_button.pack(pady=5)

    def get_upcoming_tasks(self):
        upcoming = []
        today = datetime.now().date()

        for task in self.pending_user.tasks:
            if task.completed:
                continue

            deadline_date = datetime.strptime(task.deadline, "%d/%m/%Y").date() #formats it nicely
            days_remaining = (deadline_date - today).days

            upcoming.append((task, days_remaining)) #stored as tuples because needed for sorting

        upcoming.sort(key=lambda item: item[1]) #sorts in order of urgency
        return upcoming

    def show_add_task_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Add New Task", font=("Segoe UI", 16))
        label.pack(pady=10)

        title_label = tk.Label(self.root, text="Task Title")
        title_label.pack()
        self.task_title_entry = tk.Entry(self.root)
        self.task_title_entry.pack(pady=5)

        subject_label = tk.Label(self.root, text="Subject")
        subject_label.pack()
        existing_subjects = self.get_existing_subjects()
        self.task_subject_entry = ttk.Combobox(self.root, values=existing_subjects)
        self.task_subject_entry.pack(pady=5)

        deadline_label = tk.Label(self.root, text="Deadline (DD/MM/YYYY)")
        deadline_label.pack()
        self.task_deadline_entry = tk.Entry(self.root)
        self.task_deadline_entry.pack(pady=5)

        duration_label = tk.Label(self.root, text="Estimated Study Time (mins)")
        duration_label.pack()
        self.task_duration_entry = tk.Entry(self.root)
        self.task_duration_entry.pack(pady=5)

        confidence_label = tk.Label(self.root, text="Confidence Rating (1-5)")
        confidence_label.pack()
        self.task_confidence_entry = tk.Entry(self.root)
        self.task_confidence_entry.pack(pady=5)

        save_button = tk.Button(self.root, text="Save Task", command=self.save_task)
        save_button.pack(pady=10)

        cancel_button = tk.Button(self.root, text="Cancel", command=self.show_dashboard)
        cancel_button.pack(pady=5)

    def get_existing_subjects(self):
        subjects = []
        for task in self.pending_user.tasks:
            if task.subject not in subjects:
                subjects.append(task.subject)
        return subjects

    def save_task(self):
        title = self.task_title_entry.get()
        subject = self.task_subject_entry.get()
        deadline = self.task_deadline_entry.get()
        duration_text = self.task_duration_entry.get()
        confidence_text = self.task_confidence_entry.get()

        if title == "" or subject == "":
            messagebox.showerror("Add Task Error", "Task title and subject cannot be blank.")
            return

        try: #try/except to prevent crashing
            datetime.strptime(deadline, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Add Task Error", "Deadline must be in the format DD/MM/YYYY.")
            return

        if not duration_text.isdigit() or int(duration_text) <= 0:
            messagebox.showerror("Add Task Error", "Duration must be a positive number.")
            return

        if not confidence_text.isdigit() or not (1 <= int(confidence_text) <= 5): #makes sure if user types a letter it doesnt crash
            messagebox.showerror("Add Task Error", "Confidence rating must be between 1 and 5.")
            return

        new_task = Task(title, subject, deadline, int(duration_text), int(confidence_text))
        self.pending_user.tasks.append(new_task)

        users = load_users()
        for i, user in enumerate(users):
            if user.username == self.pending_user.username:
                users[i] = self.pending_user

        save_users(users)

        messagebox.showinfo("Task Added", "Task added successfully!")
        self.show_dashboard()

    def show_task_list_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Your Tasks", font=("Segoe UI", 16))
        label.pack(pady=10)

        self.sort_var = tk.StringVar(value="Deadline") #
        self.filter_var = tk.StringVar(value="Incomplete Only")

        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=5)

        sort_menu = tk.OptionMenu(controls_frame, self.sort_var, "Deadline", "Name", "Duration", command=lambda _: self.refresh_task_list()) #dropdown widget
        sort_menu.pack(side="left", padx=5)

        filter_menu = tk.OptionMenu(controls_frame, self.filter_var, "Incomplete Only", "Complete Only", "All", command=lambda _: self.refresh_task_list())
        filter_menu.pack(side="left", padx=5)

        self.task_list_frame = tk.Frame(self.root)
        self.task_list_frame.pack(pady=10)

        self.refresh_task_list() #refreshes what was sorted

        back_button = tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard)
        back_button.pack(pady=10)

    def refresh_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        tasks = self.pending_user.tasks

        filter_choice = self.filter_var.get()
        if filter_choice == "Incomplete Only":
            tasks = [t for t in tasks if not t.completed]
        elif filter_choice == "Complete Only":
            tasks = [t for t in tasks if t.completed]

        sort_choice = self.sort_var.get()
        if sort_choice == "Deadline":
            tasks = sorted(tasks, key=lambda t: datetime.strptime(t.deadline, "%d/%m/%Y"))
        elif sort_choice == "Name":
            tasks = sorted(tasks, key=lambda t: t.title)
        elif sort_choice == "Duration":
            tasks = sorted(tasks, key=lambda t: t.duration)

        if not tasks:
            no_tasks_label = tk.Label(self.task_list_frame, text="No tasks to show")
            no_tasks_label.pack()

        for task in tasks:
            row = tk.Frame(self.task_list_frame)
            row.pack(fill="x", pady=2)

            info_text = f"{task.title} — {task.subject} — Due {task.deadline}"
            info_label = tk.Label(row, text=info_text)
            info_label.pack(side="left", padx=5)

            edit_button = tk.Button(row, text="Edit", command=lambda t=task: self.show_edit_task_screen(t))
            edit_button.pack(side="right", padx=2)

            delete_button = tk.Button(row, text="Delete", command=lambda t=task: self.confirm_delete_task(t))
            delete_button.pack(side="right", padx=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = RevisionPlannerApp(root)
    root.mainloop()