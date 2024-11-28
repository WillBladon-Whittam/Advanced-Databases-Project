import tkinter as tk

from tkinter import ttk

from advanced_database_project.gui.base_page import BasePage


class ProductsPage(BasePage):
    """
    GUI Product Page
    
    Displays all the products avaliable
    Allows searching of products by name, category and price.
    ALlows sorting of products by name, price.
    """
    
    def __init__(self, pages):
        super().__init__(pages)
        self.configure(bg="#f7f7f7")

        self.products = [
            {"name": "GPU", "price": 1499.99, "category": "Electronics"},
            {"name": "Laptop", "price": 2199.49, "category": "Electronics"},
            {"name": "Mouse", "price": 50.99, "category": "Accessories"},
            {"name": "Keyboard", "price": 12.99, "category": "Accessories"},
            {"name": "Monitor", "price": 299.99, "category": "Electronics"},
            {"name": "Motherboard", "price": 249.99, "category": "Electronics"},
            {"name": "RAM (16GB)", "price": 89.99, "category": "Electronics"},
            {"name": "Power Supply (650W)", "price": 79.99, "category": "Electronics"},
            {"name": "SSD (1TB)", "price": 119.99, "category": "Electronics"},
            {"name": "HDD (2TB)", "price": 69.99, "category": "Electronics"},
            {"name": "Cooling Fan", "price": 24.99, "category": "Accessories"},
            {"name": "CPU", "price": 329.99, "category": "Electronics"},
            {"name": "PC Case", "price": 99.99, "category": "Accessories"},
            {"name": "External Hard Drive", "price": 149.99, "category": "Accessories"},
            {"name": "Webcam", "price": 49.99, "category": "Accessories"},
            {"name": "Headset", "price": 79.99, "category": "Accessories"},
            {"name": "Ethernet Cable", "price": 10.99, "category": "Accessories"},
            {"name": "Graphics Tablet", "price": 199.99, "category": "Accessories"},
            {"name": "Wi-Fi Adapter", "price": 29.99, "category": "Electronics"},
            {"name": "UPS (Uninterruptible Power Supply)", "price": 129.99, "category": "Electronics"},
            {"name": "Docking Station", "price": 149.99, "category": "Accessories"},
            {"name": "Microphone", "price": 89.99, "category": "Accessories"},
            {"name": "Router", "price": 139.99, "category": "Electronics"},
            {"name": "Bluetooth Adapter", "price": 19.99, "category": "Accessories"},
            {"name": "Thermal Paste", "price": 6.99, "category": "Accessories"},
            {"name": "Surge Protector", "price": 29.99, "category": "Accessories"},
            {"name": "HDMI Cable", "price": 14.99, "category": "Accessories"},
            {"name": "Game Controller", "price": 59.99, "category": "Accessories"},
            {"name": "Capture Card", "price": 189.99, "category": "Electronics"},
            {"name": "Sound Card", "price": 99.99, "category": "Electronics"},
            {"name": "NAS (Network Attached Storage)", "price": 499.99, "category": "Electronics"},
            {"name": "VR Headset", "price": 399.99, "category": "Electronics"},
            {"name": "Fan Controller", "price": 34.99, "category": "Accessories"},
            {"name": "Card Reader", "price": 19.99, "category": "Accessories"},
            {"name": "Optical Drive", "price": 59.99, "category": "Accessories"},
            {"name": "VRAM Cooling Kit", "price": 39.99, "category": "Accessories"},
            {"name": "Laptop Cooling Pad", "price": 49.99, "category": "Accessories"},
            {"name": "RGB LED Strip", "price": 19.99, "category": "Accessories"},
        ]
        
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All Categories")
        self.min_price_var = tk.DoubleVar(value=0)
        self.max_price_var = tk.DoubleVar(value=5000)

        self.create_widgets()

    def create_widgets(self):
        # Product Listings Header
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0)

        title = tk.Label(header_frame, text="Product Listings", font=("Arial", 24, "bold"), bg="#f7f7f7")
        title.pack(pady=5)

        # Search bar, category dropdown, and price filter
        search_frame = tk.Frame(self, bg="#f7f7f7")
        search_frame.grid(row=2, column=0)

        search_label = tk.Label(search_frame, text="Search Name:", font=("Arial", 12), bg="#f7f7f7")
        search_label.grid(row=2, column=0, padx=(20, 10), pady=5)

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12))
        search_entry.grid(row=2, column=1, padx=(0, 20), pady=5)

        category_label = tk.Label(search_frame, text="Filter Category:", font=("Arial", 12), bg="#f7f7f7")
        category_label.grid(row=2, column=2, padx=(20, 10), pady=5)

        category_dropdown = ttk.Combobox(search_frame, textvariable=self.category_var, values=["All Categories", "Electronics", "Accessories", "Tools", "Furniture"], state="readonly", font=("Arial", 12))
        category_dropdown.grid(row=2, column=3, padx=(0, 20), pady=5)

        price_label = tk.Label(search_frame, text="Price Range ($):", font=("Arial", 12), bg="#f7f7f7")
        price_label.grid(row=2, column=4, padx=(20, 10), pady=5)

        min_price_entry = tk.Entry(search_frame, textvariable=self.min_price_var, font=("Arial", 12), width=10)
        min_price_entry.grid(row=2, column=5, padx=(0, 10), pady=5)

        max_price_entry = tk.Entry(search_frame, textvariable=self.max_price_var, font=("Arial", 12), width=10)
        max_price_entry.grid(row=2, column=6, padx=(0, 20), pady=5)

        # Sort button
        sort_button = tk.Button(search_frame, text="Sort Products", font=("Arial", 12))
        sort_button.grid(row=2, column=7, padx=(10, 20), pady=5)
        
        # Scrollable area for product listings
        product_list_frame = tk.Frame(self, bg="#f7f7f7")
        product_list_frame.grid(row=3, column=0, sticky="nsew")

        # Canvas and scrollbar
        canvas = tk.Canvas(product_list_frame, bg="#f7f7f7", height=500)
        canvas.grid(row=3, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(product_list_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame inside the canvas for products
        products_frame = tk.Frame(canvas, bg="#f7f7f7")
        canvas.create_window((0, 0), window=products_frame, anchor="nw")

        # Bind scrollwheel to the canvas
        canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, canvas))

        # Display products
        self.display_products(products_frame)

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

        for idx, product in enumerate(self.products):
            product_frame = tk.Frame(
                parent, bg="#fff", bd=1, relief="solid", padx=10, pady=10, width=200
            )
            product_frame.grid(row=idx // 6, column=idx % 6, padx=10, pady=10, sticky="nsew")

            # Placeholder for product image
            product_image = tk.Canvas(product_frame, width=100, height=100, bg="#ccc", bd=0, highlightthickness=0)
            product_image.create_text(50, 50, text="Image", fill="#777", font=("Arial", 10))
            product_image.pack()

            # Product Name
            product_name = tk.Label(product_frame, text=product["name"], font=("Arial", 14, "bold"), bg="#fff", fg="#333", width=13)
            product_name.pack(pady=(10, 5))

            # Product Price
            product_price = tk.Label(product_frame, text=f"${product['price']:.2f}", font=("Arial", 12), bg="#fff", fg="#007bff")
            product_price.pack()
