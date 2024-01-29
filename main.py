import customtkinter as ctk

class ToDoElement(ctk.CTkFrame):
    def __init__(self, master, text, delete_callback, **kwargs):
        super().__init__(master, **kwargs)

        self.checked_var = ctk.BooleanVar(value=False)

        self.checkbox = ctk.CTkCheckBox(self, height=20, width=25, text="", variable=self.checked_var, command=self.checkbox_event)
        self.checkbox.pack(side='left', pady="5")

        self.label = ctk.CTkLabel(self, height=20, text=text, font=("Arial", 12))
        self.label.pack(side='left')

        self.delete_button = ctk.CTkButton(self, height=30, width=50, text="Delete", command=lambda: delete_callback(self))
        self.delete_button.pack(side='right')

    def checkbox_event(self):
        print(f"Checkbox toggled for '{self.label.cget('text')}', current value: {self.checked_var.get()}")

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.todo_elements = []

        todo_items = ["Task 1", "Task 2", "Task 3"]

        for index, item in enumerate(todo_items):
            todo_element = ToDoElement(self, text=item, delete_callback=self.delete_task)
            todo_element.grid(row=index, column=0, padx=20, pady=5, sticky="ew")
            self.todo_elements.append(todo_element)

        # Set column weight to make tasks take full width
        self.grid_columnconfigure(0, weight=1)

    def delete_task(self, todo_element):
        self.todo_elements.remove(todo_element)
        todo_element.destroy()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew", pady=5)

        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, pady=10)

    def add_task(self):
        task_dialog = ctk.CTkInputDialog(text="Type task description:", title="Add new task")
        new_task_text = task_dialog.get_input()
        if new_task_text:
            new_todo_element = ToDoElement(self.my_frame, text=new_task_text, delete_callback=self.my_frame.delete_task)
            new_todo_element.grid(row=len(self.my_frame.todo_elements), column=0, padx=20, pady=5, sticky="ew")
            self.my_frame.todo_elements.append(new_todo_element)

app = App()
app.mainloop()
