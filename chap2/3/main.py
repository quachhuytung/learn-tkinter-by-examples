import os
import sqlite3
import tkinter as tk
from tkinter import messagebox as msg


class Todo(tk.Tk):
    def __init__(self):
        super().__init__()

        self.tasks = []

        self.title('Todo App v2.1')
        self.geometry('300x400')

        self.tasks_canvas = tk.Canvas(self)
        self.tasks_frame = tk.Frame(self.tasks_canvas)
        self.scrollbar = tk.Scrollbar(self.tasks_canvas, orient='vertical',
                command=self.tasks_canvas.yview)

        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.tasks_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_frame = self.tasks_canvas.create_window((0,0),
                window=self.tasks_frame, anchor='n')

        self.text_frame = tk.Frame(self)
        self.task_create = tk.Text(self.text_frame, height=3, bg='white', fg='black')
        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()

        self.bind('<Return>', self.add_todo)
        self.bind("<Configure>", self.on_frame_configure)
        self.tasks_canvas.bind('<Configure>', self.task_width)
        self.bind_all('<MouseWheel>', self.mouse_scroll)
        self.bind_all('<Button-4>', self.mouse_scroll)
        self.bind_all('<Button-5>', self.mouse_scroll)

        self.color_schemes = [
            {'bg': 'lightgrey', 'fg': 'black'},
            {'bg': 'grey', 'fg': 'white'}
        ]

        current_tasks = self.load_tasks()
        for task in current_tasks:
            task_text = task[0]
            self.add_todo(None, task_text, True)

    def add_todo(self, event=None, task_text=None, from_db=False):
        if not task_text:
            task_text = self.task_create.get(1.0, tk.END).strip()

        if task_text:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
            self.tasks.append(new_task)
            
            self.set_task_color(new_task, len(self.tasks))
            new_task.bind('<Button-1>', self.remove_todo)
            new_task.pack(side=tk.TOP, fill=tk.X)

            if not from_db:
                self.save_task(task_text)

        self.task_create.delete(1.0, tk.END)

    def recolor_tasks(self):
        for idx, task in enumerate(self.tasks):
            self.set_task_color(task, idx)

    def remove_todo(self, event=None):
        task = event.widget
        if msg.askyesno('Really Delete?', 'Delete ' + task.cget('text') + ' ?'):
            self.tasks.remove(event.widget)

            delete_task_query = "Delete from tasks where task=?"
            delete_task_data=(task.cget("text"), )

            self.runQuery(delete_task_query, delete_task_data)
            event.widget.destroy()
            self.recolor_tasks()


    def set_task_color(self, task, position):
        task_style_choice = position % 2
        my_scheme_choice = self.color_schemes[task_style_choice]
        task.configure(bg=my_scheme_choice['bg'])
        task.configure(fg=my_scheme_choice['fg'])


    def on_frame_configure(self, event=None):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))


    def task_width(self, event):
        canvas_width = event.width
        self.tasks_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def mouse_scroll(self, event):
        if event.delta:
            self.tasks_canvas.yview_scroll(int(-1*(event_delta/120)), 'units')
        else:
            if event.num == 5:
                move = -1
            else:
                move = 1

            self.tasks_canvas.yview_scroll(move, 'units')

    def load_tasks(self):
        load_tasks_query = "Select * from tasks"
        my_tasks = self.runQuery(load_tasks_query, receive=True)

        return my_tasks

    def save_task(self, task):
        insert_task_query = "Insert into tasks values (?)"

        insert_task_data = (task, )
        self.runQuery(insert_task_query, insert_task_data)

    @staticmethod
    def runQuery(sql, data=None, receive=False):
        conn = sqlite3.connect('task.db')
        cursor = conn.cursor()

        if data:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)

        if receive: 
            return cursor.fetchall()
        else:
            conn.commit()

        conn.close()

    @staticmethod
    def first_time_db():
        create_tables = "create table tasks(task TEXT)"
        Todo.runQuery(create_tables)

        default_task_query = "INSERT into tasks values (?)"
        default_task_data = ("----- Add item here ----",)
        Todo.runQuery(default_task_query, default_task_data)

if __name__ == '__main__':
    if not os.path.isfile('task.db'):
        Todo.first_time_db()
    todo = Todo()
    todo.mainloop()
