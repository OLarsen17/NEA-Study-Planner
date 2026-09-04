import tkinter as tk
from tkinter import messagebox

from data_handler import load_users, save_users
from models import User

from datetime import datetime


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

if __name__ == "__main__":
    root = tk.Tk()
    app = RevisionPlannerApp(root)
    root.mainloop()