import tkinter as tk
import hashlib
import sqlite3
from typing import Dict, Any

from advanced_database_project.gui.base_page import BasePage
from advanced_database_project.backend.db_connection import DatabaseConnection


class AccountPage(BasePage):
    """
    GUI Account Page - Displayed information about the customer, allows customers to edit there information and logout
    """

    def __init__(self, pages: Dict[str, BasePage], db: DatabaseConnection, user: Dict[str, Any],
                 basket: Dict[str, Any]):
        super().__init__(pages, db, user, basket)
        self.configure(bg="#f7f7f7")

        # Initialise account information variables
        self.vars = {
            "first_name": tk.StringVar(),
            "last_name": tk.StringVar(),
            "gender": tk.StringVar(),
            "email": tk.StringVar(),
            "username": tk.StringVar(),
            "password": tk.StringVar(),
            "password_confirm": tk.StringVar(),
        }

        self.entries = {}

        self.error_label = None

        self.create_widgets()

    def show(self) -> None:
        """
        Override the default show function from BasePage - set the Entry boxs to the users information.
        This can't be done when the Entry boxs are created as the user hasn't logged in yet, and the user can change.
        """
        self.vars["first_name"].set(self.user["Customer_Firstname"])
        self.vars["last_name"].set(self.user["Customer_Surname"])
        self.vars["gender"].set(self.user["Customer_Gender"])
        self.vars["email"].set(self.user["Customer_Email"])
        self.vars["username"].set(self.user["Customer_Username"])
        self.vars["password"].set("")
        self.vars["password_confirm"].set("")
        self.pack()

    def create_widgets(self) -> None:
        """
        Create the widgets for the accounts page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew")

        register_message = tk.Frame(header_frame, bg="#e6e6e6", pady=20)
        register_message.pack(fill="x")
        register_message_label = tk.Label(
            register_message,
            text="Your Account",
            font=("Arial", 24, "bold"),
            bg="#e6e6e6",
            fg="#333",
            width=50,
        )
        register_message_label.pack(pady=10)

        register_frame = tk.Frame(self, bg="#f7f7f7")
        register_frame.grid(row=2, column=0, padx=(0, 20), pady=20)

        first_name_label = tk.Label(
            register_frame, text="First Name:", font=("Arial", 12), bg="#f7f7f7")
        first_name_label.grid(row=0, column=0, pady=5)

        self.entries["first_name"] = tk.Entry(register_frame, textvariable=self.vars["first_name"], font=("Arial", 12))
        self.entries["first_name"].grid(row=0, column=1, padx=(0, 20), pady=5)

        last_name_label = tk.Label(
            register_frame, text="Last Name:", font=("Arial", 12), bg="#f7f7f7")
        last_name_label.grid(row=1, column=0, pady=5)

        self.entries["last_name"] = tk.Entry(register_frame, textvariable=self.vars["last_name"], font=("Arial", 12))
        self.entries["last_name"].grid(row=1, column=1, padx=(0, 20), pady=5)

        gender_label = tk.Label(
            register_frame, text="Gender:", font=("Arial", 12), bg="#f7f7f7")
        gender_label.grid(row=2, column=0, pady=5)

        gender_buttons_frame = tk.Frame(register_frame, bg="#f7f7f7")
        gender_buttons_frame.grid(row=2, column=1, columnspan=2, pady=5, sticky="ew")

        self.entries["male_button"] = tk.Radiobutton(
            gender_buttons_frame, text="Male", variable=self.vars["gender"], value="Male", bg="#f7f7f7")
        self.entries["female_button"] = tk.Radiobutton(
            gender_buttons_frame, text="Female", variable=self.vars["gender"], value="Female", bg="#f7f7f7")

        self.entries["male_button"].grid(row=0, column=0, padx=(0, 20), pady=5)
        self.entries["female_button"].grid(row=0, column=1, padx=(0, 20), pady=5)

        email_label = tk.Label(
            register_frame, text="Email:", font=("Arial", 12), bg="#f7f7f7")
        email_label.grid(row=3, column=0, pady=5)

        self.entries["email"] = tk.Entry(register_frame, textvariable=self.vars["email"], font=("Arial", 12))
        self.entries["email"].grid(row=3, column=1, padx=(0, 20), pady=5)

        username_label = tk.Label(
            register_frame, text="Username:", font=("Arial", 12), bg="#f7f7f7")
        username_label.grid(row=4, column=0, pady=5)

        self.entries["username"] = tk.Entry(register_frame, textvariable=self.vars["username"], font=("Arial", 12))
        self.entries["username"].grid(row=4, column=1, padx=(0, 20), pady=5)

        password_label = tk.Label(
            register_frame, text="Update Password:", font=("Arial", 12), bg="#f7f7f7")
        password_label.grid(row=5, column=0, pady=5)

        self.entries["password"] = tk.Entry(
            register_frame, textvariable=self.vars["password"], font=("Arial", 12), show="*")
        self.entries["password"].grid(row=5, column=1, padx=(0, 20), pady=5)

        confirm_password_label = tk.Label(
            register_frame, text="Confirm Password:", font=("Arial", 12), bg="#f7f7f7")
        confirm_password_label.grid(row=6, column=0, pady=5)

        self.entries["password_confirm"] = tk.Entry(
            register_frame, textvariable=self.vars["password_confirm"], font=("Arial", 12), show="*")
        self.entries["password_confirm"].grid(row=6, column=1, padx=(0, 20), pady=5)

        self.error_label = tk.Label(register_frame, font=("Arial", 12), bg="#f7f7f7", fg="#ff0000")
        self.error_label.grid(row=7, column=0, pady=(10, 0))

        update_button = tk.Button(
            register_frame, font=("Arial", 12), width=8, text="Update", command=self.update_customer)
        update_button.grid(row=7, column=1, pady=(10, 0))

        logout_button = tk.Button(
            register_frame, font=("Arial", 12), width=8, text="Log Out", command=self.logout, bg="#ff2e2e")
        logout_button.grid(row=7, column=2, pady=(10, 0))

    @staticmethod
    def validate_field(value: str, entry_widget: tk.Entry) -> bool:
        """
        Validates a field and updates its Entry based on whether it is filled.

        Args:
            value (str): The value to check that isn't empty
            entry_widget (tk.Entry): The tkitner widget that needs updating

        Returns:
            True: If the Entry Widget provided does have a value
            False: If the Entry Widget provided does not have a value
        """
        if not value:
            entry_widget.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            return False
        else:
            entry_widget.config(highlightthickness=0)
            return True

    def update_customer(self) -> None:
        """
        Register a new customer.
        - Username needs to be unique
        - Passwords need to match
        - All fields need to be filled in.
        """
        error = False

        field_entries = [
            (self.vars["first_name"].get(), self.entries["first_name"]),
            (self.vars["last_name"].get(), self.entries["last_name"]),
            (self.vars["email"].get(), self.entries["email"]),
            (self.vars["username"].get(), self.entries["username"]),
        ]

        for value, entry in field_entries:
            if not self.validate_field(value, entry):
                error = True

        password = self.user["Customer_Password"]

        if self.vars["password"].get() and self.vars["password_confirm"].get():
            if self.vars["password"].get() != self.vars["password_confirm"].get():
                self.entries["password"].get().config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.entries["password_confirm"].config(
                    highlightbackground="red", highlightcolor="red", highlightthickness=1)
                self.error_label.configure(text="Passwords do not match!")
                error = True
            else:
                self.error_label.configure(text="")
                self.entries["password"].config(highlightthickness=0)
                self.entries["password_confirm"].config(highlightthickness=0)
                password = self.vars["password"].get()
        elif self.vars["password"].get():
            self.entries["password_confirm"].config(highlightbackground="red", highlightcolor="red",
                                                    highlightthickness=1)
            self.error_label.configure(text="Passwords do not match!")
            error = True
        elif self.vars["password_confirm"].get():
            self.entries["password"].config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            self.error_label.configure(text="Passwords do not match!")
            error = True

        if not error:
            result = self.db.update_customer(
                current_username=self.user["Customer_Username"],
                firstname=self.vars["first_name"].get(),
                surname=self.vars["last_name"].get(),
                gender=self.vars["gender"].get(),
                email=self.vars["email"].get(),
                new_username=self.vars["username"].get(),
                password=password if isinstance(password, str) else None
            )

            if isinstance(result, sqlite3.IntegrityError):
                self.error_label.configure(text="Username is already taken!")
                self.entries["username"].config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            elif isinstance(result, sqlite3.Error):
                print(result)
                self.error_label.configure(text="Database Error!")
            else:
                self.user["Customer_Firstname"] = self.vars["first_name"].get()
                self.user["Customer_Surname"] = self.vars["last_name"].get()
                self.user["Customer_Gender"] = self.vars["gender"].get()
                self.user["Customer_Email"] = self.vars["email"].get()
                self.user["Customer_Username"] = self.vars["username"].get()

                if isinstance(password, bytes):
                    self.user["Password"] = password
                else:
                    self.user["Password"] = hashlib.sha256(password.encode()).digest()

    def logout(self):
        """
        Logout - resets the user information, and return to the login page
        """
        self.user["Customer_Id"] = 0
        self.user["Customer_Firstname"] = ""
        self.user["Customer_Surname"] = ""
        self.user["Customer_Gender"] = ""
        self.user["Customer_Email"] = ""
        self.user["Customer_Username"] = ""
        self.user["Customer_Password"] = ""
        self.navigate_to(self.pages["Login"])
