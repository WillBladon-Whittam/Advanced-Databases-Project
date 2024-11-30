
import tkinter as tk
import hashlib
from advanced_database_project.gui.base_page import BasePage


class LoginPage(BasePage):
    """
    GUI Home Page - displayed when the application is first opened.
    """
    
    def __init__(self, pages, db):
        super().__init__(pages, db, create_base=False)
        self.configure(bg="#f7f7f7")
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.error = None
        
        self.create_login()

    def create_login(self):
        welcome_frame = tk.Frame(self, bg="#f7f7f7")
        welcome_frame.grid(row=1, column=0, sticky="nsew") 
        
        welcome = tk.Frame(welcome_frame, bg="#e6e6e6", pady=20)
        welcome.pack(fill="x")
        welcome_label = tk.Label(
            welcome,
            text="Login to the Online Hardware Store!",
            font=("Arial", 24, "bold"),
            bg="#e6e6e6",
            fg="#333",
            width=50,
        )
        welcome_label.pack(pady=(30, 10))
        
        login_frame = tk.Frame(self, bg="#f7f7f7")
        login_frame.grid(row=2, column=0, padx=(0, 20), pady=20) 
        
        username_label = tk.Label(
            login_frame, text="Username:", font=("Arial", 12), bg="#f7f7f7")
        username_label.grid(row=0, column=0, pady=5)
        
        username_entry = tk.Entry(login_frame, textvariable=self.username, font=("Arial", 12))
        username_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        password_label = tk.Label(
            login_frame, text="Password:", font=("Arial", 12), bg="#f7f7f7")
        password_label.grid(row=1, column=0, pady=5)
        
        password_entry = tk.Entry(login_frame, textvariable=self.password, font=("Arial", 12), show="*")
        password_entry.grid(row=1, column=1, padx=(0, 20), pady=5)
        
        self.error_label = tk.Label(login_frame, text="", font=("Arial", 12), bg="#f7f7f7", fg="#ff0000")
        self.error_label.grid(row=2, column=0, pady=(10, 0))
        
        login_button = tk.Button(login_frame, font=("Arial", 12), width=8, text="Login", command=self.validate_login)
        login_button.grid(row=2, column=1, pady=(10, 0))
        
        register_label = tk.Label(
            login_frame, text="Dont have an account?", font=("Arial", 12), bg="#f7f7f7")
        register_label.grid(row=3, column=0, pady=(10, 0))
        
        register_button = tk.Button(login_frame, font=("Arial", 12, "underline"), width=8, text="Register", bg="#f7f7f7", borderwidth=0)
        register_button.grid(row=3, column=1, pady=(10, 0))
        
    def validate_login(self):
        user = self.db.getCustomerByLogin(self.username.get(), self.password.get())
        if user is None:
            self.error_label.configure(text="Invalid Username")
        elif user is False:
            self.error_label.configure(text="Invalid Password")
        else:
            self.user = user
            self.navigate_to(self.pages["Home"])
