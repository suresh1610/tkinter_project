# main.py
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import re
from todo import task
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

def open_login_window(): 
    main_frame.pack_forget()
    user_login()

def open_signup_window():
    main_frame.pack_forget()
    user_signup()


# database connection "connection and pointer is globel variables"
connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="pumo_project"
        )

pointer = connection.cursor() # pointer 

def user_login():
    def register_user():
        login_frame.destroy()
        user_signup()
    def check_user():
        username = username_entry.get()
        password = password_entry.get()

        query = 'select * from userdetails where username = %s and password = %s'
        data = (username, password)
        pointer.execute(query, data)
        user_detail = pointer.fetchall()

        if user_detail:
            messagebox.showinfo('login successfully', "welcome "+ username + " !!!")
            main_root.destroy()
            task(username)
         # Here i calling task function from todo.py and pass the username to that file
        else:
            messagebox.showinfo('Login failed', "Invalid username and password")
            username_entry.delete(0, END)
            password_entry.delete(0, END)
    
    # login_window = tk.Tk()
    # # login_window.geometry('500x200')
    # login_window.title('Login')
    # login_window.state("zoomed")
    # login_window.resizable(False, False)
    login_frame = tk.Frame(main_root)
    login_frame.place(x=0, y=0, relwidth=1, relheight=1)

    image = Image.open("C:\\Users\\sures\\Downloads\\Todonew\\2.png")
    resize_login = image.resize((1920, 1080))  # Resize the image to fit the window size
    img = ImageTk.PhotoImage(resize_login)
    label_login = Label(login_frame, image=img)
    label_login.image = img
    label_login.place(x=0, y=0, relwidth=1, relheight=1)

    login_label = tk.Label(login_frame, text="Login",bg="#d9d9d9", font=('Consolas', 40))
    login_label.place(relx=0.5, rely=0.2, anchor="center")

    username_label = tk.Label(login_frame, text="👤username:", bg="#d9d9d9", font=('Consolas', 25))
    username_label.place(relx=0.42, rely=0.3, anchor="center")

    username_entry = ttk.Entry(login_frame, font=('Consolas', 20))
    username_entry.place(relx=0.57, rely=0.3, anchor="center", width=300)
    username_entry.focus()

    password_label = tk.Label(login_frame, text="🔐password:",bg="#d9d9d9", font=('Consolas', 25))
    password_label.place(relx=0.42, rely=0.4, anchor="center")

    password_entry = ttk.Entry(login_frame, show='*', font=('Consolas', 20))
    password_entry.place(relx=0.57, rely=0.4, anchor="center", width=300)

    login_btn = tk.Button(login_frame, text='Login', command=check_user, font=('Consolas', 15), bg="#ffffff",cursor="hand2")
    login_btn.place(relx=0.5, rely=0.5, anchor="center", width=300)

    register_label = tk.Label(login_frame, text="if you don't have account--->", foreground="blue", background="#d9d9d9")
    register_label.place(relx=0.47, rely=0.6, anchor="center")

    register_btn = tk.Button(login_frame, text="register", command=register_user, bg="#ffffff",cursor="hand2")
    register_btn.place(relx=0.55, rely=0.6, anchor="center", width=80)

    # login_window.mainloop()

