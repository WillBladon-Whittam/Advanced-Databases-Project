import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np
import re

from advanced_database_project.gui.pages.checkout_page import CheckoutPage
from advanced_database_project.backend.db_connection import DatabaseConnection
from advanced_database_project.gui.base_page import BasePage


class BasketPage(BasePage):
    """
    A tkinter page to display the user's basket.
    Includes a scrollable list of product cards, total price, checkout button,
    and options to remove items or change quantities.
    """

    def __init__(self, pages: Dict[str, BasePage], db: DatabaseConnection, user: Dict[str, Any],
                 basket: Dict[str, Any]):
        super().__init__(pages, db, user, basket)
        self.configure(bg="#f7f7f7")

        self.basket_items = []
        self.orders = []
        self.total_price = 0

        self.orders_var = tk.StringVar()

        self.canvas = None

        self.create_widgets()

    def show(self) -> None:
        """
        Override the default show function from BasePage - requery the database for new items in basket
        """
        self.basket_items = self.db.get_basket_items_by_basket_id(self.basket["Basket_ID"])
        self.orders = self.db.get_orders_by_customer_id(self.user["Customer_ID"])
        self.total_price = self.calculate_total_price()
        self.refresh_page()
        self.update_scroll_region(None, self.canvas)
        self.canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, self.canvas))
        self.canvas.bind("<Configure>", lambda event: self.update_scroll_region(event, self.canvas))
        self.pack()

    def create_widgets(self) -> None:
        """
        Create widgets for the basket page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew")

        header_label = tk.Label(header_frame, text="Your Basket", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333")
        header_label.pack(pady=20)

        product_frame = tk.Frame(self, bg="#f7f7f7")
        product_frame.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        self.canvas = tk.Canvas(product_frame, bg="#f7f7f7", height=400, width=1200, highlightthickness=0)
        scrollbar = tk.Scrollbar(product_frame, orient="vertical", command=self.canvas.yview)
        scrollable_frame = tk.Frame(self.canvas, bg="#f7f7f7")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        for item in self.basket_items:
            self.create_product_card(scrollable_frame, item)

        footer_frame = tk.Frame(self, bg="#f7f7f7")
        footer_frame.grid(row=3, column=0, pady=20, padx=10, sticky="se")

        total_label = tk.Label(
            footer_frame, text=f"Total: ${self.total_price:.2f}", font=("Arial", 20, "bold"), bg="#f7f7f7", fg="#333", )
        total_label.pack(side="left", padx=20)

        checkout_button = tk.Button(
            footer_frame, text="Checkout", font=("Arial", 14), bg="#007bff", fg="#fff",
            activebackground="#0056b3", activeforeground="#fff", command=self.checkout)
        checkout_button.pack(side="right")

        orders_frame = tk.Frame(self, bg="#f7f7f7")
        orders_frame.grid(row=3, column=0, pady=20, padx=10, sticky="sw")

        orders_button = tk.Button(
            orders_frame, text="Track Order", font=("Arial", 14), bg="#007bff", fg="#fff",
            activebackground="#0056b3", activeforeground="#fff", command=self.track_order)
        orders_button.pack(side="left", padx=5)

        selected_orders_dropdown = ttk.Combobox(
            orders_frame, font=("Arial", 10), textvariable=self.orders_var, width=40,
            values=[f"Order ID {order["Order_ID"]} - {order["Order_Quantity"]} {order["Product_Name"]}" for order in self.orders],
            state="readonly")
        selected_orders_dropdown.pack(side="left", padx=5)

    def create_product_card(self, parent: tk.Frame, item: Dict[str, Any]) -> None:
        """
        Create a product card for an item in the basket.

        Args:
            parent (tk.Frame): The parent frame the product card belongs to
            item (Dict[str, Any]): The product information from the database
        """
        product_card = tk.Frame(parent, bg="#fff", bd=1, relief="solid", padx=10, pady=10, width=100)
        product_card.pack(fill="x", pady=5, padx=10)

        product_card.columnconfigure(0, weight=1)
        product_card.columnconfigure(1, weight=0)
        product_card.columnconfigure(2, weight=0)
        product_card.columnconfigure(3, weight=0)

        if item["Product_Image"] is not None:
            image = Image.open(io.BytesIO(item["Product_Image"]))
            image.thumbnail((150, 150), Image.LANCZOS)

            ph = ImageTk.PhotoImage(image)

            product_image = tk.Canvas(
                product_card, width=162, height=162, bg="#fff", bd=0, highlightthickness=0)

            x_offset = (162 - image.width) // 2
            y_offset = (162 - image.height) // 2

            product_image.create_image(x_offset, y_offset, anchor="nw", image=ph)

            product_image.image = ph
            product_image.grid(row=0, column=0, sticky="w", padx=(10, 0))

        product_name = tk.Label(
            product_card, text=item["Product_Name"], font=("Arial", 14, "bold"), bg="#fff", fg="#333")
        product_name.grid(row=0, column=1, sticky="w", padx=(10, 0))

        product_price = tk.Label(
            product_card, text=f"${item["Price"]:.2f}", font=("Arial", 14), bg="#fff", fg="#007bff")
        product_price.grid(row=0, column=2, sticky="e", padx=(10, 20))

        quantity_label = tk.Label(product_card, text="Quantity:", font=("Arial", 12), bg="#fff", fg="#333")
        quantity_label.grid(row=0, column=3, sticky="e", padx=(10, 5))

        quantity_spinbox = tk.Spinbox(product_card, from_=0, to=9999, width=5, font=("Arial", 12), justify="center")
        quantity_spinbox.config(
            command=lambda item=item, spinbox=quantity_spinbox: self.update_quantity(item, spinbox)
        )
        quantity_spinbox.delete(0, "end")
        quantity_spinbox.insert(0, item["Quantity"])
        quantity_spinbox.grid(row=0, column=4, sticky="e", padx=(5, 20))

        # Remove Button
        remove_button = tk.Button(
            product_card, text="Remove", font=("Arial", 12), bg="#ff4d4d", fg="#fff",
            command=lambda item=item: self.remove_item(item))
        remove_button.grid(row=0, column=5, padx=(20, 10), pady=5)

        self.total_price = self.calculate_total_price()

        self.canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, self.canvas))
        self.canvas.bind("<Configure>", lambda event: self.update_scroll_region(event, self.canvas))

    def calculate_total_price(self) -> int:
        """
        Calculate the total price of the basket.

        Returns:
            int: Total price of the basket
        """
        total_price = self.db.get_customer_basket_value(self.basket["Basket_ID"])
        if total_price is None:
            return 0
        return total_price["Total_Basket_Value"]

    def update_quantity(self, item: Dict[str, Any], spinbox: tk.Spinbox) -> None:
        """
        Update the quantity of an item in the basket.

        Args:
            item (Dict[str, Any]): The product information that has had the quantity updated
            spinbox (tk.Spinbox): The spinbox of that product
        """
        if int(spinbox.get()) == 0:
            self.remove_item(item)
            return
        self.db.update_basket_item(self.basket["Basket_ID"], item["Product_ID"],
                                   int(spinbox.get()))  # Update in the database
        self.basket_items = self.db.get_basket_items_by_basket_id(self.basket["Basket_ID"])
        self.total_price = self.calculate_total_price()
        self.refresh_page()

    def remove_item(self, item: Dict[str, Any]) -> None:
        """
        Remove an item from the basket.

        Args:
            item (Dict[str, Any]): The product information of the item that was removed
        """
        self.db.remove_basket_item(self.basket["Basket_ID"], item["Product_ID"])6a
        self.basket_items = self.db.get_basket_items_by_basket_id(self.basket["Basket_ID"])
        self.total_price = self.calculate_total_price()
        self.refresh_page()

    def checkout(self):
        """
        Handle the checkout process.
        """
        if self.basket_items:
            self.pages["Checkout"] = CheckoutPage(self.pages, self.db, self.user, self.basket)
            self.navigate_to(self.pages["Checkout"])

    def track_order(self):
        if self.orders_var.get():
            selected_order_id = int(re.search(r"Order ID (\d+)", self.orders_var.get()).group(1))
            selected_order = self.db.get_order_by_order_id(selected_order_id)

            stages = {
                "Ordered": 0,
                "Dispatched": 1,
                "Out for delivery": 2,
                "Delivered": 3
            }

            completed_until = stages[selected_order["Order_Status"]]
            completion_status = [1 if i <= completed_until else 0 for i in range(len(stages))]

            x_positions = np.arange(len(stages))

            plt.figure(figsize=(10, 4))
            plt.bar(
                x_positions,
                [1] * len(stages),
                color=['green' if status else 'lightgray' for status in completion_status],
                edgecolor='black',
                width=0.6
            )

            for i, stage in enumerate(stages):
                color = 'white' if completion_status[i] else 'black'
                plt.text(i, 0.5, stage, ha='center', va='center', color=color, fontsize=10)

            plt.scatter([x_positions[completed_until]], [1.2], color='red', zorder=5, label="Current Stage")
            plt.text(x_positions[completed_until], 1.4, selected_order["Order_Status"], ha='center', color='red', fontsize=12)

            plt.text(x_positions[0], -0.4, f"Time: {selected_order["Order_Date"]}", ha='center', color='blue', fontsize=10)

            plt.xticks(x_positions, [])
            plt.yticks([])
            plt.title(f"Order Tracking Timeline - Order ID {selected_order_id}", fontsize=14, pad=20)
            plt.ylim(-0.6, 2)
            plt.axhline(y=0, color='black', linewidth=0.8)  # Baseline
            plt.legend(loc='upper left', fontsize=10)

            plt.tight_layout()
            plt.show()