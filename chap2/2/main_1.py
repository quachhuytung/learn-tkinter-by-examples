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


    def add_todo(self, event=None):
        task_text = self.task_create.get(1.0, tk.END).strip()

        if task_text:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
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

if __name__ == '__main__':
    todo = Todo()
    todo.mainloop()
