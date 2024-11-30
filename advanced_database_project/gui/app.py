import tkinter as tk

from advanced_database_project.gui.pages.home_page import HomePage
from advanced_database_project.gui.pages.products_page import ProductsPage
from advanced_database_project.gui.pages.login_page import LoginPage
from advanced_database_project.gui.pages.register_page import RegisterPage
from advanced_database_project.gui.pages.account_page import AccountPage
from advanced_database_project.backend.db_connection import DatabaseConnection


class App(tk.Tk):
    """
    Main Application - Configures the tab, creates all the pages, runs even loop
    Opens the Home Page to start with.
    """
    
    def __init__(self, db: DatabaseConnection = None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.db = db
                
        self.title("Online Hardware Shop App")
        self.geometry("1280x720")       
                  
        # Create each page - store them in a Dictionary
        self.pages = {}
        self.user = {"Firstname": "",
                     "Surname": "",
                     "Gender": "",
                     "Email": "",
                     "Username": "",
                     "Password": ""}
        self.pages["Login"] = LoginPage(self.pages, self.db, self.user)
        self.pages["Register"] = RegisterPage(self.pages, self.db, self.user) 
        self.pages["Home"] = HomePage(self.pages, self.db, self.user)
        self.pages["Products"] = ProductsPage(self.pages, self.db, self.user)
        self.pages["Account"] = AccountPage(self.pages, self.db, self.user)
        # Shopping Cart Page
        # Checkout Page
        # Account Settings Page (Show customer details and orders)
        # Individual Product Pages - with reviews
        
        # Show the first page
        self.pages["Login"].pack()
                
        self.mainloop()
        