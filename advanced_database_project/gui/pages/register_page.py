
import tkinter as tk
import sqlite3
from advanced_database_project.gui.base_page import BasePage


class RegisterPage(BasePage):
    """
    GUI Register Page - displayed when a user creates an account
    """
    
    def __init__(self, pages, db, user):
        super().__init__(pages, db, user, create_base=False)
        self.configure(bg="#f7f7f7")
        
        # Initialise product search information variables
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.gender = tk.StringVar(value="Male")
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.password_confirm = tk.StringVar()
        self.error_label = None
        
        # Initialise Tkitner widgets attributes
        self.first_name_entry = None
        self.last_name_entry = None
        self.email_entry = None
        self.username_entry = None
        self.password_entry = None
        self.confirm_password_entry = None
        self.error_label = None
        
        self.create_register()

    def create_register(self):
        """
        Create the widgets for the register page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew") 
        
        register_message = tk.Frame(header_frame, bg="#e6e6e6", pady=20)
        register_message.pack(fill="x")
        register_message_label = tk.Label(
            register_message,
            text="Register!",
            font=("Arial", 24, "bold"),
            bg="#e6e6e6",
            fg="#333",
            width=50,
        )
        register_message_label.pack(pady=20)
        
        register_frame = tk.Frame(self, bg="#f7f7f7")
        register_frame.grid(row=2, column=0, padx=(0, 20), pady=20) 
        
        first_name_label = tk.Label(
            register_frame, text="First Name:", font=("Arial", 12), bg="#f7f7f7")
        first_name_label.grid(row=0, column=0, pady=5)
        
        self.first_name_entry = tk.Entry(register_frame, textvariable=self.first_name, font=("Arial", 12))
        self.first_name_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        last_name_label = tk.Label(
            register_frame, text="Last Name:", font=("Arial", 12), bg="#f7f7f7")
        last_name_label.grid(row=1, column=0, pady=5)
        
        self.last_name_entry = tk.Entry(register_frame, textvariable=self.last_name, font=("Arial", 12))
        self.last_name_entry.grid(row=1, column=1, padx=(0, 20), pady=5)
        
        gender_label = tk.Label(
            register_frame, text="Gender:", font=("Arial", 12), bg="#f7f7f7")
        gender_label.grid(row=2, column=0, pady=5)

        gender_buttons_frame = tk.Frame(register_frame, bg="#f7f7f7")
        gender_buttons_frame.grid(row=2, column=1, columnspan=2, pady=5, sticky="ew")

        male_button = tk.Radiobutton(gender_buttons_frame, text="Male", variable=self.gender, value="Male", bg="#f7f7f7")
        female_button = tk.Radiobutton(gender_buttons_frame, text="Female", variable=self.gender, value="Female", bg="#f7f7f7")

        male_button.grid(row=0, column=0, padx=(0, 20), pady=5)
        female_button.grid(row=0, column=1, padx=(0, 20), pady=5)
        
        email_label = tk.Label(
            register_frame, text="Email:", font=("Arial", 12), bg="#f7f7f7")
        email_label.grid(row=3, column=0, pady=5)
        
        self.email_entry = tk.Entry(register_frame, textvariable=self.email, font=("Arial", 12))
        self.email_entry.grid(row=3, column=1, padx=(0, 20), pady=5)

        username_label = tk.Label(
            register_frame, text="Username:", font=("Arial", 12), bg="#f7f7f7")
        username_label.grid(row=4, column=0, pady=5)
        
        self.username_entry = tk.Entry(register_frame, textvariable=self.username, font=("Arial", 12))
        self.username_entry.grid(row=4, column=1, padx=(0, 20), pady=5)
        
        password_label = tk.Label(
            register_frame, text="Password:", font=("Arial", 12), bg="#f7f7f7")
        password_label.grid(row=5, column=0, pady=5)
        
        self.password_entry = tk.Entry(register_frame, textvariable=self.password, font=("Arial", 12), show="*")
        self.password_entry.grid(row=5, column=1, padx=(0, 20), pady=5)
        
        confirm_password_label = tk.Label(
            register_frame, text="Confirm Password:", font=("Arial", 12), bg="#f7f7f7")
        confirm_password_label.grid(row=6, column=0, pady=5)
        
        self.confirm_password_entry = tk.Entry(register_frame, textvariable=self.password_confirm, font=("Arial", 12), show="*")
        self.confirm_password_entry.grid(row=6, column=1, padx=(0, 20), pady=5)
        
        self.error_label = tk.Label(register_frame, font=("Arial", 12), bg="#f7f7f7", fg="#ff0000")
        self.error_label.grid(row=7, column=0, pady=(10, 0))
        
        register_button = tk.Button(register_frame, font=("Arial", 12), width=8, text="Register", command=self.register)
        register_button.grid(row=7, column=1, pady=(10, 0))
        
    @staticmethod
    def validate_field(value: str, entry_widget: tk.Entry):
        """
        Validates a field and updates its Entry based on whether it is filled.

        Args:
            value (str): The value to check taht isn't empty
            entry_widget (tk.Entry): The tkitner widget that needs updating
        """   
        if not value:
            entry_widget.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            return False
        else:
            entry_widget.config(highlightthickness=0)
            return True

    def register(self):
        """
        Register a new customer.
        - Username needs to be unique
        - Passwords need to match
        - All fields need to be filled in.
        """
        error = False

        field_entries = [
            (self.first_name.get(), self.first_name_entry),
            (self.last_name.get(), self.last_name_entry),
            (self.email.get(), self.email_entry),
            (self.username.get(), self.username_entry),
            (self.password.get(), self.password_entry),
            (self.password_confirm.get(), self.confirm_password_entry),
        ]

        for value, entry in field_entries:
            if not self.validate_field(value, entry):
                error = True

        # Check if passwords match
        if self.password.get() and self.password_confirm.get():
            if self.password.get() != self.password_confirm.get():
                self.password_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.confirm_password_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.error_label.configure(text="Passwords do not match!")
                error = True
            else:
                self.error_label.configure(text="")
                self.password_entry.config(highlightthickness=0)
                self.confirm_password_entry.config(highlightthickness=0)

        if not error:
            result = self.db.insertCustomer(
                self.first_name.get(),
                self.last_name.get(),
                self.gender.get(),
                self.email.get(),
                self.username.get(),
                self.password.get()
            )

            if isinstance(result, sqlite3.IntegrityError):
                self.error_label.configure(text="Username is already taken!")
                self.username_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            elif isinstance(result, sqlite3.Error):
                self.error_label.configure(text="Database Error!")
            else:
                self.user["Firstname"] = self.first_name.get()
                self.user["Surname"] = self.last_name.get()
                self.user["Gender"] = self.gender.get()
                self.user["Email"] = self.email.get()
                self.user["Username"] = self.username.get()
                self.user["Password"] = self.password.get()
                self.navigate_to(self.pages["Home"])