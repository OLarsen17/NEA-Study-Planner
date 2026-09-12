import tkinter as tk
from tkinter import messagebox

from data_handler import load_users, save_users
from models import User, Task, StudySession

from datetime import datetime, timedelta

from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg





class RevisionPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Revision Planner")
        self.root.geometry("500x400")
        self.current_week_start = None

        self.show_welcome_screen()

    def clear_screen(self): #removes current screen so user can move onto next
        for widget in self.root.winfo_children():
            widget.destroy()

    #-----LOGIN-----#

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
        self.username_entry.bind("<Return>", lambda event: self.check_username())

        continue_button = tk.Button(self.root, text="Continue", command=self.check_username)
        continue_button.pack(pady=10)

        create_account_link = tk.Button(self.root, text="Don't have an account? Create one", command=self.show_create_account_screen)
        create_account_link.pack(pady=5)

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
        self.password_entry.bind("<Return>", lambda event: self.check_password())

        self.show_password_var = tk.BooleanVar(value=False)
        show_password_check = tk.Checkbutton(self.root, text="Show password", variable=self.show_password_var, command=self.toggle_password_visibility)
        show_password_check.pack()

        continue_button = tk.Button(self.root, text="Continue", command=self.check_password)
        continue_button.pack(pady=10)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

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
        self.confirm_password_entry.bind("<Return>", lambda event: self.create_account())

        self.show_create_password_var = tk.BooleanVar(value=False)
        show_create_password_check = tk.Checkbutton(self.root, text="Show password", variable=self.show_create_password_var, command=self.toggle_create_password_visibility)
        show_create_password_check.pack()

        create_button = tk.Button(self.root, text="Create Account", command=self.create_account)
        create_button.pack(pady=10)

        login_link = tk.Button(self.root, text="Already have an account? Log in", command=self.show_login_screen)
        login_link.pack(pady=5)

    def toggle_create_password_visibility(self):
        if self.show_create_password_var.get():
            self.new_password_entry.config(show="")
            self.confirm_password_entry.config(show="")
        else:
            self.new_password_entry.config(show="*")
            self.confirm_password_entry.config(show="*")

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

    #-----DASHBOARD-----#

    def show_dashboard(self):
        self.check_reminders()
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

        timer_button = tk.Button(self.root, text="Study Timer", command=self.show_timer_task_select_screen)
        timer_button.pack(pady=5)

        settings_button = tk.Button(self.root, text="Settings", command=self.show_settings_screen)
        settings_button.pack(pady=5)

        #test_stats_button = tk.Button(self.root, text="TEST: Print stats", command=self.print_test_statistics)
        #test_stats_button.pack(pady=5)

        statistics_button = tk.Button(self.root, text="Statistics", command=self.show_statistics_screen)
        statistics_button.pack(pady=5)

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
        self.task_confidence_entry = ttk.Spinbox(self.root, from_=1, to=5, width=5, state="readonly")
        self.task_confidence_entry.set(3)
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

        date_parts = deadline.split("/")

        if len(date_parts) != 3 or not all(part.isdigit() for part in date_parts):
            messagebox.showerror("Add Task Error", "Deadline must be in the format DD/MM/YYYY.")
            return

        day, month, year = date_parts

        if len(year) != 4:
            messagebox.showerror("Add Task Error", "Deadline must be in the format DD/MM/YYYY.")
            return

        try:
            datetime.strptime(deadline, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Add Task Error", "That date doesn't exist. Please check the day and month.")
            return

        new_task = Task(title, subject, deadline, int(duration_text), int(confidence_text))
        self.pending_user.tasks.append(new_task)

        self.save_current_user()

        messagebox.showinfo("Task Added", "Task added successfully!")
        self.show_dashboard()

    #-----TASKS SCREEN-----#

    def show_task_list_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Your Tasks", font=("Segoe UI", 16))
        label.pack(pady=10)

        add_task_button = tk.Button(self.root, text="+ Add new task", command=self.show_add_task_screen)
        add_task_button.pack(pady=5)

        self.sort_var = tk.StringVar(value="Deadline") #
        self.filter_var = tk.StringVar(value="Incomplete Only")
        self.subject_filter_var = tk.StringVar(value="All Subjects")

        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=5)

        sort_menu = tk.OptionMenu(controls_frame, self.sort_var, "Deadline", "Name", "Duration", command=lambda _: self.refresh_task_list()) #dropdown widget
        sort_menu.pack(side="left", padx=5)

        filter_menu = tk.OptionMenu(controls_frame, self.filter_var, "Incomplete Only", "Complete Only", "All", command=lambda _: self.refresh_task_list())
        filter_menu.pack(side="left", padx=5)

        subject_options = ["All Subjects"] + self.get_existing_subjects()
        subject_filter_menu = tk.OptionMenu(controls_frame, self.subject_filter_var, *subject_options, command=lambda _: self.refresh_task_list())
        subject_filter_menu.pack(side="left", padx=5)

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

        subject_choice = self.subject_filter_var.get()
        if subject_choice != "All Subjects":
            tasks = [t for t in tasks if t.subject == subject_choice] 

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

            completed_var = tk.BooleanVar(value=task.completed)
            complete_checkbox = tk.Checkbutton(row, variable=completed_var, command=lambda t=task, v=completed_var: self.toggle_task_complete(t, v))
            complete_checkbox.pack(side="left")

            if task.completed:
                if task.confidence_rating != task.initial_confidence_rating:
                    confidence_text = f"Confidence: {task.initial_confidence_rating} → {task.confidence_rating}"
                else:
                    confidence_text = f"Confidence: {task.confidence_rating}"
            else:
                confidence_text = f"Confidence: {task.confidence_rating}"

            info_text = f"{task.title} — {task.subject} — Due {task.deadline} — {confidence_text}"
            info_label = tk.Label(row, text=info_text)
            info_label.pack(side="left", padx=5)

            edit_button = tk.Button(row, text="Edit", command=lambda t=task: self.show_edit_task_screen(t))
            edit_button.pack(side="right", padx=2)

            delete_button = tk.Button(row, text="Delete", command=lambda t=task: self.confirm_delete_task(t))
            delete_button.pack(side="right", padx=2)

    def toggle_task_complete(self, task, completed_var):
        task.completed = completed_var.get()
        if task.completed:
            task.completed_date = datetime.now().date()
        else:
            task.completed_date = None
        self.save_current_user()
        self.refresh_task_list()

    def show_edit_task_screen(self, task):
        self.clear_screen()
        self.editing_task = task

        label = tk.Label(self.root, text="Edit Task", font=("Segoe UI", 16))
        label.pack(pady=10)

        title_label = tk.Label(self.root, text="Task Title")
        title_label.pack()
        self.edit_title_entry = tk.Entry(self.root)
        self.edit_title_entry.insert(0, task.title) #inserts existing text to be edited
        self.edit_title_entry.pack(pady=5)

        subject_label = tk.Label(self.root, text="Subject")
        subject_label.pack()
        existing_subjects = self.get_existing_subjects()
        self.edit_subject_entry = ttk.Combobox(self.root, values=existing_subjects)
        self.edit_subject_entry.insert(0, task.subject)
        self.edit_subject_entry.pack(pady=5)

        deadline_label = tk.Label(self.root, text="Deadline (DD/MM/YYYY)")
        deadline_label.pack()
        self.edit_deadline_entry = tk.Entry(self.root)
        self.edit_deadline_entry.insert(0, task.deadline)
        self.edit_deadline_entry.pack(pady=5)

        duration_label = tk.Label(self.root, text="Estimated Study Time (mins)")
        duration_label.pack()
        self.edit_duration_entry = tk.Entry(self.root)
        self.edit_duration_entry.insert(0, str(task.duration))
        self.edit_duration_entry.pack(pady=5)

        confidence_label = tk.Label(self.root, text="Confidence Rating (1-5)")
        confidence_label.pack()
        self.edit_confidence_entry = ttk.Spinbox(self.root, from_=1, to=5, width=5, state="readonly")
        self.edit_confidence_entry.set(task.confidence_rating)
        self.edit_confidence_entry.pack(pady=5)

        save_button = tk.Button(self.root, text="Save Changes", command=self.save_edited_task)
        save_button.pack(pady=10)

        cancel_button = tk.Button(self.root, text="Cancel", command=self.show_task_list_screen)
        cancel_button.pack(pady=5)

    def save_edited_task(self):
        title = self.edit_title_entry.get()
        subject = self.edit_subject_entry.get()
        deadline = self.edit_deadline_entry.get()
        duration_text = self.edit_duration_entry.get()
        confidence_text = self.edit_confidence_entry.get()

        if title == "" or subject == "":
            messagebox.showerror("Edit Task Error", "Task title and subject cannot be blank.")
            return

        date_parts = deadline.split("/")

        if len(date_parts) != 3 or not all(part.isdigit() for part in date_parts):
            messagebox.showerror("Add Task Error", "Deadline must be in the format DD/MM/YYYY.")
            return

        day, month, year = date_parts

        if len(year) != 4:
            messagebox.showerror("Add Task Error", "Deadline must be in the format DD/MM/YYYY.")
            return

        try:
            datetime.strptime(deadline, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Edit Task Error", "That date doesn't exist. Please check the day and month.")
            return

        self.editing_task.title = title
        self.editing_task.subject = subject
        self.editing_task.deadline = deadline
        self.editing_task.duration = int(duration_text)
        self.editing_task.confidence_rating = int(confidence_text)

        self.save_current_user()

        messagebox.showinfo("Task Updated", "Task updated successfully!")
        self.show_task_list_screen()

    def confirm_delete_task(self, task):
        confirmed = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task? This action cannot be undone.") #makes sure user doesnt accidentally delete a task
        if confirmed:
            self.pending_user.tasks.remove(task) #removes it from json task list

            self.save_current_user()

            messagebox.showinfo("Task Deleted", "Task deleted successfully.")
            self.show_task_list_screen()

    #-----STUDY TIMER-----#

    def show_timer_task_select_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Select a task to study", font=("Segoe UI", 16))
        label.pack(pady=10)

        incomplete_tasks = [t for t in self.pending_user.tasks if not t.completed]

        if not incomplete_tasks:
            no_tasks_label = tk.Label(self.root, text="No incomplete tasks to study")
            no_tasks_label.pack()
        else:
            for task in incomplete_tasks:
                if task.elapsed_seconds > 0:
                    minutes_so_far = task.elapsed_seconds // 60
                    button_text = f"{task.title} ({task.subject}) — {minutes_so_far} min saved"
                else:
                    button_text = f"{task.title} ({task.subject})"

                task_button = tk.Button(self.root, text=button_text, command=lambda t=task: self.open_timer_screen(t))
                task_button.pack(pady=3)

        back_button = tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard)
        back_button.pack(pady=10)

    def open_timer_screen(self, task):
        self.timer_task = task
        self.timer_running = False
        self.sitting_seconds = 0
        self.timer_session_start = None

        self.clear_screen()

        studying_label = tk.Label(self.root, text="Currently studying", font=("Segoe UI", 10))
        studying_label.pack(pady=(10, 0))

        task_label = tk.Label(self.root, text=task.title, font=("Segoe UI", 16))
        task_label.pack()

        self.timer_display_label = tk.Label(self.root, text=self.format_time(task.elapsed_seconds), font=("Segoe UI", 36))
        self.timer_display_label.pack(pady=20)

        target_label = tk.Label(self.root, text=f"Target: {task.duration} minutes")
        target_label.pack()

        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)

        self.start_button = tk.Button(controls_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=5)

        self.pause_button = tk.Button(controls_frame, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_button.pack(side="left", padx=5)

        reset_sitting_button = tk.Button(controls_frame, text="Reset this sitting", command=self.reset_sitting)
        reset_sitting_button.pack(side="left", padx=5)

        if task.elapsed_seconds > 0:
            reset_all_button = tk.Button(controls_frame, text="Reset all", command=self.reset_all_progress)
            reset_all_button.pack(side="left", padx=5)

        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        continue_later_button = tk.Button(action_frame, text="Continue later", command=self.continue_later)
        continue_later_button.pack(side="left", padx=5)

        stop_button = tk.Button(action_frame, text="Stop and finish", command=self.stop_timer)
        stop_button.pack(side="left", padx=5)

    def format_time(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        self.timer_running = True
        self.timer_session_start = datetime.now()

        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")

        self.update_timer_display()

    def pause_timer(self):
        self.timer_running = False

        just_elapsed = (datetime.now() - self.timer_session_start).total_seconds()
        self.sitting_seconds += int(just_elapsed)

        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def update_timer_display(self):
        if not self.timer_running:
            return

        if not self.timer_display_label.winfo_exists():
            return

        just_elapsed = (datetime.now() - self.timer_session_start).total_seconds()
        current_total = self.timer_task.elapsed_seconds + self.sitting_seconds + int(just_elapsed)

        self.timer_display_label.config(text=self.format_time(current_total))

        self.root.after(1000, self.update_timer_display)

    def reset_sitting(self):
        self.timer_running = False
        self.sitting_seconds = 0
        self.timer_session_start = None

        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

        self.timer_display_label.config(text=self.format_time(self.timer_task.elapsed_seconds))

    def reset_all_progress(self):
        confirmed = messagebox.askyesno("Reset All Progress", "This will erase all previously saved time on this task, not just this sitting. Are you sure?")
        if confirmed:
            self.timer_task.elapsed_seconds = 0
            self.reset_sitting()
            self.save_current_user()

    def get_current_sitting_seconds(self):
        if self.timer_running:
            just_elapsed = (datetime.now() - self.timer_session_start).total_seconds()
            return self.sitting_seconds + int(just_elapsed)
        else:
            return self.sitting_seconds

    def continue_later(self):
        total_sitting_seconds = self.get_current_sitting_seconds()
        self.timer_task.elapsed_seconds += total_sitting_seconds

        self.save_current_user()
        self.show_timer_task_select_screen()

    def stop_timer(self):
        
        total_seconds = self.timer_task.elapsed_seconds + self.get_current_sitting_seconds()

        start_of_task = datetime.now() - timedelta(seconds=total_seconds)
        session = StudySession(task_id=self.timer_task.id, task_subject=self.timer_task.subject, start_time=start_of_task, end_time=datetime.now())
        session.duration_seconds = total_seconds

        self.pending_user.sessions.append(session)
        self.last_session_total_seconds = total_seconds
        self.timer_task.elapsed_seconds = 0

        self.clear_screen()

        finished_label = tk.Label(self.root, text="Session finished", font=("Segoe UI", 16))
        finished_label.pack(pady=10)

        task_label = tk.Label(self.root, text=self.timer_task.title)
        task_label.pack()

        time_label = tk.Label(self.root, text=f"Time studied: {self.format_time(total_seconds)}", font=("Segoe UI", 14))
        time_label.pack(pady=15)

        complete_label = tk.Label(self.root, text="Is this task complete?")
        complete_label.pack()

        yes_button = tk.Button(self.root, text="Yes, mark complete", command=lambda: self.finish_session(mark_complete=True))
        yes_button.pack(pady=3)

        no_button = tk.Button(self.root, text="Not yet", command=lambda: self.finish_session(mark_complete=False))
        no_button.pack(pady=3)

        confidence_label = tk.Label(self.root, text="Update confidence rating (1-5)")
        confidence_label.pack(pady=(15, 0))

        self.confidence_var = tk.StringVar(value=str(self.timer_task.confidence_rating))
        confidence_spinbox = ttk.Spinbox(self.root, from_=1, to=5, textvariable=self.confidence_var, width=5, state="readonly")
        confidence_spinbox.pack(pady=5)

    def finish_session(self, mark_complete):
        new_confidence = int(self.confidence_var.get())
        self.timer_task.confidence_rating = new_confidence

        if mark_complete:
            self.timer_task.completed = True
            self.timer_task.completed_date = datetime.now().date()
        else:
            self.timer_task.elapsed_seconds = self.last_session_total_seconds

        self.save_current_user()

        if mark_complete:
            self.show_dashboard()
        else:
            self.open_timer_screen(self.timer_task)

    def save_current_user(self):
        users = load_users()
        for i, user in enumerate(users):
            if user.username == self.pending_user.username:
                users[i] = self.pending_user
        save_users(users)

    #-----SETTINGS-----#

    def show_settings_screen(self):
        self.clear_screen()

        label = tk.Label(self.root, text="Settings", font=("Segoe UI", 16))
        label.pack(pady=10)

        settings = self.pending_user.settings

        appearance_label = tk.Label(self.root, text="Appearance", font=("Segoe UI", 12))
        appearance_label.pack(pady=(10, 0))

        theme_label = tk.Label(self.root, text="Theme")
        theme_label.pack()
        self.theme_var = tk.StringVar(value=settings.theme)
        theme_menu = tk.OptionMenu(self.root, self.theme_var, "light", "dark")
        theme_menu.pack(pady=5)

        font_size_label = tk.Label(self.root, text="Font size")
        font_size_label.pack()
        self.font_size_var = tk.StringVar(value=settings.font_size)
        font_size_menu = tk.OptionMenu(self.root, self.font_size_var, "small", "medium", "large")
        font_size_menu.pack(pady=5)

        self.high_contrast_var = tk.BooleanVar(value=settings.high_contrast)
        high_contrast_checkbox = tk.Checkbutton(self.root, text="High Contrast Mode", variable=self.high_contrast_var)
        high_contrast_checkbox.pack(pady=5)

        reminders_label = tk.Label(self.root, text="Reminders", font=("Segoe UI", 12))
        reminders_label.pack(pady=(15, 0))

        self.reminders_enabled_var = tk.BooleanVar(value=settings.reminders_enabled)
        reminders_checkbox = tk.Checkbutton(self.root, text="Enable reminders", variable=self.reminders_enabled_var)
        reminders_checkbox.pack(pady=5)

        reminder_days_label = tk.Label(self.root, text="Remind me this many days before a deadline")
        reminder_days_label.pack()
        self.reminder_days_entry = tk.Entry(self.root)
        self.reminder_days_entry.insert(0, str(settings.reminder_days))
        self.reminder_days_entry.pack(pady=5)

        save_button = tk.Button(self.root, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=15)

        back_button = tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard)
        back_button.pack(pady=5)

    def save_settings(self):
        reminder_days_text = self.reminder_days_entry.get()

        if not reminder_days_text.isdigit() or not (1 <= int(reminder_days_text) <= 14):
            messagebox.showerror("Settings Error", "Reminder days must be a whole number between 1 and 14.")
            return

        self.pending_user.settings.theme = self.theme_var.get()
        self.pending_user.settings.font_size = self.font_size_var.get()
        self.pending_user.settings.high_contrast = self.high_contrast_var.get()
        self.pending_user.settings.reminders_enabled = self.reminders_enabled_var.get()
        self.pending_user.settings.reminder_days = int(reminder_days_text)

        self.save_current_user()

        messagebox.showinfo("Settings Saved", "Your settings have been saved.")
        self.show_dashboard()

    def check_reminders(self):
        if not self.pending_user.settings.reminders_enabled:
            return

        today = datetime.now().date()
        reminder_days = self.pending_user.settings.reminder_days

        for task in self.pending_user.tasks:
            if task.completed or task.reminder_sent:
                continue

            deadline_date = datetime.strptime(task.deadline, "%d/%m/%Y").date()
            days_remaining = (deadline_date - today).days

            if days_remaining <= reminder_days:
                self.show_reminder_popup(task, days_remaining)
                task.reminder_sent = True

        self.save_current_user()

    def show_reminder_popup(self, task, days_remaining):
        if days_remaining < 0:
            message = f"{task.title} is overdue."
        elif days_remaining == 0:
            message = f"{task.title} is due today."
        elif days_remaining == 1:
            message = f"{task.title} is due tomorrow."
        else:
            message = f"{task.title} is due in {days_remaining} days."

        messagebox.showinfo("Reminder", message)

    #-----STATISTICS-----#

    def calculate_statistics(self, start_date=None, end_date=None):
        sessions = self.pending_user.sessions
        tasks = self.pending_user.tasks

        if start_date and end_date:
            sessions = [s for s in sessions if start_date <= s.start_time.date() <= end_date]

        if start_date and end_date:
            week_tasks = [t for t in tasks if t.completed_date and start_date <= t.completed_date <= end_date]
        else:
            week_tasks = [t for t in tasks if t.completed]

        total_seconds = sum(getattr(s, "duration_seconds", s.duration * 60) for s in sessions)

        subject_totals = {}
        for session in sessions:
            session_seconds = getattr(session, "duration_seconds", session.duration * 60)
            subject = getattr(session, "task_subject", "Unknown")
            subject_totals[subject] = subject_totals.get(subject, 0) + session_seconds
        completed_count = len(week_tasks)
        total_count = len(tasks)

        subject_completion = {}
        for task in week_tasks:
            subject = task.subject
            if subject not in subject_completion:
                subject_completion[subject] = {"completed": 0, "total": 0}
            subject_completion[subject]["total"] += 1
            if task.completed:
                subject_completion[subject]["completed"] += 1

        if len(week_tasks) > 0:
            average_confidence = round(sum(t.confidence_rating for t in week_tasks) / len(week_tasks), 1)        
        else:
            average_confidence = 0

        return {
            "total_seconds": total_seconds,
            "subject_totals": subject_totals,
            "completed_count": completed_count,
            "total_count": total_count,
            "average_confidence": average_confidence,
            "subject_completion": subject_completion
        }

    def get_week_range(self, reference_date):
        monday = reference_date - timedelta(days=reference_date.weekday())
        sunday = monday + timedelta(days=6)
        return monday, sunday

    def print_test_statistics(self):
        stats = self.calculate_statistics()
        print(f"Total time: {self.format_time(stats['total_seconds'])}")
        for subject, seconds in stats['subject_totals'].items():
            print(f"{subject}: {self.format_time(seconds)}")
        print(f"Completed: {stats['completed_count']} / {stats['total_count']}")

    def format_time_readable(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"

    def show_statistics_screen(self):
        self.clear_screen()

        if self.current_week_start is None:
            self.current_week_start, _ = self.get_week_range(datetime.now().date())

        week_start = self.current_week_start
        week_end = week_start + timedelta(days=6)

        stats = self.calculate_statistics(start_date=week_start, end_date=week_end)
        tasks = self.pending_user.tasks

        label = tk.Label(self.root, text="Statistics", font=("Segoe UI", 16))
        label.pack(pady=10)

        week_frame = tk.Frame(self.root)
        week_frame.pack(pady=5)

        prev_week_button = tk.Button(week_frame, text="← Previous week", command=self.go_to_previous_week)
        prev_week_button.pack(side="left", padx=5)

        week_label = tk.Label(week_frame, text=f"Week of {week_start.strftime('%d %b')} – {week_end.strftime('%d %b %Y')}")
        week_label.pack(side="left", padx=10)

        next_week_button = tk.Button(week_frame, text="Next week →", command=self.go_to_next_week)
        next_week_button.pack(side="left", padx=5)

        today_button = tk.Button(week_frame, text="Today", command=self.go_to_current_week)
        today_button.pack(side="left", padx=5)

        summary_frame = tk.Frame(self.root)
        summary_frame.pack(pady=5)

        total_time_label = tk.Label(summary_frame, text=f"Total study time: {self.format_time(stats['total_seconds'])}")
        total_time_label.pack()

        completed_label = tk.Label(summary_frame, text=f"Tasks completed: {stats['completed_count']} / {stats['total_count']}")
        completed_label.pack()

        confidence_label = tk.Label(summary_frame, text=f"Average confidence: {stats['average_confidence']} / 5")
        confidence_label.pack()

        charts_frame = tk.Frame(self.root)
        charts_frame.pack(pady=10)

        bar_frame = tk.Frame(charts_frame)
        bar_frame.pack(side="left", padx=10)

        subjects = list(set(t.subject for t in tasks) | set(stats['subject_totals'].keys()))
        minutes = []
        for subject in subjects:
            seconds = stats['subject_totals'].get(subject, 0)
            minutes.append(round(seconds / 60, 1))

        has_time_data = any(seconds > 0 for seconds in stats['subject_totals'].values())

        if subjects and has_time_data:
            bar_figure = Figure(figsize=(3.5, 3), dpi=80)
            bar_ax = bar_figure.add_subplot()
            bars = bar_ax.bar(subjects, minutes)
            bar_ax.set_title("Time per subject (mins)")
            bar_ax.tick_params(axis='x', labelrotation=30)

            max_height = max(minutes) if minutes else 0
            label_offset = max_height * 0.05

            for bar, subject in zip(bars, subjects):
                seconds = stats['subject_totals'].get(subject, 0)
                label = self.format_time_readable(seconds)
                bar_ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + label_offset, label, ha='center', va='bottom', fontsize=8)

            bar_ax.set_ylim(top=max_height * 1.2)
            bar_figure.tight_layout()

            bar_canvas = FigureCanvasTkAgg(bar_figure, master=bar_frame)
            bar_canvas.draw()
            bar_canvas.get_tk_widget().pack()
        else:
            no_bar_data_label = tk.Label(bar_frame, text="No study data for this week")
            no_bar_data_label.pack()

        pie_frame = tk.Frame(charts_frame)
        pie_frame.pack(side="left", padx=10)

        has_completion_data = stats['completed_count'] > 0 or (stats['total_count'] - stats['completed_count']) > 0

        if has_completion_data:
            pie_figure = Figure(figsize=(3.5, 3), dpi=80)
            pie_ax = pie_figure.add_subplot()
            pie_ax.pie(
                [stats['completed_count'], stats['total_count'] - stats['completed_count']],
                labels=["Completed", "Remaining"],
                autopct="%1.0f%%"
            )
            pie_ax.set_title("Task completion")

            pie_canvas = FigureCanvasTkAgg(pie_figure, master=pie_frame)
            pie_canvas.draw()
            pie_canvas.get_tk_widget().pack()
        else:
            no_pie_data_label = tk.Label(pie_frame, text="No task activity for this week")
            no_pie_data_label.pack()

        progress_report_button = tk.Button(self.root, text="View progress report →", command=self.show_progress_report_screen)
        progress_report_button.pack(pady=5)

        back_button = tk.Button(self.root, text="Back to Dashboard", command=self.show_dashboard)
        back_button.pack(pady=10)

    def go_to_current_week(self):
        self.current_week_start, _ = self.get_week_range(datetime.now().date())
        self.show_statistics_screen()

    def go_to_previous_week(self):
        account_week_start, _ = self.get_week_range(self.pending_user.created_date)
        new_week_start = self.current_week_start - timedelta(days=7)

        if new_week_start < account_week_start:
            messagebox.showinfo("No Earlier Data", "You can't go back further than the week your account was created.")
            return

        self.current_week_start = new_week_start
        self.show_statistics_screen()

    def go_to_next_week(self):
        current_week_start, _ = self.get_week_range(datetime.now().date())
        new_week_start = self.current_week_start + timedelta(days=7)

        if new_week_start > current_week_start:
            messagebox.showinfo("No Future Data", "You can't view weeks that haven't happened yet.")
            return

        self.current_week_start = new_week_start
        self.show_statistics_screen()

    def show_progress_report_screen(self):
        self.clear_screen()

        stats = self.calculate_statistics()

        label = tk.Label(self.root, text="Progress Report", font=("Segoe UI", 16))
        label.pack(pady=10)

        summary_text = f"You completed {stats['completed_count']} of {stats['total_count']} tasks and studied for {self.format_time_readable(stats['total_seconds'])}."
        summary_label = tk.Label(self.root, text=summary_text, wraplength=400)
        summary_label.pack(pady=5)

        feedback_label = tk.Label(self.root, text="Subject Feedback", font=("Segoe UI", 12))
        feedback_label.pack(pady=(15, 5))

        feedback_frame = tk.Frame(self.root)
        feedback_frame.pack(pady=5)

        for subject, completion in stats['subject_completion'].items():
            completed = completion["completed"]
            total = completion["total"]

            if total == 0:
                continue

            completion_ratio = completed / total

            if completion_ratio < 0.5:
                feedback_text = f"{subject}: You are falling behind in {subject}. Consider prioritising this subject next week."
            elif completion_ratio == 1:
                feedback_text = f"{subject}: You are making excellent progress in {subject}."
            else:
                feedback_text = f"{subject}: You are making good progress in {subject}."

            subject_row = tk.Label(feedback_frame, text=feedback_text, wraplength=400, justify="left", anchor="w")
            subject_row.pack(fill="x", pady=2)

        back_button = tk.Button(self.root, text="Back to Statistics", command=self.show_statistics_screen)
        back_button.pack(pady=10) 

if __name__ == "__main__":
    root = tk.Tk()
    app = RevisionPlannerApp(root)
    root.mainloop()