from advanced_database_project.gui.app import App
from advanced_database_project.backend.db_connection import DatabaseConnection

import argparse
from pathlib import Path
import os
import atexit


def cleanup():
    if os.path.isfile("running_process.pid"):
        os.remove("running_process.pid")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reload-db', action='store_true')
    args = parser.parse_args()

    # Check there is only 1 instance of the application running
    if os.path.isfile("running_process.pid"):
        print("Another instance of the script is already running. If not, remove 'running_process.pid' file.")
        quit()

    with open("running_process.pid", 'w') as pid_file:
        pid_file.write(str(os.getpid()))

    atexit.register(cleanup)

    # Create database if it doesn't already exist (if tables are missing
    # the database is automatically regenerated), or the parser is set in the cmd
    my_file = Path("./database.db")
    database_connection = DatabaseConnection()
    if args.reload_db or not my_file.is_file() or not database_connection.check_tables():
        database_connection.run_sql_script(Path("create_database_script.sql"))
        for path in Path("./advanced_database_project/assets/").iterdir():
            database_connection.insert_image(Path(path))

    # Run the application
    App(database_connection)
