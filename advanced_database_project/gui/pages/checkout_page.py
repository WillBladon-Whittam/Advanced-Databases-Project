import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple

from advanced_database_project.gui.base_page import BasePage
from advanced_database_project.backend.db_connection import DatabaseConnection


class CheckoutPage(BasePage):
    """
    GUI Checkout Page - Displayed information about the customer, allows customers to edit there information and logout
    """

    def __init__(self, pages: Dict[str, BasePage], db: DatabaseConnection, user: Dict[str, Any],
                 basket: Dict[str, Any]):
        super().__init__(pages, db, user, basket)
        self.configure(bg="#f7f7f7")

        # Initialise account information variables
        self.vars = {
            # Billing
            "billing_address_street_number": tk.StringVar(),
            "billing_address_street": tk.StringVar(),
            "billing_address_postcode": tk.StringVar(),
            "card_number": tk.StringVar(),
            "card_expiry": tk.StringVar(),
            "name_on_card": tk.StringVar(),
            "cvc": tk.StringVar(),
            # Shipping
            "shipping_address_street_number": tk.StringVar(),
            "shipping_address_street": tk.StringVar(),
            "shipping_address_postcode": tk.StringVar(),
        }

        self.entries = {}

        self.error_label = None

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create widgets for the checkout page.
        """

        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew")

        header_label = tk.Label(header_frame, text="Checkout Page", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333")
        header_label.pack(pady=20)

        form_frame = tk.Frame(header_frame, bg="#f7f7f7")
        form_frame.pack(padx=20, pady=10)

        # Create form sections
        self.create_section(form_frame, "Billing Information", 0, [
            ("Street Number:", "billing_address_street_number"),
            ("Street:", "billing_address_street"),
            ("Postcode:", "billing_address_postcode"),
        ])
        self.create_section(form_frame, "Payment Information", 1, [
            ("Card Number:", "card_number"),
            ("Card Expiry Date (MM/YY):", "card_expiry"),
            ("Name on Card:", "name_on_card"),
            ("CVC:", "cvc"),
        ])
        self.create_section(form_frame, "Shipping Information", 2, [
            ("Street Number:", "shipping_address_street_number"),
            ("Street:", "shipping_address_street"),
            ("Postcode:", "shipping_address_postcode"),
        ])

        # Navigation buttons
        buttons_frame = tk.Frame(header_frame, bg="#f7f7f7")
        buttons_frame.pack(pady=20)

        back_button = tk.Button(
            buttons_frame, text="Back to Basket", font=("Arial", 12),
            command=self.back_to_basket, bg="#ff4d4d", fg="#fff")
        back_button.pack(side="left", padx=10)

        place_order_button = tk.Button(
            buttons_frame, text="Place Order", font=("Arial", 12), command=self.place_order, bg="#4caf50", fg="#fff")
        place_order_button.pack(side="right", padx=10)

        self.error_label = tk.Label(header_frame, text="", font=("Arial", 12), bg="#f7f7f7", fg="#ff0000")
        self.error_label.pack(pady=10)

    def create_section(self, parent: tk.Frame, section_title: str, row: int, fields: List[Tuple[str, str]]):
        """
        Create a labeled section with entry fields.

        Args:
            parent (tk.Frame): The parent frame.
            section_title (str): Title of the section.
            row (int): Row position to place the section.
            fields (List[Tuple[str, str]]): List of tuple, first tuple is the label of the text,
                                            the second is the key for the vars list
        """
        section_frame = tk.LabelFrame(parent, text=section_title, font=("Arial", 14, "bold"), bg="#f7f7f7")
        section_frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        section_frame.columnconfigure(1, weight=1)

        for idx, (label_text, vars_key) in enumerate(fields):
            label = tk.Label(section_frame, text=label_text, font=("Arial", 12), bg="#f7f7f7")
            label.grid(row=idx, column=0, sticky="w", padx=5, pady=5)

            entry = tk.Entry(section_frame, textvariable=self.vars[vars_key], font=("Arial", 12))
            entry.grid(row=idx, column=1, sticky="ew", padx=5, pady=5)
            self.entries[vars_key] = entry

    def back_to_basket(self) -> None:
        """
        Navigate back to the basket page.
        """
        self.navigate_to(self.pages["Cart"])

    def place_order(self) -> None:
        """
        Validate and process the order.
        """

        error = False
        for value, entry in zip(self.vars.values(), self.entries.values()):
            if not self.validate_field(value.get(), entry):
                entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=1)
                error = True
            else:
                entry.config(highlightthickness=0)

        if error:
            return

        self.db.create_shipping(
            self.user["Customer_ID"], self.vars["shipping_address_street_number"].get(),
            self.vars["shipping_address_street"].get(), self.vars["shipping_address_postcode"].get(),
            (datetime.now() + timedelta(3)).strftime("%d/%m/%Y"))
        shipping_id = self.db.cursor.lastrowid

        self.db.create_billing(
            self.user["Customer_ID"], self.vars["billing_address_street_number"].get(),
            self.vars["billing_address_street"].get(), self.vars["billing_address_postcode"].get(),
            self.vars["card_number"].get(), self.vars["card_expiry"].get(), self.vars["name_on_card"].get(),
            self.vars["cvc"].get())
        billing_id = self.db.cursor.lastrowid

        for product in self.db.get_basket_items_by_basket_id(self.basket["Basket_ID"]):
            self.db.place_order(datetime.now().strftime("%d/%m/%Y"), self.user["Customer_ID"],
                                int(product["Product_ID"]), shipping_id, billing_id, int(product["Quantity"]),
                                "Ordered")

        self.db.clear_basket(self.basket["Basket_ID"])
        self.clear_fields()

        self.navigate_to(self.pages["Home"])
        tk.messagebox.showinfo("Success", f"Your order has been placed!")

    def clear_fields(self) -> None:
        """
        Clear all form fields
        """
        for var in self.vars.values():
            var.set("")
