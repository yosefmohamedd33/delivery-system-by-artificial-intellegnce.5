from customtkinter import *
from tkinter import *
from PIL import Image, ImageTk
import os
import webbrowser
import time
import subprocess
import threading

# Colors
background_color = '#10181c'
entry_color = '#192028'
entry_focus_color = '#4272be'
button_color = '#256bfe'

root = Tk()
root.resizable(False, False)
root.title('Delivery System')
root.config(bg=background_color)

logo = Label(root,
             text='Login UI',
             font=('Montserrat Bold', 30),
             bg=background_color,
             fg='white')
logo.grid(row=0, padx=200, pady=60)

# EMAIL
email_frame = CTkFrame(root,
                     width=300,
                     fg_color=entry_color,
                     corner_radius=20,
                     border_width=1,
                     border_color=background_color,
                     bg_color=background_color)
email_frame.grid(row=1)

txt_email = CTkEntry(email_frame,
                     width=300,
                     placeholder_text_color='gray',
                     placeholder_text='Enter your Email',
                     border_width=0,
                     bg_color=entry_color,
                     font=('Montserrat', 16),
                     fg_color=('white', entry_color))
txt_email.grid(padx=10, pady=20)

# PASSWORD
password_frame = CTkFrame(root,
                         width=300,
                         fg_color=entry_color,
                         corner_radius=20,
                         border_width=1,
                         border_color=background_color,
                         bg_color=background_color)
password_frame.grid(row=2, pady=10)
txt_password = CTkEntry(password_frame,
                         width=300,
                         placeholder_text_color='gray',
                         placeholder_text='Enter your Password',
                         show='•',
                         border_width=0,
                         bg_color=entry_color,
                         font=('Montserrat', 16),
                         fg_color=('white', entry_color))
txt_password.grid(padx=10, pady=20)

# FORGOT PASSWORD
btn_forgot_password = Button(root,
                             border=0,
                             relief='flat',
                             bg=background_color,
                             fg='#236cfe',
                             text='Forgot Password?',
                             font=('Montserrat Medium', 10),
                             cursor='hand2',
                             activebackground=background_color,
                             activeforeground='white')
btn_forgot_password.grid(row=3)

# LOGIN
def login_action():
    email = txt_email.get()
    password = txt_password.get()
    
    # Check credentials
    if email == "admin" and password == "admin":
        # Open the next page (project options)
        root.destroy()
        open_project_options()  # Calls the function to open the project options page
        
        # Start Flask in a new thread
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.start()

        # Wait for the Flask server to be up
        time.sleep(2)  # This is just to give time for Flask to start
        open_map()
        
    else:
        # Show an error message
        error_label.config(text="Invalid username or password.", fg="red")

def open_map():
    # Open the map page in the web browser (Flask map interface)
    webbrowser.open('http://127.0.0.1:5000')
    
def run_flask():
    """Function to run the Flask app in a separate thread."""
    # Path to your main.py
    main_py_path = r"C:\Users\EL-MOHANDES\Desktop\AI PROJ\Project\project\project\main.py"

    # Start Flask in a separate thread
    def start_flask():
        subprocess.run(["python", main_py_path])
        
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.start()
        
        time.sleep(2)  # Adjust time if necessary to allow the server to start
        webbrowser.open("http://127.0.0.1:5000/")
        
btn_login = CTkButton(root,
                     width=300,
                     height=60,
                     corner_radius=20,
                     text='LOGIN',
                     border_width=0,
                     bg_color=background_color,
                     font=('Montserrat Medium', 20),
                     fg_color=('white', button_color),
                     hover_color=('black', '#257cfe'),
                     cursor='hand2',
                     command=login_action)  # Calls the login_action function
btn_login.grid(row=4, pady=10)

# Error message label (initially empty)
error_label = Label(root,
                    bg=background_color,
                    fg='red',
                    font=('Montserrat', 12),
                    text="")
error_label.grid(row=5)

# CEATE ACCOUNT
signup_frame = Frame(root,
                    bg=background_color)
