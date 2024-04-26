import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector
import psycopg2
from datetime import datetime
from tkcalendar import DateEntry
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def task(username):  # main function

    root = Tk()
    root.state("zoomed")
    root.title('todo application')
    conn = mysql.connector.connect(  # here i am connect to database
        host="localhost",
        user="root",
        passwd="",
        database="pumo_project"
    )

    pointer = conn.cursor()
    create_query = '''create table if not exists todo(
                task_id serial primary key,
                task_name varchar(50),
                task_date date,
                completion_status boolean,
                u_name varchar(30) references userdetails(username)
                )'''
    pointer.execute(create_query,)
    conn.commit()

    def load_task():
        clear_frames()

        today = datetime.now().date()

        query = "select * from todo where u_name = %s order by task_date"
        date = (username,)
        pointer.execute(query, date)
        todos = pointer.fetchall()

        frame = None

        for task_ele in todos:
            task_id, task_name, task_date, completion_status, u_name = task_ele

            if task_date == today:
                frame = today_frame
            elif task_date > today:
                frame = tomorrow_frame
            else:
                frame = previous_frame

            task_checkbox = ttk.Checkbutton(frame, text=task_name)
            task_checkbox.pack()


    

    def clear_frames():
        for frame in [today_frame, tomorrow_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
    


    def add_task(): # insert entered data into the db (sub function)
        enter_task = task_entry.get()
        date = task_date_entry.get()
        complete = False
        u_name = username

        query = "insert into todo(task_name, task_date, completion_status, u_name) values(%s, %s, %s, %s)"
        data = (enter_task, date, complete, u_name)
        pointer.execute(query, data)
        conn.commit()
    

    user_name = Label(root, text=username, font=('Goudy Stout', 15))
    user_name.pack()
    
    task_label = Label(root, text="Enter your task :", font=('Consolas', 12))
    task_label.place(x=100, y = 50)

    task_entry = Entry(root, width=42, font=('Consolas', 12))
    task_entry.place(x=300, y =50)

    task_date_label = Label(root, text="Enter your date (yyyy-mm-dd):", font=('Consolas', 12))
    task_date_label.place(x=800, y=50)

    # task_date = DateEntry(root,date_pattern='yyyy/mm/dd' ,width=20, background='darkblue',foreground='white', borderwidth=2)
    # task_date.place(x=450, y=105)
    task_date_entry = Entry(root, width=20, font=('Consolas', 12))
    task_date_entry.place(x=1130, y=50)

    task_add_btn = Button(root, text="add task", command=add_task, width=20)
    task_add_btn.place(x=1400, y=45)

    today_frame = LabelFrame(root, text="today's task")
    today_frame.place(x=20, y = 100)

    # frame_label = Checkbutton(today_frame, text="readugiytdjtrsyersyres books")
    # frame_label.pack(side="left")

    # frame_label2 = Checkbutton(today_frame, text="read books 2")
    # frame_label2.pack(side="left")

    tomorrow_frame = LabelFrame(root, text="tomorrow's task")
    tomorrow_frame.place(x=500, y = 200)

    previous_frame = LabelFrame(root, text="tomorrow's task")
    previous_frame.place(x=1000, y = 200)

    load_task()

    root.mainloop()
    conn.close()

# task("suresh123")

