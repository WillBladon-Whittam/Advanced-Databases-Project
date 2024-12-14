from advanced_database_project.backend.db_connection import DatabaseConnection

from abc import ABC, abstractmethod
import tkinter as tk
from typing import List, Dict, Any, Self


class BasePage(tk.Frame, ABC):
    """
    GUI Base Page
    
    Creates all the content that is the same on every page.
    This class is inherited by all other pages.
    """

    def __init__(self, pages: Dict[str, Self], db: DatabaseConnection, user: Dict[str, Any], basket: Dict[str, Any],
                 create_base: bool = True):
        super().__init__()
        self.pages = pages
        self.db = db
        self.user = user
        self.basket = basket
        self.create_base = create_base

        if self.create_base:
            self.create_navbar()
            self.create_footer()

    def navigate_to(self, page: Self) -> None:
        """
        Navigate to a new page.
        Closes the current page, opens the new page given as a parameter

        Args:
            page (BasePage / tk.Frame): The page that should be opened
        """
        self.pack_forget()
        page.show()

    def show(self) -> None:
        """
        Show the page
        """
        self.pack()

    def refresh_page(self) -> None:
        """
        Refreshes a page.
        This is done by tearing down all the current widgets on the page, and recreating the base widgets.
        """
        for widget in self.winfo_children():
            widget.destroy()
        if self.create_base:
            self.create_navbar()
            self.create_footer()
        self.create_widgets()

    def create_navbar(self) -> tk.Frame:
        """
        Create a navigation bar at the top.

        Returns:
            tk.Frame: Returns the Navbar created
        """
        navbar = tk.Frame(self, bg="#333", height=50)
        navbar.grid(row=0, column=0, sticky="nsew")

        buttons = ["Home", "Products", "Cart", "Account", "Settings"]
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

    def create_footer(self) -> tk.Frame:
        """
        Create a footer section.

        Returns:
            tk.Frame: Returns the Footer created
        """

        footer = tk.Frame(self, bg="#333", height=50)
        footer.grid(row=100, column=0, sticky="nsew")  # Arbitrary big row value (make sure it's at the bottom)

        footer_label = tk.Label(
            footer,
            text="© 2024 Online Hardware Store | Contact us at support@hardwarestore.com",
            font=("Arial", 10),
            bg="#333",
            fg="#fff",
        )
        footer_label.pack(pady=10)

        return footer

    @staticmethod
    def scroll_canvas(event, canvas):
        """
        Scroll the canvas with the mouse wheel.
        """
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    @staticmethod
    def update_scroll_region(event, canvas):
        """
        Update the scroll region of the canvas. Stops the canvas from scrolling forever.
        """
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    @abstractmethod
    def create_widgets(self) -> None:
        """
        Create all the widgets for the body of the page
        """
        ...
