import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
from datetime import datetime
from typing import List, Dict, Any

from advanced_database_project.backend.db_connection import DatabaseConnection
from advanced_database_project.gui.base_page import BasePage


class ProductInfoPage(BasePage):
    """
    A tkinter page to display detailed product information.
    Includes name, price, suppliers, reviews, and an add-to-basket button.
    """

    def __init__(self, pages: Dict[str, BasePage], db: DatabaseConnection, user: Dict[str, Any],
                 basket: Dict[str, Any], product: Dict[str, Any]):
        super().__init__(pages, db, user, basket)
        self.configure(bg="#f7f7f7")

        self.product = product
        self.canvas = None
        self.review_text = None

        self.rating = None
        self.stars = []

        self.quantity = tk.StringVar(value="1")

        self.result_label = None

        self.create_widgets()

    def show(self) -> None:
        """
        Override the default show function from BasePage - rebind the scrollwheel to the scrollable canvas
        """
        self.product = self.db.select_products(self.product["Product_Name"])[0]
        self.stars = []
        self.refresh_page()
        self.update_scroll_region(None, self.canvas)
        self.canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, self.canvas))
        self.canvas.bind("<Configure>", lambda event: self.update_scroll_region(event, self.canvas))
        self.pack()

    def navigate_to(self, page: BasePage) -> None:
        """
        Override the default show function from BasePage - unbind the scrollwheel to the scrollable canvas
        """
        self.rating = None
        self.pack_forget()
        page.show()

    def create_widgets(self) -> None:
        """
        Create widgets for the product information page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew")

        product_name_frame = tk.Frame(header_frame, bg="#e6e6e6", pady=20)
        product_name_frame.pack(fill="x")
        product_name_label = tk.Label(
            product_name_frame, text=self.product["Product_Name"], font=("Arial", 24, "bold"),
            bg="#e6e6e6", fg="#333", width=50, )
        product_name_label.pack()

        product_frame = tk.Frame(self, bg="#f7f7f7")
        product_frame.grid(row=2, column=0, pady=(10, 0), sticky="w")

        if self.product["Product_Image"] is not None:
            image = Image.open(io.BytesIO(self.product["Product_Image"]))
            image.thumbnail((320, 320), Image.LANCZOS)

            ph = ImageTk.PhotoImage(image)

            product_image = tk.Canvas(product_frame, width=320, height=320, bg="#fff", bd=0, highlightthickness=0)

            x_offset = (320 - image.width) // 2
            y_offset = (320 - image.height) // 2

            product_image.create_image(x_offset, y_offset, anchor="nw", image=ph)

            product_image.image = ph
            product_image.grid(row=0, column=0, padx=20, sticky="nw")

        stock_label = tk.Label(
            product_frame, text=f"Available Stock: {self.product["Stock_Level"]}", font=("Arial", 20), bg="#f7f7f7")
        stock_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="w")

        price_label = tk.Label(
            product_frame, text=f"Price: ${self.product["Price"]:.2f}", font=("Arial", 20), bg="#f7f7f7", fg="#007bff")
        price_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        details_frame = tk.Frame(product_frame, bg="#f7f7f7")
        details_frame.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="nw")

        product_name_label = tk.Label(
            details_frame, text=self.product["Product_Name"], font=("Arial", 24), bg="#f7f7f7", fg="#555")
        product_name_label.pack(anchor="w", pady=5)

        category_label = tk.Label(details_frame,
                                  text=f"Category: {self.db.select_categories_by_id(self.product["Category_ID"])["Category_Name"]}",
                                  font=("Arial", 20), bg="#f7f7f7", fg="#555")
        category_label.pack(anchor="w")

        suppliers_label = tk.Label(
            details_frame, text=f"Suppliers:", font=("Arial", 20), bg="#f7f7f7", fg="#555")
        suppliers_label.pack(anchor="w", pady=5)

        for key, value in self.db.select_suppliers_by_id(self.product["Supplier_ID"]).items():
            if key == "Supplier_ID":
                continue
            suppliers_info_label = tk.Label(details_frame, text=value, font=("Arial", 16), bg="#f7f7f7", fg="#555")
            suppliers_info_label.pack(anchor="w")

        reviews_frame = tk.Frame(product_frame, bg="#f7f7f7", width=500)
        reviews_frame.grid(row=0, column=2, pady=(5, 0), padx=(10, 0), sticky="ne")

        self.canvas = tk.Canvas(reviews_frame, bg="#f7f7f7", height=320, width=500)
        scrollbar = tk.Scrollbar(reviews_frame, orient="vertical", command=self.canvas.yview)

        scrollable_frame = tk.Frame(self.canvas, bg="#f7f7f7")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        reviews_label = tk.Label(
            scrollable_frame, text=f"Customer Reviews:", font=("Arial", 20), bg="#f7f7f7", fg="#555")
        reviews_label.pack(anchor="nw", pady=(5, 0))

        for review in self.db.select_reviews_by_product_id(self.product["Product_ID"]):
            for key, value in review.items():
                if key == "Customer_ID":
                    customer = self.db.select_customer_by_id(value)
                    review_info_label = tk.Label(
                        scrollable_frame, text=customer["Customer_Firstname"] + " " + customer["Customer_Surname"],
                        font=("Arial", 16, "underline"), bg="#f7f7f7", fg="#555")
                    review_info_label.pack(anchor="nw")
                elif key == "Product_ID":
                    continue
                elif key == "Review_Stars":
                    stars = ""
                    for _ in range(int(value)):
                        stars += "\u2606"
                    review_info_label = tk.Label(scrollable_frame, text=stars,
                                                 font=("Arial", 16), bg="#f7f7f7", fg="#555")
                    review_info_label.pack(anchor="nw")
                elif key == "Review_Comment":
                    if value:
                        review_info_label = tk.Label(scrollable_frame, text=value,
                                                     font=("Arial", 16), bg="#f7f7f7", fg="#555")
                        review_info_label.pack(anchor="nw")
                elif key == "Review_Date":
                    review_info_label = tk.Label(scrollable_frame, text=value + "\n",
                                                 font=("Arial", 14), bg="#f7f7f7", fg="#555")
                    review_info_label.pack(anchor="nw")

        leave_review_frame = tk.Frame(product_frame, bg="#f7f7f7")
        leave_review_frame.grid(row=1, column=2, pady=10, sticky="w")

        self.review_text = tk.Text(leave_review_frame, font=("Arial", 12), width=30, height=5, wrap="word")
        self.review_text.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")

        for i in range(5):
            star = tk.Label(
                leave_review_frame, text="\u2606", font=("Arial", 24), bg="#f7f7f7", fg="#555", cursor="hand2")
            star.grid(row=0, column=1 + i, padx=5, sticky="n")
            star.bind("<Button-1>", lambda event, r=i + 1: self.update_rating(r))
            self.stars.append(star)

        leave_review_button = tk.Button(
            leave_review_frame, text="Leave a Review", font=("Arial", 14), bg="#30d424", fg="#fff",
            command=self.leave_review)
        leave_review_button.grid(row=1, column=0, padx=(10, 0), sticky="nw")

        basket_frame = tk.Frame(product_frame, bg="#f7f7f7", width=50)
        basket_frame.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

        add_to_basket_btn = tk.Button(
            basket_frame, text="Add to Basket", font=("Arial", 14), bg="#007bff", fg="#fff",
            activebackground="#0056b3", activeforeground="#fff", command=self.add_to_basket)
        add_to_basket_btn.grid(row=0, column=0, sticky="w")

        quantity_spinbox = tk.Spinbox(
            basket_frame, from_=1, to=9999, width=5, font=("Arial", 14), textvariable=self.quantity)
        quantity_spinbox.delete(0, "end")
        quantity_spinbox.insert(0, 1)
        quantity_spinbox.grid(row=0, column=1, padx=10, sticky="w")

        self.result_label = tk.Label(product_frame, text="", font=("Arial", 14), bg="#f7f7f7", fg="#ff0000", width=20)
        self.result_label.grid(row=1, column=1, pady=20, sticky="sw")

        back_button = tk.Button(
            product_frame, text="Return", font=("Arial", 14), bg="#f7f7f7",
            command=lambda: self.navigate_to(self.pages["Products"]))
        back_button.grid(row=1, column=3, pady=10, padx=5, sticky="sw")

        self.canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, self.canvas))
        self.canvas.bind("<Configure>", lambda event: self.update_scroll_region(event, self.canvas))

    def update_rating(self, new_rating: int) -> None:
        """
        Update the rating by changing the colour of the stars

        Args:
            new_rating: The new rating selected (1-5)
        """
        self.rating = new_rating
        for i in range(5):
            if i < self.rating:
                self.stars[i].config(text="\u2605", fg="gold")  # Filled star
            else:
                self.stars[i].config(text="\u2606", fg="gray")  # Empty star

    def leave_review(self) -> None:
        """
        A Customer leaves a review on a product.
        Validate that the stars have been selected.
        """
        if self.rating is None:
            for star in self.stars:
                star.configure(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            return
        self.db.add_review(self.user["Customer_ID"], self.product["Product_ID"], self.rating,
                           self.review_text.get("1.0", "end-1c"), datetime.now().strftime("%d/%m/%Y"))
        self.stars = []
        self.refresh_page()
        self.rating = None

    def add_to_basket(self) -> None:
        """
        Add an item to a basket
        """
        result = self.db.add_item_to_basket(
            self.basket["Basket_ID"], self.product["Product_ID"], int(self.quantity.get()))
        if isinstance(result, sqlite3.IntegrityError):
            self.result_label.configure(text="Not enough stock!", fg="#555")
        else:
            self.result_label.configure(text="Added to basket!", fg="#1aff00")