signup_frame.grid(row=6)
lbl_signup = Label(signup_frame,
                    border=0,
                    relief='flat',
                    bg=background_color,
                    fg='gray',
                    text='Don\'t have an account?',
                    font=('Montserrat Medium', 10))
lbl_signup.grid(row=0, column=0)
btn_signup = Button(signup_frame,
                    border=0,
                    relief='flat',
                    bg=background_color,
                    fg='#236cfe',
                    text='Sign Up',
                    font=('Montserrat Medium', 10),
                    cursor='hand2',
                    activebackground=background_color,
                    activeforeground='white')
btn_signup.grid(row=0, column=1)

# CENTER WINDOW
root.update_idletasks()
width = root.winfo_reqwidth()
height = root.winfo_reqheight()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - width) // 2
y = (screen_height - height) // 2

root.geometry(f'{width}x{height}+{x}+{y-30}')

# Function to open the project options page
def open_project_options():
    # Create the project options window
    project_options = Tk()
    project_options.resizable(False, False)
    project_options.title('Project Options')
    project_options.config(bg=background_color)
    

    # Logo or title for the page
    logo = Label(project_options,
                 text='Project Dashboard',
                 font=('Montserrat Bold', 30),
                 bg=background_color,
                 fg='white')
    logo.grid(row=0, padx=200, pady=60)

    # Option 1: A button for the first feature in your project
    btn_option1 = CTkButton(project_options,
                            width=300,
                            height=60,
                            corner_radius=20,
                            text='Option 1 - A* Algorithm',
                            border_width=0,
                            bg_color=background_color,
                            font=('Montserrat Medium', 20),
                            fg_color=('white', button_color),
                            hover_color=('black', '#257cfe'),
                            cursor='hand2')
    btn_option1.grid(row=1, pady=10)

    # Option 2: A button for the second feature in your project
    btn_option2 = CTkButton(project_options,
                            width=300,
                            height=60,
                            corner_radius=20,
                            text='Option 2 - Map Visualization',
                            border_width=0,
                            bg_color=background_color,
                            font=('Montserrat Medium', 20),
                            fg_color=('white', button_color),
                            hover_color=('black', '#257cfe'),
                            cursor='hand2')
    btn_option2.grid(row=2, pady=10)

    # Option 3: A button for the third feature in your project
    btn_option3 = CTkButton(project_options,
                            width=300,
                            height=60,
                            corner_radius=20,
                            text='Option 3 - Delivery Routes',
                            border_width=0,
                            bg_color=background_color,
                            font=('Montserrat Medium', 20),
                            fg_color=('white', button_color),
                            hover_color=('black', '#257cfe'),
                            cursor='hand2')
    btn_option3.grid(row=3, pady=10)
    
#     btn_map = CTkButton(root,
#                     width=300,
#                     height=60,
#                     corner_radius=20,
#                     text='Open Map to Pick Point',
#                     border_width=0,
#                     bg_color=background_color,
#                     font=('Montserrat Medium', 20),
#                     fg_color=('white', button_color),
#                     hover_color=('black', '#257cfe'),
#                     cursor='hand2',
#                     command=open_map)  # Trigger open_map function when clicked
# btn_map.grid(row=5, pady=10)

    # Option 4: A button for logout
    btn_logout = CTkButton(project_options,
                           width=300,
                           height=60,
                           corner_radius=20,
                           text='Logout',
                           border_width=0,
                           bg_color=background_color,
                           font=('Montserrat Medium', 20),
                           fg_color=('white', '#f44336'),
                           hover_color=('black', '#f44336'),
                           cursor='hand2')
    btn_logout.grid(row=4, pady=10)


    # Center the window on the screen
    project_options.update_idletasks()
    width = project_options.winfo_reqwidth()
    height = project_options.winfo_reqheight()

    screen_width = project_options.winfo_screenwidth()
    screen_height = project_options.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    project_options.geometry(f'{width}x{height}+{x}+{y-30}')

    # Mainloop for the new window
    project_options.mainloop()

# MAINLOOP for the login page
root.mainloop()
