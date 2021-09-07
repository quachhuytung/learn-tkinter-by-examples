import tkinter as tk
from tkinter import messagebox as msg


class Todo(tk.Tk):
    def __init__(self):
        super().__init__()

        self.tasks = []

        self.title('Todo App v0')
        self.geometry('300x400')

        self.task_create = tk.Text(self, height=3)
        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()


        self.bind('<Return>', self.add_todo)
        self.color_schemes = [
            {'bg': 'lightgrey', 'fg': 'black'},
            {'bg': 'grey', 'fg': 'white'}
        ]


    def add_todo(self, event=None):
        task_text = self.task_create.get(1.0, tk.END).strip()

        if task_text:
            new_task = tk.Label(self, text=task_text, pady=10)
            self.tasks.append(new_task)
            
            self.set_task_color(new_task, len(self.tasks))
            new_task.bind('<Button-1>', self.remove_todo)
            new_task.pack(side=tk.TOP, fill=tk.X)

        self.task_create.delete(1.0, tk.END)

    def recolor_tasks(self):
        for idx, task in enumerate(self.tasks):
            self.set_task_color(task, idx)

    def remove_todo(self, event=None):
        task = event.widget
        if msg.askyesno('Really Delete?', 'Delete ' + task.cget('text') + ' ?'):
            self.tasks.remove(event.widget)
            event.widget.destroy()
            self.recolor_tasks()


    def set_task_color(self, task, position):
        task_style_choice = position % 2
        my_scheme_choice = self.color_schemes[task_style_choice]
        task.configure(bg=my_scheme_choice['bg'])
        task.configure(fg=my_scheme_choice['fg'])

        

if __name__ == '__main__':
    todo = Todo()
    todo.mainloop()
