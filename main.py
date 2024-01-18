import customtkinter as ctk

class ToDoElement(ctk.CTkFrame):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, **kwargs)

        self.checked_var = ctk.BooleanVar(value=False)

        self.checkbox = ctk.CTkCheckBox(self, text="", variable=self.checked_var, command=self.checkbox_event)
        self.checkbox.grid(row=0, column=0, padx=(0, 5))  # Adjusted padx for less spacing

        self.label = ctk.CTkLabel(self, text=text, font=("Arial", 12))  # Adjusted font size
        self.label.grid(row=0, co   lumn=1, padx=5)

    def checkbox_event(self):
        print(f"Checkbox toggled for '{self.label.cget('text')}', current value: {self.checked_var.get()}")

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.todo_elements = []

        # Example to-do items
        todo_items = ["Task 1", "Task 2", "Task 3"]

        for index, item in enumerate(todo_items):
            todo_element = ToDoElement(self, text=item)
            todo_element.grid(row=index, column=0, padx=20, pady=5)
            self.todo_elements.append(todo_element)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")

app = App()
app.mainloop()
