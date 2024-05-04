import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector
from tkinter import messagebox
from tkinter.messagebox import askokcancel, WARNING
from tkinter import simpledialog
# import psycopg2
from datetime import datetime
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def display_completed(username):  # dispaly completed task
        # clear_frames()
        complete_window = tk.Tk()
        # complete_window.state("zoomed")
        complete_window.geometry('1000x700')
        complete_window.resizable(False, False)
        complete_window.title("histroy")

        conn = mysql.connector.connect(  # here i am connect to database
            host="localhost",
            user="root",
            passwd="",
            database="pumo_project"
        )

        pointer = conn.cursor()

        notebook = ttk.Notebook(complete_window)
        notebook.pack(padx=2, pady=5,expand=True)

        user_detail = ttk.Frame(notebook, width=1000, height=680)
        user_detail.pack(fill="both", expand=True)

        histroy = ttk.Frame(notebook, width=1000, height=680)
        histroy.pack(fill="both", expand=True)

        notebook.add(user_detail, text="User details")
        notebook.add(histroy, text="task histroy")

        user_detail_query = "select * from userdetails where username = %s"
        user_data = (username,)
        pointer.execute(user_detail_query, user_data)
        u_deteil = pointer.fetchall()

        for details in u_deteil:
            username, email, password, first_name, last_name = details

            user_name_label = tk.Label(user_detail, text="username:", font=('Consolas', 15))
            user_name_label.place(relx=0.02, rely=0.02)

            user_name_display = tk.Label(user_detail, text=username, font=('Consolas', 15))
            user_name_display.place(relx=0.15, rely=0.02)

            email_label = tk.Label(user_detail, text="email address:", font=('Consolas', 15))
            email_label.place(relx=0.02, rely=0.1)

            email_display = tk.Label(user_detail, text=email, font=('Consolas', 15))
            email_display.place(relx=0.25, rely=0.1)

            passwd_label = tk.Label(user_detail, text="password:", font=('Consolas', 15))
            passwd_label.place(relx=0.02, rely=0.2)

            passwd_display = tk.Label(user_detail, text=password, font=('Consolas', 15))
            passwd_display.place(relx=0.25, rely=0.2)

            firstN_label = tk.Label(user_detail, text="First Name:", font=('Consolas', 15))
            firstN_label.place(relx=0.02, rely=0.3)

            firstN_display = tk.Label(user_detail, text=first_name, font=('Consolas', 15))
            firstN_display.place(relx=0.25, rely=0.3)

            lastN_label = tk.Label(user_detail, text="Last Name:", font=('Consolas', 15))
            lastN_label.place(relx=0.02, rely=0.4)

            lastN_display = tk.Label(user_detail, text=last_name, font=('Consolas', 15))
            lastN_display.place(relx=0.25, rely=0.4)

        complete_status = 1
        complete_query = "select * from todo where completion_status=%s and u_name=%s"
        complete_data = (complete_status,username)
        pointer.execute(complete_query, complete_data)
        todos = pointer.fetchall()

        complted_frame = tk.LabelFrame(histroy,text="completed task",background="#ffffff", font=('Consolas', 15))
        complted_frame.place(relx=0.26, rely=0.1, width=500)

        for todo_ele in todos:
            task_id, task_name, task_date, completion_status, u_name = todo_ele

            complete_frame = Frame(complted_frame, bg="#ffffff")
            complete_frame.pack(anchor='w')

            completed_label = tk.Label(complete_frame, text=f"✔️{task_name}", bg="#ffffff")
            completed_label.pack(side='left', padx=10, pady=10)

            completed_date = tk.Label(complete_frame, text=task_date, bg="#ffffff")
            completed_date.pack(side="left", padx=10, pady=10)

            status = tk.Label(complete_frame, text="completed", bg="#ffffff")
            status.pack(side="left")
        
        complete_window.mainloop()

