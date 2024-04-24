# signup.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import psycopg2 
from ctypes import windll
from todo import task

windll.shcore.SetProcessDpiAwareness(1)

def signup():
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
                task()
                return
            except psycopg2.errors.UniqueViolation as error:
                messagebox.showinfo("sign up", "The username already exist, Please choose a different username")
                signup_window.destroy()
                signup()
                return
    
    connection = psycopg2.connect(  # here i am connect to database
        host = 'localhost',
        dbname = 'postgres',
        user = 'postgres',
        password = '12345',
        port = 5432
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