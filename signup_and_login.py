# main.py

import tkinter as tk
from tkinter import ttk
# from login import user_login
# from signup import signup
from tkinter import *
from tkinter import messagebox
# from signup import signup
import mysql.connector
import psycopg2
import re
from todo import task
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def open_login_window():
    main_root.destroy()
    user_login()

def open_signup_window():
    main_root.destroy()
    user_signup()

def user_login():
    def check_user():
        username = username_entry.get()
        password = password_entry.get()


        connection = mysql.connector.connect(  # here i am connect to database
            host="localhost",
            user="root",
            passwd="",
            database="pumo_project"
        )

        pointer = connection.cursor()
        query = 'select * from userdetails where username = %s and password = %s'
        data = (username, password)
        pointer.execute(query, data)
        user_detail = pointer.fetchall()

        if user_detail:
            messagebox.showinfo('login successfully', "welcome "+ username + " !!!")
            login_window.destroy()
            task(username)
         # Here i calling task function from todo.py and pass the username to that file
        else:
            messagebox.showinfo('Login failed', "Invalid username and password")
            username_entry.delete(0, END)
            password_entry.delete(0, END)
    
    login_window = tk.Tk()
    login_window.geometry('500x200')
    login_window.title('Login')
    login_window.resizable(False, False)

    username_label = ttk.Label(login_window, text="Enter your username:")
    username_label.grid(column=4, row=2, padx=10, pady=10)

    username_entry = ttk.Entry(login_window)
    username_entry.grid(column=5, row=2, padx=10, pady=10)
    username_entry.focus()

    password_label = ttk.Label(login_window, text="Enter your password:")
    password_label.grid(column=4, row=3, padx=10, pady=10)

    password_entry = ttk.Entry(login_window, show='*')
    password_entry.grid(column=5, row=3, padx=10, pady=10)

    login_btn = ttk.Button(login_window, text='Login', command=check_user)
    login_btn.grid(column=5, row=4, padx=10, pady=10)

    register_label = ttk.Label(login_window, text="if you don't have account--->", foreground="blue")
    register_label.grid(column=4, row=5, padx=10, pady=10)

    register_btn = ttk.Button(login_window, text="register", command=user_signup)
    register_btn.grid(column=5, row=5, padx =10, pady=10)

    login_window.mainloop()

def user_signup():
    def validate_username(username):
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$', username)) # Username must contain at least one letter and one number

    def validate_password(password):
        # Password must contain at least one letter, one number, and one special character
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$', password)) 

    def register():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not validate_username(username):
            messagebox.showerror("sign up", "Username and password must contain at least one letter, one number and special character")
            return
        elif not validate_password(password):
            messagebox.showerror("sign up", "Password must contain at least one letter, one number and special character")
            return

        elif validate_username(username) and validate_password(password):
            try:
                insert_query = 'insert into userdetails(username, email, password) values(%s, %s, %s)'
                date = (username, email, password)
                pointer.execute(insert_query, date)
                connection.commit()
                messagebox.showinfo("Sign up","your data is successfully registered")
                signup_window.destroy()
                task(username)  # Here i calling task function from todo.py and pass the username to that file
                return
            except mysql.connector.errors.IntegrityError as error:
                messagebox.showinfo("sign up", "The username already exist, Please choose a different username")
                signup_window.destroy()
                # signup()
                return
    
    connection = mysql.connector.connect(  # here i am connect to database
        host="localhost",
        user="root",
        passwd="",
        database="pumo_project"
    )

    pointer = connection.cursor() # creating cursor

    table_creation_query = 'create table if not exists userdetails(username varchar(30) primary key, email varchar(40), password varchar(15))'
    pointer.execute(table_creation_query)
    connection.commit()

# Create signup window
    signup_window = tk.Tk()
    signup_window.title("Sign Up")
    signup_window.resizable(False, False)
    signup_window.geometry('500x200')
    
    username_label = ttk.Label(signup_window, text="Username:")
    username_label.grid(column=3, row=0, padx=10, pady=10)

    username_entry = ttk.Entry(signup_window)
    username_entry.grid(column=4, row=0, padx=10, pady=10)

    email_label = ttk.Label(signup_window, text="Email:")
    email_label.grid(column=3, row=1, padx=10, pady=10)

    email_entry = ttk.Entry(signup_window)
    email_entry.grid(column=4, row=1, padx=10, pady=10)

    password_label = ttk.Label(signup_window, text="Password:")
    password_label.grid(column=3, row=2, padx=10, pady=10)

    password_entry = ttk.Entry(signup_window, show="*")
    password_entry.grid(column=4, row=2, padx=10, pady=10)

    signup_button = ttk.Button(signup_window, text="Sign Up", command=register)
    signup_button.grid(column=4, row=3, padx=10, pady=10)

    signup_window.mainloop()

main_root = Tk()
main_root.title("Login / Sign Up")
main_root.geometry('500x200')
main_root.resizable(False, False)

login_label = ttk.Label(main_root, text="if you already have account --->")
login_label.place(relx=0.4, rely=0.3, anchor="center")

login_button = ttk.Button(main_root, text="Login", command=open_login_window)
login_button.place(relx=0.75, rely=0.3, anchor="center")

signup_label = ttk.Label(main_root, text="if you don't have account --->")
signup_label.place(relx=0.4, rely=0.5, anchor="center")

signup_button = ttk.Button(main_root, text="Sign Up", command=open_signup_window)
signup_button.place(relx=0.75, rely=0.5, anchor="center")

main_root.mainloop()


