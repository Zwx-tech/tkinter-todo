import sqlite3
import customtkinter as ctk
from dialog import CustomDialog

class ToDoElement(ctk.CTkFrame):
    def __init__(self, master, text, delete_callback, edit_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.checked_var = ctk.BooleanVar(value=False)
        self.checkbox = ctk.CTkCheckBox(self, height=20, width=25, text="", variable=self.checked_var, command=self.checkbox_event)
        self.checkbox.pack(side='left', pady="5")
        self.label = ctk.CTkLabel(self, height=20, text=text, font=("Arial", 12))
        self.label.pack(side='left')
        self.edit_button = ctk.CTkButton(self, height=30, width=50, text="Edit", command=lambda: edit_callback(self))
        self.edit_button.pack(side='right', padx=(10, 0))
        self.delete_button = ctk.CTkButton(self, height=30, width=50, text="Delete", command=lambda: delete_callback(self))
        self.delete_button.pack(side='right')

    def checkbox_event(self):
        print(f"Checkbox toggled for '{self.label.cget('text')}', current value: {self.checked_var.get()}")

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, db_connection, **kwargs):
        super().__init__(master, **kwargs)
        self.db_connection = db_connection
        self.todo_elements = self.load_tasks()

    def load_tasks(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT task_text FROM tasks")
        rows = cursor.fetchall()
        tasks = [row[0] for row in rows]
        todo_elements = []
        for index, item in enumerate(tasks):
            todo_element = ToDoElement(self, text=item, delete_callback=self.delete_task, edit_callback=self.edit_task)
            todo_element.grid(row=index, column=0, padx=20, pady=5, sticky="ew")
            todo_elements.append(todo_element)
        return todo_elements

    def delete_task(self, todo_element):
        self.todo_elements.remove(todo_element)
        todo_element.destroy()
        self.update_database()

    def edit_task(self, todo_element):
        # Open a dialog for editing the task
        edit_dialog = CustomDialog(text="Edit task description:", title="Edit Task", text_value=todo_element.label.cget('text'))
        edited_text = edit_dialog.get_input()
        if edited_text:
            todo_element.label.configure(text=edited_text)
            self.update_database()

    def update_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM tasks")
        for task_element in self.todo_elements:
            cursor.execute("INSERT INTO tasks (task_text) VALUES (?)", (task_element.label.cget('text'),))
        self.db_connection.commit()

class App(ctk.CTk):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.my_frame = MyFrame(master=self, db_connection=self.db_connection, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, pady=10)

    def add_task(self):
        task_dialog = ctk.CTkInputDialog(text="Type task description:", title="Add new task")
        new_task_text = task_dialog.get_input()
        if new_task_text:
            new_todo_element = ToDoElement(self.my_frame, text=new_task_text, delete_callback=self.my_frame.delete_task, edit_callback=self.my_frame.edit_task)
            new_todo_element.grid(row=len(self.my_frame.todo_elements), column=0, padx=20, pady=5, sticky="ew")
            self.my_frame.todo_elements.append(new_todo_element)
            self.my_frame.update_database()

# Connect to SQLite database
conn = sqlite3.connect('tasks.db')

# Create tasks table if not exists
conn.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        task_text TEXT
    )
''')

app = App(db_connection=conn)
app.mainloop()

# Don't forget to close the database connection when the program exits
conn.close()
