import tkinter as tk

class BasePage(tk.Frame):
    """
    GUI Base Page
    
    Creates all the content that is the same on every page.
    """
    def __init__(self, pages, db, user, create_base: bool = True):
        self.pages = pages
        self.db = db
        self.user = user
        
        super().__init__()
        
        if create_base:
            # Create navigation bar
            self.create_navbar()

            # Create footer
            self.create_footer()

    def navigate_to(self, page):
        self.pack_forget()
        page.show()
        
    def show(self):
        self.pack()
    
    def create_navbar(self):
        """
        Create a navigation bar at the top.
        """
        navbar = tk.Frame(self, bg="#333", height=50)
        navbar.grid(row=0, column=0, sticky="nsew")

        # Navigation buttons
        buttons = ["Home", "Products", "Cart", "Account", "Contact"]
        for button_text in buttons:
            button = tk.Button(
                navbar,
                text=button_text,
                font=("Arial", 12),
                bg="#333",
                fg="#fff",
                activebackground="#555",
                activeforeground="#fff",
                bd=0,
                padx=17,
                pady=10,
                width=23,
                command=lambda text=button_text: self.navigate_to(self.pages[text]),
            )
            button.pack(side="left")

        return navbar
    
    def create_footer(self):
        """
        Create a footer section.
        """

        footer = tk.Frame(self, bg="#333", height=50)
        footer.grid(row=100, column=0, sticky="nsew")  # Arbitrary big row value (make sure its at the bottom)

        footer_label = tk.Label(
            footer,
            text="© 2024 Online Hardware Store | Contact us at support@hardwarestore.com",
            font=("Arial", 10),
            bg="#333",
            fg="#fff",
        )
        footer_label.pack(pady=10)

        return footer