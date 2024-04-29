import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector
from tkinter import messagebox
from tkinter.messagebox import askokcancel, WARNING
from tkinter import simpledialog
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

        today = datetime.now().date()
        complete_status = 0

        query = "select * from todo where u_name = %s and completion_status=%s order by task_date"
        date = (username,complete_status)
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
            
            task_frame = Frame(frame)
            task_frame.pack(fill='x', pady=5, padx=5)

            completion_var = tk.IntVar(value=0)

            task_checkbox = ttk.Checkbutton(task_frame, text=task_name, variable=completion_var, onvalue=1, offvalue=0)
            task_checkbox.pack(side="left")

            edit_btn = ttk.Button(task_frame, text="edit", command=lambda task_id=task_id: edit_task(task_id))
            edit_btn.pack(side="left", padx=5)

            delete_btn = ttk.Button(task_frame, text="delete", command=lambda task_id=task_id: delete_task(task_id))
            delete_btn.pack(side="left", padx=5)

            complete_btn = ttk.Button(task_frame, text="todo completed", command=lambda task_id=task_id: update_task(task_id))
            complete_btn.pack(side="left")
    
    def clear_frame():
        for frames in [today_frame, tomorrow_frame, previous_frame, complted_frame]:
            for widget in frames.winfo_children():
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
        clear_frame()
        reload_task()
    
    def update_task(task_id):

        complete_status = True
        query = "update todo set completion_status=%s where task_id=%s"
        data = (complete_status,task_id)
        pointer.execute(query, data)
        conn.commit()
        clear_frame()
        reload_task()
        print("data is updated")
    
    def edit_task_name(task_id, new_task_name):
        edit_query = "update todo set task_name=%s where task_id=%s"
        edit_data = (new_task_name, task_id)
        pointer.execute(edit_query, edit_data)
        conn.commit()
        clear_frame()
        reload_task()

    
    def edit_task(task_id):
        new_task_name = tk.simpledialog.askstring("Edit task", "Enter your new task name:")
        if new_task_name:
            edit_task_name(task_id, new_task_name)
        
    
    def delete_task(task_id):
        ans = askokcancel(title="delete task", message="are you sure?", icon=WARNING)
        if ans:
            delete_query = "delete from todo where task_id=%s"
            data = (task_id,)
            pointer.execute(delete_query, data)
            conn.commit()
            clear_frame()
            reload_task()
            messagebox.showinfo("delete message", "Todo deleted successfully")
        else:
            messagebox.showinfo("delete message", "Todo deletion failed")

        
    
    def display_completed():  # dispaly completed task
        # clear_frames()
        complete_status = 1

        query = "select * from todo where completion_status=%s and u_name=%s"
        data = (complete_status,username)
        pointer.execute(query, data)
        todos = pointer.fetchall()

        for todo_ele in todos:
            task_id, task_name, task_date, completion_status, u_name = todo_ele

            complete_frame = Frame(complted_frame)
            complete_frame.pack(anchor='w')

            completed_label = Label(complete_frame, text=task_name)
            completed_label.pack(side='left')

            completed_date = Label(complete_frame, text=task_date)
            completed_date.pack(side="left")

    
    def reload_task():
        load_task()
        display_completed()
    
    seperator_line = ttk.Separator(root, orient="horizontal")
    seperator_line.pack(fill='x')

    user_name = Label(root, text=f"welcome {username}", font=('Times New Roman', 15))
    user_name.place(x=1700, y=5)

    seperator_line_name = ttk.Separator(root, orient='horizontal')
    seperator_line_name.place(x=0, y=40, width='2000')

    task_label = Label(root, text="Enter your task :", font=('Consolas', 12))
    task_label.place(x=100, y = 60)
    # task_label.pack(padx=5, pady=0)

    task_entry = Entry(root, width=42, font=('Consolas', 12))
    task_entry.place(x=300, y =60)
    #task_entry.pack(padx=5, pady=5)

    task_date_label = Label(root, text="Enter your date (yyyy-mm-dd):", font=('Consolas', 12))
    task_date_label.place(x=800, y=60)
    #task_date_label.pack(padx=5, pady=5)

    # task_date = DateEntry(root,date_pattern='yyyy/mm/dd' ,width=20, background='darkblue',foreground='white', borderwidth=2)
    # task_date.place(x=450, y=105)
    task_date_entry = Entry(root, width=20, font=('Consolas', 12))
    task_date_entry.place(x=1130, y=60)
    #task_date_entry.pack(padx=5, pady=5)

    task_add_btn = Button(root, text="add task", command=add_task, width=20)
    task_add_btn.place(x=1400, y=55)
    #task_add_btn.pack(padx=5, pady=5)

    today_frame = LabelFrame(root, text="today's task")
    today_frame.place(x=20, y = 100)
    #today_frame.pack(padx=5, pady=5)

    tomorrow_frame = LabelFrame(root, text="upcoming task")
    #tomorrow_frame.pack(padx=5, pady=5)
    tomorrow_frame.place(x=700, y = 100)

    previous_frame = LabelFrame(root, text="incomplete previous task")
    previous_frame.place(x=1300, y = 100)
    #previous_frame.pack(padx=5, pady=5)

    complted_frame = LabelFrame(root,text="completed task")
    complted_frame.place(x=30, y=800)
    #complted_frame.pack(side="right",pady=5, padx=5)
    
    reload_task()

    root.mainloop()
    conn.close()
# task("suresh123")

