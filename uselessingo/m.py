import tkinter as tk
from tkinter import ttk, messagebox

class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Management System")
        self.root.geometry("800x600")
        
        # (database Entriesss)
        self.users = {"admin": "password", "trainer": "1234"}
        self.current_user = None
        self.workouts = []
        
        # Create the main container
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (HomePage, LoginPage, WorkoutPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(HomePage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
        # Update the header based on login status
        if hasattr(frame, 'update_header'):
            frame.update_header()
    
    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            self.current_user = username
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.show_frame(WorkoutPage)
            return True
        else:
            messagebox.showerror("Error", "Invalid credentials")
            return False
    
    def logout(self):
        self.current_user = None
        self.show_frame(HomePage)
    
    def add_workout(self, workout_data):
        workout_data['user'] = self.current_user
        self.workouts.append(workout_data)
        messagebox.showinfo("Success", "Workout added successfully!")
        self.show_frame(WorkoutPage)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Header
        self.header = tk.Frame(self)
        self.header.pack(fill="x", padx=10, pady=10)
        
        self.home_btn = tk.Button(self.header, text="Home", 
                                command=lambda: controller.show_frame(HomePage),
                                state="disabled")
        self.home_btn.pack(side="left")
        
        self.login_btn = tk.Button(self.header, text="Login", 
                                  command=lambda: controller.show_frame(LoginPage))
        self.login_btn.pack(side="right")
        
        # Content
        content = tk.Frame(self)
        content.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(content, text="Gym Management System", 
                font=("Helvetica", 24)).pack(pady=50)
        
        tk.Label(content, text="Track your workouts and progress", 
                font=("Helvetica", 14)).pack(pady=10)
        
        tk.Button(content, text="Let's Get Started", 
                command=lambda: controller.show_frame(WorkoutPage),
                state="normal" if controller.current_user else "disabled").pack(pady=20)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Header
        self.header = tk.Frame(self)
        self.header.pack(fill="x", padx=10, pady=10)
        
        self.home_btn = tk.Button(self.header, text="Home", 
                                command=lambda: controller.show_frame(HomePage))
        self.home_btn.pack(side="left")
        
        # Content
        content = tk.Frame(self)
        content.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(content, text="Login", font=("Helvetica", 20)).pack(pady=20)
        
        # Login form
        form = tk.Frame(content)
        form.pack()
        
        tk.Label(form, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
        self.username = tk.Entry(form)
        self.username.grid(row=0, column=1, pady=5)
        
        tk.Label(form, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
        self.password = tk.Entry(form, show="*")
        self.password.grid(row=1, column=1, pady=5)
        
        btn_frame = tk.Frame(content)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Login", 
                command=self.attempt_login).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", 
                command=lambda: controller.show_frame(HomePage)).pack(side="left", padx=10)
    
    def attempt_login(self):
        username = self.username.get()
        password = self.password.get()
        if self.controller.login(username, password):
            self.username.delete(0, tk.END)
            self.password.delete(0, tk.END)

class WorkoutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Header
        self.header = tk.Frame(self)
        self.header.pack(fill="x", padx=10, pady=10)
        
        self.home_btn = tk.Button(self.header, text="Home", 
                                command=lambda: controller.show_frame(HomePage))
        self.home_btn.pack(side="left")
        
        self.logout_btn = tk.Button(self.header, text="Logout", 
                                  command=controller.logout)
        self.logout_btn.pack(side="right")
        
        # Content
        self.content = tk.Frame(self)
        self.content.pack(expand=True, fill="both", padx=50, pady=50)
        
        self.update_header()
        self.create_workout_form()
    
    def update_header(self):
        if hasattr(self, 'welcome_label'):
            self.welcome_label.destroy()
        
        self.welcome_label = tk.Label(self.header, 
                                    text=f"Welcome, {self.controller.current_user}!")
        self.welcome_label.pack(side="left", padx=20)
    
    def create_workout_form(self):
        # Clear previous content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="Enter Workout Details", 
                font=("Helvetica", 16)).pack(pady=10)
        
        # Workout form
        form = tk.Frame(self.content)
        form.pack(pady=20)
        
        # Date
        tk.Label(form, text="Date:").grid(row=0, column=0, sticky="e", pady=5)
        self.date_entry = tk.Entry(form)
        self.date_entry.grid(row=0, column=1, pady=5)
        
        # Exercise Type
        tk.Label(form, text="Exercise:").grid(row=1, column=0, sticky="e", pady=5)
        self.exercise_var = tk.StringVar()
        exercises = ["Cardio", "Weight Training", "Yoga", "CrossFit", "Swimming"]
        self.exercise_menu = ttk.Combobox(form, textvariable=self.exercise_var, values=exercises)
        self.exercise_menu.grid(row=1, column=1, pady=5)
        
        # Duration
        tk.Label(form, text="Duration (mins):").grid(row=2, column=0, sticky="e", pady=5)
        self.duration_entry = tk.Entry(form)
        self.duration_entry.grid(row=2, column=1, pady=5)
        
        # Submit button
        btn_frame = tk.Frame(self.content)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Submit Workout", 
                command=self.submit_workout).pack(side="left", padx=10)
        tk.Button(btn_frame, text="View Workouts", 
                command=self.show_workouts).pack(side="left", padx=10)
    
    def submit_workout(self):
        workout_data = {
            "date": self.date_entry.get(),
            "exercise": self.exercise_var.get(),
            "duration": self.duration_entry.get(),
            "calories": self.calories_entry.get(),
            "notes": self.notes_text.get("1.0", tk.END).strip()
        }
        
        if not all(workout_data.values()):
            messagebox.showwarning("Warning", "Please fill all fields!")
            return
        
        self.controller.add_workout(workout_data)
    
    def show_workouts(self):
        # Clear previous content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="Your Workout History", 
                font=("Helvetica", 16)).pack(pady=10)
        
        if not self.controller.workouts:
            tk.Label(self.content, text="No workouts recorded yet").pack()
            tk.Button(self.content, text="Back", 
                    command=self.create_workout_form).pack(pady=20)
            return
        
        # Create a treeview to display workouts
        columns = ("Date", "Exercise", "Duration", "Calories")
        tree = ttk.Treeview(self.content, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Add workout data
        for workout in self.controller.workouts:
            if workout['user'] == self.controller.current_user:
                tree.insert("", tk.END, values=(
                    workout['date'],
                    workout['exercise'],
                    workout['duration'],
                    workout['calories']
                ))
        
        tree.pack(expand=True, fill="both", pady=10)
        
        # Back button
        tk.Button(self.content, text="Back", 
                command=self.create_workout_form).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()