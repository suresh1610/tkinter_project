# main.py

import tkinter as tk
from tkinter import ttk
from login import todo_login
from signup import signup
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def open_login_window():
    todo_login()

def open_signup_window():
    signup()

root = tk.Tk()
root.title("Login / Sign Up")
root.geometry('500x200')
root.resizable(False, False)

login_label = ttk.Label(root, text="if you already have account --->")
login_label.place(relx=0.4, rely=0.3, anchor="center")

login_button = ttk.Button(root, text="Login", command=open_login_window)
login_button.place(relx=0.75, rely=0.3, anchor="center")

signup_label = ttk.Label(root, text="if you don't have account --->")
signup_label.place(relx=0.4, rely=0.5, anchor="center")

signup_button = ttk.Button(root, text="Sign Up", command=open_signup_window)
signup_button.place(relx=0.75, rely=0.5, anchor="center")

root.mainloop()


