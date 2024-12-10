from advanced_database_project.gui.app import App
from advanced_database_project.backend.db_connection import DatabaseConnection

import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reload-db', action='store_true')
    args = parser.parse_args()
    
    my_file = Path("./database.db")
        
    # Create database if it doesn't already exist, or the parser is set in the cmd
    if args.reload_db or not my_file.is_file():
        database_connection = DatabaseConnection()
        database_connection.sql.run_sql_script(Path("create_database_script.sql"))
        for path in Path("./advanced_database_project/assets/").iterdir():
           database_connection.insert_image(Path(path))
    else:
        database_connection = DatabaseConnection()

    
    App(database_connection)