def task(username):  # main function

    root = Tk()
    root.state("zoomed")
    root.title('todo application')
    image = Image.open("C:\\Users\\sures\\Downloads\\Todo\\main_page2.png")
    resize_login = image.resize((1920, 1080))
    img = ImageTk.PhotoImage(resize_login)
    label_login = Label(image=img)
    label_login.image = img
    label_login.pack()
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
            
            task_frame = tk.Frame(frame, background='#ffffff')
            task_frame.pack(fill='x', pady=5, padx=5)

            completion_var = tk.IntVar(value=1)

            task_checkbox = tk.Checkbutton(task_frame, text=task_name, variable=completion_var, onvalue=1, offvalue=0, 
                                           background="#ffffff", font=('Consolas', 13),cursor="hand2")
            task_checkbox.pack(side="left")

            edit_btn = ttk.Button(task_frame, text="edit", command=lambda task_id=task_id: edit_task(task_id),cursor="hand2")
            edit_btn.pack(side="left", padx=5)

            delete_btn = ttk.Button(task_frame, text="delete", command=lambda task_id=task_id: delete_task(task_id),cursor="hand2")
            delete_btn.pack(side="left", padx=5)

            complete_btn = ttk.Button(task_frame, text="✔️", command=lambda task_id=task_id: update_task(task_id),cursor="hand2")
            complete_btn.pack(side="left")
    
    def clear_frame():
        for frames in [today_frame, tomorrow_frame, previous_frame]:
            for widget in frames.winfo_children():
                widget.destroy()

    def add_task(): # insert entered data into the db (sub function)

        enter_task = task_entry.get()
        date = task_date_entry.get()
        complete = False
        u_name = username

        if enter_task != "" and date != "":
            query = "insert into todo(task_name, task_date, completion_status, u_name) values(%s, %s, %s, %s)"
            data = (enter_task, date, complete, u_name)
            pointer.execute(query, data)
            conn.commit()
            clear_frame()
            reload_task()
        elif enter_task == "":
            messagebox.showerror("add task", "Enter task")
            return
        elif date == "":
            messagebox.showerror("add task", "Enter date")
            return

    
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
    
    def display_completed_task():
        display_completed(username)
    
    def reload_task():
        load_task()


    user_name = tk.Label(root, text=f"welcome 👤{username}", font=('Consolas', 20), bg="#d9d9d9")
    user_name.place(relx=0.05, rely=0.02, width=400)

    seperator_line_name = ttk.Separator(root, orient='horizontal')
    seperator_line_name.place(x=0, y=79, width='2000')

    task_label = tk.Label(root, text="📝Enter your task :", font=('Consolas', 18), bg="#ffffff")
    task_label.place(relx=0.13, rely=0.13,anchor="center")

    task_entry = ttk.Entry(root, width=42, font=('Consolas', 13))
    task_entry.place(relx=0.32, rely =0.13, anchor="center", width=400)
    task_entry.focus()

    task_date_label = tk.Label(root, text="📅Enter your date (yyyy-mm-dd):", font=('Consolas', 18), bg="#ffffff")
    task_date_label.place(relx=0.48, rely=0.11)

    task_date_entry = ttk.Entry(root, width=20, font=('Consolas', 12))
    task_date_entry.place(relx=0.76, rely=0.12, width=300)

    task_add_btn = tk.Button(root, text="add task ", command=add_task, width=10, font=('Consolas', 15), bg="#ffffff",
                             cursor="hand2")
    task_add_btn.place(relx=0.215, rely=0.18)

    task_complete_btn = tk.Button(root, text="⚙️settings", command=display_completed_task, width=10, font=('Consolas', 15), bg="#ffffff", 
                                  cursor="hand2")
    task_complete_btn.place(relx=0.84, rely=0.02, width=200)

    today_frame = tk.LabelFrame(root, text="Due today", bg="#ffffff", font=('Consolas', 15))
    today_frame.place(relx=0.03, rely = 0.25)

    tomorrow_frame = LabelFrame(root, text="Due tomorrow", bg="#ffffff", font=('Consolas', 15))
    tomorrow_frame.place(relx=0.35, rely = 0.25)

    previous_frame = LabelFrame(root, text="Over due",bg="#ffffff", font=('Consolas', 15))
    previous_frame.place(relx=0.68, rely = 0.25)
  
    reload_task()

    root.mainloop()
    conn.close()

# task("suresh123")

