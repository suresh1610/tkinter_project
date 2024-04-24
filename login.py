# login.py
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from signup import signup
import psycopg2
from todo import task
from ctypes import windll


windll.shcore.SetProcessDpiAwareness(1)


def login():
    def check_user():
        username = username_entry.get()
        password = password_entry.get()


        connection = psycopg2.connect(
            host = 'localhost',
            dbname = 'postgres',
            user = 'postgres',
            password = '12345',
            port = 5432
        )

        pointer = connection.cursor()
        query = 'select * from userdetails where username = %s and password = %s'
        data = (username, password)
        pointer.execute(query, data)
        user_detail = pointer.fetchall()

        if user_detail:
            messagebox.showinfo('login successfully', "welcome "+ username + " !!!")
            root.destroy()
            task()
        else:
            messagebox.showinfo('Login failed', "Invalid username and password")
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            login()
    
    root = tk.Tk()
    root.geometry('500x200')
    root.title('Login')
    root.resizable(False, False)

    username_label = ttk.Label(root, text="Enter your username:")
    username_label.grid(column=4, row=2, padx=10, pady=10)

    username_entry = ttk.Entry(root)
    username_entry.grid(column=5, row=2, padx=10, pady=10)
    username_entry.focus()

    password_label = ttk.Label(root, text="Enter your password:")
    password_label.grid(column=4, row=3, padx=10, pady=10)

    password_entry = ttk.Entry(root, show='*')
    password_entry.grid(column=5, row=3, padx=10, pady=10)

    login_btn = ttk.Button(root, text='Login', command=check_user)
    login_btn.grid(column=5, row=4, padx=10, pady=10)

    register_label = ttk.Label(root, text="if you don't have account--->", foreground="blue")
    register_label.grid(column=4, row=5, padx=10, pady=10)

    register_btn = ttk.Button(root, text="register", command=signup)
    register_btn.grid(column=5, row=5, padx =10, pady=10)

    root.mainloop()

