import tkinter as tk
from tkinter import messagebox

from data_handler import load_users, save_users
from models import User


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
            messagebox.showinfo("Login Success", "Login successful! (Dashboard coming soon)")
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

if __name__ == "__main__":
    root = tk.Tk()
    app = RevisionPlannerApp(root)
    root.mainloop()