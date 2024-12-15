import tkinter as tk
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, Any

from advanced_database_project.gui.base_page import BasePage
from advanced_database_project.backend.db_connection import DatabaseConnection


class RegisterPage(BasePage):
    """
    GUI Register Page - displayed when a user creates an account
    """

    def __init__(self, pages: Dict[str, BasePage], db: DatabaseConnection, user: Dict[str, Any],
                 basket: Dict[str, Any]):
        super().__init__(pages, db, user, basket, create_base=False)
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

        self.entries = {}

        self.create_widgets()

    def navigate_to(self, page: BasePage) -> None:
        """
        Override the default navigate_to function from BasePage - Reset the all Entry boxes after the page has changed.
        """
        self.first_name.set("")
        self.last_name.set("")
        self.gender.set("Male")
        self.email.set("")
        self.username.set("")
        self.password.set("")
        self.password_confirm.set("")
        self.error_label.configure(text="")

        self.pack_forget()
        page.show()

    def create_widgets(self) -> None:
        """
        Create the widgets for the register page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew")

        register_message = tk.Frame(header_frame, bg="#e6e6e6", pady=20)
        register_message.pack(fill="x")
        register_message_label = tk.Label(
            register_message, text="Register!", font=("Arial", 24, "bold"), bg="#e6e6e6", fg="#333", width=50)
        register_message_label.pack(pady=20)

        register_frame = tk.Frame(self, bg="#f7f7f7")
        register_frame.grid(row=2, column=0, padx=(0, 20), pady=20)

        first_name_label = tk.Label(register_frame, text="First Name:", font=("Arial", 12), bg="#f7f7f7")
        first_name_label.grid(row=0, column=0, pady=5)

        self.entries["first_name"] = tk.Entry(register_frame, textvariable=self.first_name, font=("Arial", 12))
        self.entries["first_name"].grid(row=0, column=1, padx=(0, 20), pady=5)

        last_name_label = tk.Label(register_frame, text="Last Name:", font=("Arial", 12), bg="#f7f7f7")
        last_name_label.grid(row=1, column=0, pady=5)

        self.entries["last_name"] = tk.Entry(register_frame, textvariable=self.last_name, font=("Arial", 12))
        self.entries["last_name"].grid(row=1, column=1, padx=(0, 20), pady=5)

        gender_label = tk.Label(register_frame, text="Gender:", font=("Arial", 12), bg="#f7f7f7")
        gender_label.grid(row=2, column=0, pady=5)

        gender_buttons_frame = tk.Frame(register_frame, bg="#f7f7f7")
        gender_buttons_frame.grid(row=2, column=1, columnspan=2, pady=5, sticky="ew")

        male_button = tk.Radiobutton(
            gender_buttons_frame, text="Male", variable=self.gender, value="Male", bg="#f7f7f7")
        female_button = tk.Radiobutton(
            gender_buttons_frame, text="Female", variable=self.gender, value="Female", bg="#f7f7f7")

        male_button.grid(row=0, column=0, padx=(0, 20), pady=5)
        female_button.grid(row=0, column=1, padx=(0, 20), pady=5)

        email_label = tk.Label(
            register_frame, text="Email:", font=("Arial", 12), bg="#f7f7f7")
        email_label.grid(row=3, column=0, pady=5)

        self.entries["email"] = tk.Entry(register_frame, textvariable=self.email, font=("Arial", 12))
        self.entries["email"].grid(row=3, column=1, padx=(0, 20), pady=5)

        username_label = tk.Label(register_frame, text="Username:", font=("Arial", 12), bg="#f7f7f7")
        username_label.grid(row=4, column=0, pady=5)

        self.entries["username"] = tk.Entry(register_frame, textvariable=self.username, font=("Arial", 12))
        self.entries["username"].grid(row=4, column=1, padx=(0, 20), pady=5)

        password_label = tk.Label(register_frame, text="Password:", font=("Arial", 12), bg="#f7f7f7")
        password_label.grid(row=5, column=0, pady=5)

        self.entries["password"] = tk.Entry(register_frame, textvariable=self.password, font=("Arial", 12), show="*")
        self.entries["password"].grid(row=5, column=1, padx=(0, 20), pady=5)

        confirm_password_label = tk.Label(register_frame, text="Confirm Password:", font=("Arial", 12), bg="#f7f7f7")
        confirm_password_label.grid(row=6, column=0, pady=5)

        self.entries["password_confirm"] = tk.Entry(
            register_frame, textvariable=self.password_confirm, font=("Arial", 12), show="*")
        self.entries["password_confirm"].grid(row=6, column=1, padx=(0, 20), pady=5)

        self.error_label = tk.Label(register_frame, font=("Arial", 12), bg="#f7f7f7", fg="#ff0000")
        self.error_label.grid(row=7, column=0, pady=(10, 0))

        register_button = tk.Button(
            register_frame, font=("Arial", 12), width=8, text="Register", command=self.register_user)
        register_button.grid(row=7, column=1, pady=(10, 0))

        go_back_button = tk.Button(
            register_frame, font=("Arial", 12), width=8, text="Back", command=self.return_to_login)
        go_back_button.grid(row=7, column=2, pady=(10, 0))

    def return_to_login(self) -> None:
        """
        Return back to the Login Page
        """
        self.navigate_to(self.pages["Login"])

    def register_user(self) -> None:
        """
        Register a new customer.
        - Username needs to be unique
        - Passwords need to match
        - All fields need to be filled in.
        """
        error = False

        field_entries = [
            (self.first_name.get(), self.entries["first_name"]),
            (self.last_name.get(), self.entries["last_name"]),
            (self.email.get(), self.entries["email"]),
            (self.username.get(), self.entries["username"]),
            (self.password.get(), self.entries["password"]),
            (self.password_confirm.get(), self.entries["password_confirm"]),
        ]

        for value, entry in field_entries:
            if not self.validate_field(value, entry):
                error = True

        # Check if passwords match
        if self.password.get() and self.password_confirm.get():
            if self.password.get() != self.password_confirm.get():
                self.entries["password"].config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.entries["password_confirm"].config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.error_label.configure(text="Passwords do not match!")
                error = True
            else:
                self.error_label.configure(text="")
                self.entries["password"].config(highlightthickness=0)
                self.entries["password_confirm"].config(highlightthickness=0)

        if not error:
            result = self.db.insert_customer(
                self.first_name.get(),
                self.last_name.get(),
                self.gender.get(),
                self.email.get(),
                self.username.get(),
                self.password.get()
            )

            if isinstance(result, sqlite3.IntegrityError):
                self.error_label.configure(text="Username is already taken!")
                self.entries["username"].config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            elif isinstance(result, sqlite3.Error):
                self.error_label.configure(text="Database Error!")
            else:
                self.user["Customer_ID"] = self.db.cursor.lastrowid
                self.user["Customer_Firstname"] = self.first_name.get()
                self.user["Customer_Surname"] = self.last_name.get()
                self.user["Customer_Gender"] = self.gender.get()
                self.user["Customer_Email"] = self.email.get()
                self.user["Customer_Username"] = self.username.get()
                self.user["Customer_Password"] = hashlib.sha256(self.password.get().encode()).digest()

                basket = self.db.get_basket_by_customer_id(self.user["Customer_ID"])
                if basket is None:
                    self.db.create_basket_by_customer_id(self.user["Customer_ID"], datetime.now().strftime("%d/%m/%Y"))
                    self.basket.update(self.db.get_basket_by_customer_id(self.user["Customer_ID"]))
                else:
                    self.basket.update(basket)

                self.navigate_to(self.pages["Home"])
