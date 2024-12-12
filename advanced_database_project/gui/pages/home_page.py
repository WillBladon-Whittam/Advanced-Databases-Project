import tkinter as tk
from typing import List, Dict
from PIL import ImageTk, Image
import io

from advanced_database_project.backend.db_connection import DatabaseConnection
from advanced_database_project.gui.base_page import BasePage


class HomePage(BasePage):
    """
    GUI Home Page - displayed when the application is first opened.
    """
    
    def __init__(self, pages: List[tk.Frame], db: DatabaseConnection, user: Dict[str, str]):
        super().__init__(pages, db, user)
        self.configure(bg="#f7f7f7")
        
        self.top_products = self.db.selectBestSellingProducts()

        self.create_welcome()
        self.create_featured_products()

    def create_welcome(self):
        """
        Create a Welcome Message with a Shop Now button
        """
        content = tk.Frame(self, bg="#f7f7f7")
        content.grid(row=1, column=0, sticky="nsew") 
        
        welcome = tk.Frame(content, bg="#e6e6e6", pady=20)
        welcome.pack(fill="x")
        welcome_label = tk.Label(
            welcome,
            text="Welcome to the Online Hardware Store!",
            font=("Arial", 24, "bold"),
            bg="#e6e6e6",
            fg="#333"
        )
        welcome_label.pack(pady=(30, 10))
        
        shop_now_button = tk.Button(
            welcome,
            text="Shop Now",
            font=("Arial", 14),
            bg="#007bff",
            fg="#fff",
            activebackground="#0056b3",
            activeforeground="#fff",
            bd=0,
            padx=20,
            pady=10,
            command=lambda: self.navigate_to(self.pages["Products"]),
        )
        shop_now_button.pack()
        
    def create_featured_products(self):
        """
        Create Top Selling Products.
        These will be the highest sellers from the orders
        """
        content = tk.Frame(self, bg="#f7f7f7")
        content.grid(row=2, column=0, sticky="nsew") 

        featured_label = tk.Label(
            content,
            text="Top Selling Products",
            font=("Arial", 20, "bold"),
            bg="#f7f7f7",
            fg="#333",
        )
        featured_label.pack(pady=(10, 10))

        featured_frame = tk.Frame(content, bg="#f7f7f7")
        featured_frame.pack(fill="both")

        for i, product in enumerate(self.top_products):
            self.create_product_card(featured_frame, product, row=1, col=i + 1)

        return content


    def create_product_card(self, parent, product, row, col):
        """
        Create a single product card and place it in the grid.
        """
        product_frame = tk.Frame(
            parent, bg="#fff", bd=1, relief="solid", padx=10, pady=10
        )
        product_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        if product[6] is not None:
            image = Image.open(io.BytesIO(product[6]))

            image.thumbnail((150, 150), Image.LANCZOS)

            ph = ImageTk.PhotoImage(image)

            product_image = tk.Canvas(
                product_frame, width=162, height=162, bg="#fff", bd=0, highlightthickness=0)

            x_offset = (162 - image.width) // 2
            y_offset = (162 - image.height) // 2

            product_image.create_image(x_offset, y_offset, anchor="nw", image=ph)

            product_image.image = ph
            product_image.pack()

        if len(product[1]) >= 18:
            name = "\n".join(product[1].split(" "))
        else:
            name = product[1]
        product_name = tk.Label(product_frame, text=name, font=("Arial", 12, "bold"), bg="#fff", fg="#333", width=13)
        product_name.pack(pady=(10, 5))

        product_price = tk.Label(product_frame, text=f"${product[3]:.2f}", font=("Arial", 12), bg="#fff", fg="#007bff")
        product_price.pack()
