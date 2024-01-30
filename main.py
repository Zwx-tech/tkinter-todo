import sqlite3
import customtkinter as ctk
from dialog import CustomDialog

class ToDoElement(ctk.CTkFrame):

    def __init__(self, master, text, checked, end_date, end_hour, delete_callback, edit_callback, update_callback, **kwargs):
        super().__init__(master, **kwargs)

        self.end_date = end_date
        self.end_hour = end_hour

        self.checked_var = ctk.BooleanVar(value=checked)
        self.checkbox = ctk.CTkCheckBox(self, height=20, width=25, text="", variable=self.checked_var, command=self.checkbox_event)
        self.checkbox.pack(side='left', pady="5")
        self.label = ctk.CTkLabel(self, height=20, text=text, font=("Arial", 12))
        self.label.pack(side='left', fill="x", expand=True)
        
        self.end_date_label = ctk.CTkLabel(self, height=20, text=f"End Date: {end_date} {end_hour}", font=("Arial", 10))
        self.end_date_label.pack(side='left', fill="x", expand=True)
        self.edit_button = ctk.CTkButton(self, height=30, width=50, text="Edit", command=lambda: edit_callback(self))
        self.edit_button.pack(side='right', padx=(10, 0))
        self.delete_button = ctk.CTkButton(self, height=30, width=50, text="Delete", command=lambda: delete_callback(self))
        self.delete_button.pack(side='right')
        self.update_callback = update_callback
    
    def checkbox_event(self):
        self.update_callback()

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, db_connection, **kwargs):
        super().__init__(master, **kwargs)
        self.db_connection = db_connection
        self.todo_elements = self.load_tasks()

    def load_tasks(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT task_text, checked, end_date, end_hour FROM tasks")
        rows = cursor.fetchall()
        todo_elements = []
        for index, (item, checked, end_date, end_hour) in enumerate(rows):
            todo_element = ToDoElement(
                self, text=item, checked=checked, end_date=end_date, end_hour=end_hour,
                update_callback=self.update_database, delete_callback=self.delete_task, edit_callback=self.edit_task
            )
            todo_element.pack(side="top", fill="x", padx="5", pady="5")
            todo_elements.append(todo_element)
        return todo_elements


    def delete_task(self, todo_element):
        self.todo_elements.remove(todo_element)
        todo_element.destroy()
        self.update_database()

    def edit_task(self, todo_element):
        task_time = todo_element.end_date_label.cget('text').split(" ")

        edit_dialog = CustomDialog(text="Edit task description:", title="Edit Task", text_value=todo_element.label.cget('text'), end_date=task_time[2], hour=task_time[3])
        edited_text, edited_date, edited_hour = edit_dialog.get_input()
        if edited_text:
            todo_element.label.configure(text=edited_text)
            todo_element.end_date_label.configure(text=f"End Date: {edited_date} {edited_hour}")
            todo_element.end_date = edited_date
            todo_element.end_hour = edited_hour
            self.update_database()


    def update_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM tasks")
        for task_element in self.todo_elements:
            cursor.execute(
                "INSERT INTO tasks (task_text, checked, end_date, end_hour) VALUES (?, ?, ?, ?)",
                (task_element.label.cget('text'), task_element.checked_var.get(), task_element.end_date, task_element.end_hour)
            )
        self.db_connection.commit() 



class App(ctk.CTk):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = MyFrame(master=self, db_connection=self.db_connection, width=450, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, pady=10)

    def add_task(self):
        new_task_dialog = CustomDialog(text="Edit task description:", title="Edit Task")
        new_task_text, new_task_date, new_task_hour = new_task_dialog.get_input()
        if new_task_text:
            new_todo_element = ToDoElement(self.my_frame, text=new_task_text, update_callback=self.my_frame.update_database, delete_callback=self.my_frame.delete_task, edit_callback=self.my_frame.edit_task, checked=False, end_date=new_task_date, end_hour=new_task_hour)
            new_todo_element.pack(side="top", fill="x", padx="5", pady="5")
            self.my_frame.todo_elements.append(new_todo_element)
            self.my_frame.update_database()

conn = sqlite3.connect('tasks.db')

conn.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        task_text TEXT,
        checked INTEGER,
        end_date TEXT,
        end_hour TEXT
    )
''')


app = App(db_connection=conn)
app.mainloop()

conn.close()