def user_signup():
    def already_user():
        signup_frame.pack_forget()
        user_login()

    def validate_username(username):
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$', username)) # Username must contain at least one letter and one number

    def validate_password(password):
        # Password must contain at least one letter, one number, and one special character
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$', password)) 

    def register():
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        repassword = confirm_password_entry.get()

        if not validate_username(username):
            messagebox.showerror("sign up", "Username and password must contain at least one letter, one number and special character")
            return
        elif not validate_password(password):
            messagebox.showerror("sign up", "Password must contain at least one letter, one number and special character")
            return
        elif password != repassword:
            messagebox.showerror("sign up", "Incorrect password, password and retype password have to be same")
            return

        elif validate_username(username) and validate_password(password) and validate_password(repassword):
            try:
                insert_query = 'insert into userdetails(username, email, password, first_name, last_name) values(%s, %s, %s, %s, %s)'
                date = (username, email, password, firstname, lastname)
                pointer.execute(insert_query, date)
                connection.commit()
                messagebox.showinfo("Sign up","your data is successfully registered")
                main_root.destroy()
                task(username)  # Here i calling task function from todo.py and pass the username to that file
                return
            except mysql.connector.errors.IntegrityError as error:
                messagebox.showinfo("sign up", "The username already exist, Please choose a different username")
                # signup_window.destroy()
                # signup()
                return
    
    # def see_passwd():
    #     if password_entry['show'] == '*':
    #         password_entry.config(show="")
    #         password_sh.config(text="O",font=('Consoles',10))
    #     else:
    #         password_entry.config(show="*")
    #         password_sh.config(text="⌀",font=('Consoles',10))


    table_creation_query = 'create table if not exists userdetails(username varchar(30) primary key, email varchar(40), password varchar(15))'
    pointer.execute(table_creation_query)
    connection.commit()

# Create signup window
    # signup_window = tk.Tk()
    # signup_window.state("zoomed")
    # signup_window.resizable(False, False)
    # # signup_window.geometry('500x200')
    signup_frame = tk.Frame(main_root)
    signup_frame.place(x=0, y=0, relwidth=1, relheight=1)

    image = Image.open("C:\\Users\\sures\\Downloads\\Todonew\\3.png")
    resize_login = image.resize((1920, 1080))  # Resize the image to fit the window size
    img = ImageTk.PhotoImage(resize_login)
    label_signup = Label(signup_frame, image=img)
    label_signup.image = img
    label_signup.place(x=0, y=0, relwidth=1, relheight=1)

    # image = Image.open("C:\\Users\\sures\\Downloads\\Todonew\\3.png")
    # resize_login = image.resize((1920, 1080))
    # img = ImageTk.PhotoImage(resize_login)
    # label_login = Label(image=img)
    # label_login.image = img
    # label_login.pack()

    signup_label = tk.Label(signup_frame, text="Sign up", bg="#d9d9d9",fg="#444242", font=('Consolas', 40))
    signup_label.place(relx=0.5, rely=0.15, anchor="center")

    first_name_label = tk.Label(signup_frame, text="First name:", bg="#d9d9d9", font=('Consolas', 20))
    first_name_label.place(relx=0.4, rely=0.25, anchor="center")

    first_name_entry = ttk.Entry(signup_frame,font=('Consolas', 20))
    first_name_entry.place(relx=0.576, rely=0.25, anchor="center", width=300)
    first_name_entry.focus()

    last_name_label = tk.Label(signup_frame, text="last name  :", bg="#d9d9d9", font=('Consolas', 20))
    last_name_label.place(relx=0.4, rely=0.33, anchor="center")

    last_name_entry = ttk.Entry(signup_frame,font=('Consolas', 20))
    last_name_entry.place(relx=0.576, rely=0.32, anchor="center", width=300)
    
    username_label = tk.Label(signup_frame, text="👤username :", bg="#d9d9d9", font=('Consolas', 20))
    username_label.place(relx=0.4, rely=0.4, anchor="center")

    username_entry = ttk.Entry(signup_frame, font=('Consolas', 20))
    username_entry.place(relx=0.576, rely=0.4, anchor="center", width=300)

    username_detail_label = tk.Label(signup_frame, text="• username must have atleast one number and minimum 5 letters", bg="#d9d9d9", font=('Consolas', 10))
    username_detail_label.place(relx=0.496, rely=0.45, anchor="center")

    # first_name_label = tk.Label(signup_window, text="First Name:", bg="#d9d9d9", font=('Consolas', 20))
    # first_name_label.place(relx=0.4, rely=0.35, anchor="center")

    email_label = tk.Label(signup_frame, text="Ⓜ Email   :", bg="#d9d9d9", font=('Consolas', 20))
    email_label.place(relx=0.4, rely=0.5, anchor="center")

    email_entry = ttk.Entry(signup_frame, font=('Consolas', 20))
    email_entry.place(relx=0.576, rely=0.5, anchor="center", width=300)

    password_label = tk.Label(signup_frame, text="🔐password :",bg="#d9d9d9", font=('Consolas', 20))
    password_label.place(relx=0.4, rely=0.57, anchor="center")

    password_entry = ttk.Entry(signup_frame, show="*", font=('Consolas', 20))
    password_entry.place(relx=0.576, rely=0.57, anchor="center", width=300)

    password_1_detail_label = tk.Label(signup_frame, text="• password must have atleast one number and one letter",bg="#d9d9d9", font=('Consolas', 10))
    password_1_detail_label.place(relx=0.48, rely=0.61, anchor="center")

    password_2_detail_label = tk.Label(signup_frame, text="• password must have atleast one special character",bg="#d9d9d9", font=('Consolas', 10))
    password_2_detail_label.place(relx=0.471, rely=0.63, anchor="center")

    password_3_detail_label = tk.Label(signup_frame, text="• password must have more than 5 characters",bg="#d9d9d9", font=('Consolas', 10))
    password_3_detail_label.place(relx=0.454, rely=0.65, anchor="center")

    confirm_password_label = tk.Label(signup_frame, text="🔐Retype password:",bg="#d9d9d9", font=('Consolas', 20))
    confirm_password_label.place(relx=0.43, rely=0.7, anchor="center")

    confirm_password_entry = ttk.Entry(signup_frame, show="*", font=('Consolas', 20))
    confirm_password_entry.place(relx=0.59, rely=0.7, anchor="center", width=250)

    signup_button = tk.Button(signup_frame, text="Sign Up", command=register, font=('Consolas', 15), bg="#ffffff",cursor="hand2")
    signup_button.place(relx=0.50, rely=0.8, anchor="center", width="300")

    already_un_label = tk.Label(signup_frame, text="if you already have account--->", foreground="blue", background="#d9d9d9")
    already_un_label.place(relx=0.47, rely=0.88, anchor="center")

    register_btn = tk.Button(signup_frame, text="login", command=already_user, bg="#ffffff",cursor="hand2")
    register_btn.place(relx=0.56, rely=0.88, anchor="center", width=80)

    # signup_window.mainloop()

