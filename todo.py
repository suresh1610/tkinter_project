import tkinter as tk
from tkinter import ttk
from tkinter import *
import psycopg2
import datetime
from tkcalendar import DateEntry
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def task():

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
# query = '''create table if not exists task(
#                 username varchar(30),
#                 task varchar(50),
#                 task_date date,
#                 completion_status boolean
#                 )'''
    # username = 'suersh123'
    # task = 'purchase fruits from market'
    # date = datetime.datetime.now()
    # complete = False
    # query = "insert into task(username, task, task_date, completion_status) values(%s, %s, %s, %s)"
    # data = (username, task, date, complete)

    # pointer.execute(query, data)
    # conn.commit()
    # conn.close()

    task_label = ttk.Label(root, text="Enter your task :", font=('Consolas', 15))
    task_label.place(x=200, y=50)

    task_entry = ttk.Entry(root, width=50)
    task_entry.place(x=450, y=55)

    task_date_label = ttk.Label(root, text="Enter your date:", font=('Consolas', 15))
    task_date_label.place(x=900, y=50)

    task_date = DateEntry(root, width=20, background='darkblue',foreground='white', borderwidth=2)
    task_date.place(x=1130, y=55)

    task_add_btn = ttk.Button(root, text="add task")
    task_add_btn.place(x=1400, y=60)



    root.mainloop()
task()

