import tkinter as tk
from tkinter import ttk
from typing import List, Dict
from PIL import ImageTk, Image
import io

from advanced_database_project.backend.db_connection import DatabaseConnection
from advanced_database_project.gui.base_page import BasePage


class ProductsPage(BasePage):
    """
    GUI Product Page

    Displays all the products avaliable
    Allows searching of products by name, category and price.
    ALlows sorting of products by name, price.
    """

    def __init__(self, pages: List[tk.Frame], db: DatabaseConnection, user: Dict[str, str]):
        super().__init__(pages, db, user)
        self.configure(bg="#f7f7f7")

        self.products = self.db.selectProducts()
        self.categories = ["All Categories"] + [category[1]
                                                for category in self.db.selectCategories()]

        # Initialise product search information variables
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.min_price_var = tk.DoubleVar(value=0)
        self.max_price_var = tk.DoubleVar(value=5000)
        self.sort_criteria = tk.StringVar(value="Name")
        self.sort_order = tk.StringVar(value="ASC")
        
        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the products page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0)

        title = tk.Label(header_frame, text="Product Listings",
                         font=("Arial", 24, "bold"), bg="#f7f7f7")
        title.pack(pady=5)

        search_frame = tk.Frame(self, bg="#f7f7f7")
        search_frame.grid(row=2, column=0)

        search_label = tk.Label(
            search_frame, text="Search Name:", font=("Arial", 12), bg="#f7f7f7")
        search_label.grid(row=2, column=0, pady=5)

        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, font=("Arial", 12))
        search_entry.grid(row=2, column=1, padx=(0, 20), pady=5)
        self.search_var.trace_add('write', self.update_products)

        category_label = tk.Label(
            search_frame, text="Filter Category:", font=("Arial", 12), bg="#f7f7f7")
        category_label.grid(row=2, column=2, pady=5)

        category_dropdown = ttk.Combobox(
            search_frame, textvariable=self.category_var, values=self.categories, state="readonly", font=("Arial", 12))
        category_dropdown.grid(row=2, column=3, padx=(0, 20), pady=5)
        self.category_var.trace_add('write', self.update_products)

        price_label = tk.Label(
            search_frame, text="Price Range ($):", font=("Arial", 12), bg="#f7f7f7")
        price_label.grid(row=2, column=4, pady=5)

        min_price_entry = tk.Entry(
            search_frame, textvariable=self.min_price_var, font=("Arial", 12), width=10)
        min_price_entry.grid(row=2, column=5, padx=(0, 10), pady=5)
        self.min_price_var.trace_add('write', self.update_products)

        max_price_entry = tk.Entry(
            search_frame, textvariable=self.max_price_var, font=("Arial", 12), width=10)
        max_price_entry.grid(row=2, column=6, padx=(0, 20), pady=5)
        self.max_price_var.trace_add('write', self.update_products)

        sort_frame = tk.Frame(search_frame, bg="#f7f7f7")
        sort_frame.grid(row=2, column=8, pady=5)

        sort_label = tk.Label(sort_frame, text="Sort by:",
                              font=("Arial", 12), bg="#f7f7f7")
        sort_label.grid(row=2, column=0, padx=(0, 10))

        sort_criteria_button = tk.Button(sort_frame, textvariable=self.sort_criteria, font=(
            "Arial", 12), command=self.toggle_sort_criteria, width=8)
        sort_criteria_button.grid(row=2, column=1, padx=(0, 10))

        sort_order_button = tk.Button(
            sort_frame,
            textvariable=self.sort_order,
            font=("Arial", 10),
            command=self.toggle_sort_order,
            width=4
        )
        sort_order_button.grid(row=2, column=2)

        product_list_frame = tk.Frame(self, bg="#f7f7f7")
        product_list_frame.grid(row=3, column=0, sticky="nsew")

        canvas = tk.Canvas(product_list_frame, bg="#f7f7f7", height=500)
        canvas.grid(row=3, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(
            product_list_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        self.products_frame = tk.Frame(canvas, bg="#f7f7f7")
        canvas.create_window((0, 0), window=self.products_frame, anchor="nw")

        canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

        self.display_products(self.products_frame)

        product_list_frame.grid_rowconfigure(0, weight=1)
        product_list_frame.grid_columnconfigure(0, weight=1)

        canvas.bind("<Configure>", lambda event: self.update_scroll_region(event, canvas))

    def scroll_canvas(self, event, canvas):
        """
        Scroll the canvas with the mouse wheel.
        """
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def update_scroll_region(self, event, canvas):
        """
        Update the scroll region of the canvas. Stops the canvas from scolling forever.
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    def display_products(self, parent):
        """
        Display products as a grid, with 6 in a column.
        """
        for widget in parent.winfo_children():
            widget.destroy()

        for i, product in enumerate(self.products):
            product_frame = tk.Frame(
                parent, bg="#fff", bd=1, relief="solid", padx=10, pady=10, width=200,
            )
            product_frame.grid(row=i // 6, column=i %
                               6, padx=10, pady=10, sticky="nsew")

            # Placeholder for product image
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
                
            print(product[1], len(product[1]))
            if len(product[1]) >= 18:
                name = "\n".join(product[1].split(" "))
            else:
                name = product[1]
            product_name = tk.Label(product_frame, text=name, font=(
                "Arial", 12, "bold"), bg="#fff", fg="#333", width=15)
            product_name.pack(pady=(10, 5))

            product_price = tk.Label(product_frame, text=f"${product[3]:.2f}", font=(
                "Arial", 12), bg="#fff", fg="#007bff")
            product_price.pack()

    def update_products(self, a, b, c):
        """
        Update the products listed - this is called when filtering or sorting products to update the products

        Params a, b and c are the trace parameters that are unused.
        """
        category_var = self.category_var.get().lower()
        if category_var == "all categories":
            category_var = ""

        try:
            min_price_var = float(self.min_price_var.get()) if self.min_price_var.get() else 0
        except tk.TclError:
            min_price_var = 0

        try:
            max_price_var = float(self.max_price_var.get()) if self.max_price_var.get() else 0
        except tk.TclError:
            max_price_var = 5000

        self.products = self.db.selectProducts(filter_name=self.search_var.get().lower(),
                                               filter_category=category_var,
                                               filter_price=(min_price_var, max_price_var),
                                               sort_by=self.sort_criteria.get(),
                                               sort_order=self.sort_order.get())
        self.display_products(self.products_frame)

    def toggle_sort_criteria(self):
        """
        Cycle through the sorting criteria (Name, Category, Price).
        """
        current = self.sort_criteria.get()
        criteria = ["Name", "Category", "Price"]
        next_index = (criteria.index(current) + 1) % len(criteria)
        self.sort_criteria.set(criteria[next_index])
        self.update_products(None, None, None)  # Update the product display

    def toggle_sort_order(self):
        """
        Toggle the sorting order (ASC/DESC).
        """
        current = self.sort_order.get()
        self.sort_order.set("DESC" if current == "ASC" else "ASC")
        self.update_products(None, None, None)  # Update the product display