main_root = Tk()
main_root.title("Login / Sign Up")
main_root.state("zoomed")
main_root.resizable(False, False)

main_frame = tk.Frame(main_root)
main_frame.place(x=0, y=0, relwidth=1, relheight=1)

image = Image.open("C:\\Users\\sures\\Downloads\\Todo\\1.png")
resize_login = image.resize((1920, 1080))  # Resize the image to fit the window size
img = ImageTk.PhotoImage(resize_login)
label_main = Label(main_frame, image=img)
label_main.image = img
label_main.place(x=0,y=0,relwidth=1, relheight=1)

# login_label = ttk.Label(mamainot, text="if you already have account --->")
# login_label.place(relx=0.4, rely=0.3, anchor="center")

login_button = tk.Button(main_frame, text="Login",command=open_login_window, font=('Consolas', 15), bg="#ffffff", cursor="hand2")
login_button.place(relx=0.8, rely=0.38, anchor="center", width=350)

# signup_label = ttk.Label(main_root, text="if you don't have account --->")
# signup_label.place(relx=0.4, rely=0.5, anchor="center")

signup_button = tk.Button(main_frame, text="Sign Up", command=open_signup_window, font=('Consolas', 15), bg="#ffffff", 
                         cursor="hand2")
signup_button.place(relx=0.8, rely=0.55, anchor="center", width=350)

main_root.mainloop()