import tkinter as tk

from advanced_database_project.gui.home_page import HomePage
from advanced_database_project.gui.products_page import ProductsPage
from advanced_database_project.backend.db_connection import DatabaseConnection


class App(tk.Tk):
    """
    Main Application - Configures the tab, creates all the pages, runs even loop
    Opens the Home Page to start with, 
    """
    
    def __init__(self, db: DatabaseConnection = None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.db = db
                
        self.title("Online Hardware Shop App")
        self.geometry("1280x720")
                
        # Create each page - store them in a Dictionary
        self.pages = {}
        self.pages["Home"] = HomePage(self.pages, self.db)
        self.pages["Products"] = ProductsPage(self.pages, self.db)
        
        # Show the first page
        self.pages["Home"].pack()
                
        self.mainloop()
        