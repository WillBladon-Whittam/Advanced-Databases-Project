import tkinter as tk

from advanced_database_project.gui.pages.home_page import HomePage
from advanced_database_project.gui.pages.products_page import ProductsPage
from advanced_database_project.gui.pages.login_page import LoginPage
from advanced_database_project.gui.pages.register_page import RegisterPage
from advanced_database_project.gui.pages.account_page import AccountPage
from advanced_database_project.gui.pages.settings_page import SettingsPage
from advanced_database_project.gui.pages.basket_page import BasketPage
from advanced_database_project.backend.db_connection import DatabaseConnection


class App(tk.Tk):
    """
    Main Application - Configures the tab, creates all the pages, runs event loop
    Opens the Home Page to start with.
    """

    def __init__(self, db: DatabaseConnection = None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.db = db

        self.title("Online Hardware Shop App")
        self.geometry("1300x750")

        self.pages = {}
        self.basket = {}
        self.user = {}

        self.pages["Login"] = LoginPage(self.pages, self.db, self.user, self.basket)
        self.pages["Register"] = RegisterPage(self.pages, self.db, self.user, self.basket)
        self.pages["Home"] = HomePage(self.pages, self.db, self.user, self.basket)
        self.pages["Products"] = ProductsPage(self.pages, self.db, self.user, self.basket)
        self.pages["Account"] = AccountPage(self.pages, self.db, self.user, self.basket)
        self.pages["Settings"] = SettingsPage(self.pages, self.db, self.user, self.basket)
        self.pages["Cart"] = BasketPage(self.pages, self.db, self.user, self.basket)

        # Show the first page
        self.pages["Login"].pack()

        self.mainloop()
