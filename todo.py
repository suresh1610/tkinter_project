import tkinter as tk
from tkinter import ttk
from tkinter import *
import psycopg2
import datetime
from tkcalendar import DateEntry
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def task(username):  # main function

    root = tk.Tk()
    root.state("zoomed")
    root.title('todo application')
    conn = psycopg2.connect(
        host = 'localhost',
        dbname = 'postgres', 
        user = 'postgres',
        password = '12345',
        port = 5432 
    )

    pointer = conn.cursor()
    create_query = '''create table if not exists todo(
                id serial primary key,
                task varchar(50),
                task_date date,
                completion_status boolean,
                u_name varchar(30) references userdetails(username)
                )'''
    pointer.execute(create_query,)
    conn.commit()

    def add_task(): # insert entered data into the db (sub function)
        task = task_entry.get()
        date = task_date_entry.get()
        complete = False
        u_name = username

        query = "insert into todo(task, task_date, completion_status, u_name) values(%s, %s, %s, %s)"
        data = (task, date, complete, u_name)

        pointer.execute(query, data)
        conn.commit()

    task_label = ttk.Label(root, text="Enter your task :", font=('Consolas', 15))
    task_label.place(x=200, y=50)

    task_entry = ttk.Entry(root, width=42, font=('Consolas', 15))
    task_entry.place(x=450, y=55)

    task_date_label = ttk.Label(root, text="Enter your date (yyyy-mm-dd):", font=('Consolas', 15))
    task_date_label.place(x=200, y=100)

    # task_date = DateEntry(root,date_pattern='yyyy/mm/dd' ,width=20, background='darkblue',foreground='white', borderwidth=2)
    # task_date.place(x=450, y=105)
    task_date_entry = ttk.Entry(root, width=30, font=('Consolas', 15))
    task_date_entry.place(x=620, y=100)

    task_add_btn = ttk.Button(root, text="add task", command=add_task, width=20)
    task_add_btn.place(x=1200, y=105)

    root.mainloop()
    conn.close()

# task("suresh123")

