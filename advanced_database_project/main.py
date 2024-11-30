from advanced_database_project.gui.app import App
from advanced_database_project.backend.db_connection import DatabaseConnection

if __name__ == "__main__":
    App(DatabaseConnection())