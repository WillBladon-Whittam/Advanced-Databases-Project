
import tkinter as tk
from typing import List, Dict

from advanced_database_project.backend.db_connection import DatabaseConnection
from advanced_database_project.gui.base_page import BasePage


class LoginPage(BasePage):
    """
    GUI Login Page - displayed when the application is first opened.
    Prompts the user to login with there credentials or register and create an account
    """
    
    def __init__(self, pages: List[tk.Frame], db: DatabaseConnection, user: Dict[str, str]):
        super().__init__(pages, db, user, create_base=False)
        self.configure(bg="#f7f7f7")
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.error = None
        
        self.create_login()
        
    def navigate_to(self, page):
        """
        Overide the default naviage_to function from BasePage - Reset the username and password Entry boxes after the page has changed.
        """
        self.username.set("")
        self.password.set("")
        self.error_label.configure(text="")
    
        self.pack_forget()
        page.show()

    def create_login(self):
        """
        Create the widgets for the login page.
        """
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
        welcome_label.pack(pady=(20, 20))
        
        login_frame = tk.Frame(self, bg="#f7f7f7")
        login_frame.grid(row=2, column=0, padx=(0, 20), pady=20) 
        
        username_label = tk.Label(
            login_frame, text="Username:", font=("Arial", 12), bg="#f7f7f7")
        username_label.grid(row=0, column=0, pady=5)
        
        self.username_entry = tk.Entry(login_frame, textvariable=self.username, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        password_label = tk.Label(
            login_frame, text="Password:", font=("Arial", 12), bg="#f7f7f7")
        password_label.grid(row=1, column=0, pady=5)
        
        self.password_entry = tk.Entry(login_frame, textvariable=self.password, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, padx=(0, 20), pady=5)
        
        self.error_label = tk.Label(login_frame, text="", font=("Arial", 12), bg="#f7f7f7", fg="#ff0000")
        self.error_label.grid(row=2, column=0, pady=(10, 0))
        
        login_button = tk.Button(login_frame, font=("Arial", 12), width=8, text="Login", command=self.validate_login)
        login_button.grid(row=2, column=1, pady=(10, 0))
        
        register_label = tk.Label(
            login_frame, text="Dont have an account?", font=("Arial", 12), bg="#f7f7f7")
        register_label.grid(row=3, column=0, pady=(10, 0))
        
        register_button = tk.Button(login_frame, font=("Arial", 12, "underline"), width=8, text="Register", bg="#f7f7f7", borderwidth=0, command=self.register)
        register_button.grid(row=3, column=1, pady=(10, 0))
        
    def validate_login(self):
        """
        Validate the information entered by the user.
        Check the username and password match in the database.
        Set the user information when the information is validated.
        """
        user = self.db.getCustomerByLogin(self.username.get(), self.password.get())
        if user is None:
            self.error_label.configure(text="Invalid Username")
        elif user is False:
            self.error_label.configure(text="Invalid Password")
        else:
            self.user["Firstname"] = user[1]
            self.user["Surname"] = user[2]
            self.user["Gender"] = user[3]
            self.user["Email"] = user[4]
            self.user["Username"] = user[5]
            self.user["Password"] = user[6]
            self.navigate_to(self.pages["Home"])
            
    def register(self):
        """
        Go to Register Page
        """
        self.navigate_to(self.pages["Register"])
