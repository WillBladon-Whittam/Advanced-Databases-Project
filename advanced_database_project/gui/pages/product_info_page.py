import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
from datetime import datetime
from typing import List, Dict

from advanced_database_project.backend.db_connection import DatabaseConnection
from advanced_database_project.gui.base_page import BasePage


class ProductInfoPage(BasePage):
    """
    A tkinter page to display detailed product information.
    Includes name, price, suppliers, reviews, and an add-to-basket button.
    """

    def __init__(self, pages: List[tk.Frame], db: DatabaseConnection, user: Dict[str, str], product: tuple):
        super().__init__(pages, db, user)
        self.configure(bg="#f7f7f7")
        
        self.product = product
        self.canvas = None
        
        self.canvas_scoll_bind = None
        self.canvas_scoll_region_bind = None
        
        self.rating = None
        self.stars = []
        
        self.create_widgets()
        
    def show(self):
        """
        Overide the default show function from BasePage - rebind the the scrollwheel to the scrollable canvas
        """
        self.update_scroll_region(None, self.canvas)
        self.canvas_scoll_bind = self.canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, self.canvas))
        self.canvas_scoll_region_bind = self.canvas.bind("<Configure>", lambda event: self.update_scroll_region(event, self.canvas))
        self.pack()
        
    def navigate_to(self, page):
        """
        Overide the default show function from BasePage - unbind the the scrollwheel to the scrollable canvas
        """
        self.rating = None
        self.canvas.unbind("<MouseWheel>", self.canvas_scoll_bind)
        self.canvas.unbind("<Configure>", self.canvas_scoll_region_bind)
        self.pack_forget()
        page.show()

    def create_widgets(self):
        """
        Create widgets for the product information page.
        """
        header_frame = tk.Frame(self, bg="#f7f7f7")
        header_frame.grid(row=1, column=0, sticky="nsew") 
        
        settings_message = tk.Frame(header_frame, bg="#e6e6e6", pady=20)
        settings_message.pack(fill="x")
        settings_message_label = tk.Label(
            settings_message,
            text=self.product[1],
            font=("Arial", 24, "bold"),
            bg="#e6e6e6",
            fg="#333",
            width=50,
        )
        settings_message_label.pack(pady=10)

        product_frame = tk.Frame(self, bg="#f7f7f7")
        product_frame.grid(row=2, column=0, pady=10, sticky="w")

        # Product Image
        if self.product[6] is not None:
                       
            image = Image.open(io.BytesIO(self.product[6]))

            image.thumbnail((320, 320), Image.LANCZOS)

            ph = ImageTk.PhotoImage(image)

            product_image = tk.Canvas(
                product_frame, width=320, height=320, bg="#fff", bd=0, highlightthickness=0)

            x_offset = (320 - image.width) // 2
            y_offset = (320 - image.height) // 2

            product_image.create_image(x_offset, y_offset, anchor="nw", image=ph)

            product_image.image = ph
            product_image.grid(row=0, column=0, pady=10, sticky="nw")
            
        price_label = tk.Label(product_frame, text=f"Price: ${self.product[3]:.2f}",
                               font=("Arial", 20), bg="#f7f7f7", fg="#007bff")
        price_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        details_frame = tk.Frame(product_frame, bg="#f7f7f7")
        details_frame.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="nw")
        
        product_name_label = tk.Label(details_frame, text=self.product[1],
                                    font=("Arial", 26), bg="#f7f7f7", fg="#555")
        product_name_label.pack(anchor="w", pady=5)
        
        category_label = tk.Label(details_frame, text=f"Category: {self.db.selectCategoriesById(self.product[2])[1]}",
                                    font=("Arial", 20), bg="#f7f7f7", fg="#555")
        category_label.pack(anchor="w")
        
        suppliers_label = tk.Label(details_frame, text=f"Suppliers:",
                                    font=("Arial", 20), bg="#f7f7f7", fg="#555")
        suppliers_label.pack(anchor="w", pady=5)
        
        for value in self.db.selectSuppliersById(self.product[5])[1:]:
            suppliers_info_label = tk.Label(details_frame, text=value,
                                        font=("Arial", 16), bg="#f7f7f7", fg="#555")
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
        
        reviews_label = tk.Label(scrollable_frame, text=f"Customer Reviews:", 
                                  font=("Arial", 20), bg="#f7f7f7", fg="#555")
        reviews_label.pack(anchor="nw", pady=(5, 0))
        
        for review in self.db.selectReviewsByProductId(self.product[0]):
            for i, review_value in enumerate(review[1:]):
                if i == 0:  # Customer ID
                    customer = self.db.selectCustomerById(review_value)       
                    review_info_label = tk.Label(scrollable_frame, text=customer[1] + " " +customer[2],
                                                font=("Arial", 16, "underline"), bg="#f7f7f7", fg="#555")
                    review_info_label.pack(anchor="nw")
                elif i == 1:  # Product ID
                    continue
                elif i == 2:  # Stars
                    stars = ""
                    for _ in range(int(review_value)):
                        stars += "\u2606"
                    review_info_label = tk.Label(scrollable_frame, text=stars,
                                            font=("Arial", 16), bg="#f7f7f7", fg="#555")
                    review_info_label.pack(anchor="nw")
                elif i == 3:  # Review Comment
                    if review_value:
                        review_info_label = tk.Label(scrollable_frame, text=review_value,
                                                    font=("Arial", 16), bg="#f7f7f7", fg="#555")
                    review_info_label.pack(anchor="nw")
                elif i == 4:  # Review Date
                    review_info_label = tk.Label(scrollable_frame, text=review_value + "\n",
                                                font=("Arial", 14), bg="#f7f7f7", fg="#555")
                    review_info_label.pack(anchor="nw")
                    
                    
        leave_review_frame = tk.Frame(product_frame, bg="#f7f7f7")
        leave_review_frame.grid(row=1, column=2, pady=10, sticky="w")
        
        self.review_entry = tk.Text(leave_review_frame, font=("Arial", 12), width=30, height=5, wrap="word")
        self.review_entry.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nw")
        
        for i in range(5):
            star = tk.Label(leave_review_frame, text="\u2606", font=("Arial", 24), bg="#f7f7f7", fg="#555", cursor="hand2")
            star.grid(row=0, column=1+i, padx=5, sticky="n")
            star.bind("<Button-1>", lambda event, r=i+1: self.update_rating(r))
            self.stars.append(star)
        
        leave_review_button = tk.Button(leave_review_frame, text="Leave a Review", font=("Arial", 14), bg="#30d424", fg="#fff",
                                        command=self.leave_review)
        leave_review_button.grid(row=1, column=0, padx=(10, 0), sticky="nw")
        
        basket_frame = tk.Frame(product_frame, bg="#f7f7f7")
        basket_frame.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

        add_to_basket_btn = tk.Button(basket_frame, text="Add to Basket", font=("Arial", 14), bg="#007bff",
                                      fg="#fff", activebackground="#0056b3", activeforeground="#fff",
                                      command=self.add_to_basket)
        add_to_basket_btn.pack()
        
        back_button = tk.Button(product_frame, text="Return", font=("Arial", 14), bg="#f7f7f7",
                                      fg="#555",
                                      command=lambda: self.navigate_to(self.pages["Products"]))
        back_button.grid(row=1, column=2, pady=10, padx=10, sticky="se")
        
        self.canvas_scoll_bind = self.canvas.bind_all("<MouseWheel>", lambda event: self.scroll_canvas(event, self.canvas))
        self.canvas_scoll_region_bind = self.canvas.bind("<Configure>", lambda event: self.update_scroll_region(event, self.canvas))
        
    def update_rating(self, new_rating):
        self.rating = new_rating
        for i in range(5):
            if i < self.rating:
                self.stars[i].config(text="\u2605", fg="gold")  # Filled star
            else:
                self.stars[i].config(text="\u2606", fg="gray")  # Empty star
                
    def leave_review(self):
        if self.rating is None:
            for star in self.stars:
                star.configure(highlightbackground="red", highlightcolor="red", highlightthickness=1)
            return
        self.db.addReview(self.user["Id"], self.product[0], self.rating, self.review_entry.get("1.0", "end-1c"), datetime.now().strftime("%d/%m/%Y"))
        self.create_widgets()
        self.rating = None
        
        
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

    def add_to_basket(self):
        ...
