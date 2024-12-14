import sqlite3
from pathlib import Path
from typing import Literal, Tuple, List, Any, Dict


class SqlWrapper:
    """
    SQL Wrapper to create a connection to the database automatically and handle queries

    SQL is configured to return Dict instead of tuples, with the keys as the column names and the values as the value
    """

    def __init__(self, db_file: str = r".\database") -> None:
        self.db_file = db_file
        self.db = sqlite3.connect(self.db_file)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()
        self.cursor.execute("PRAGMA foreign_keys=ON")

    def __str__(self):
        return f"SQL Database wrapper for: {self.db_file}"

    def execute(self, sql_query: str, sql_parameters: Tuple = tuple()) -> None:
        self.cursor.execute(sql_query, sql_parameters)

    def run_sql_script(self, sql_file_path: Path) -> None:
        """
        Run an .sql query script

        Args:
            sql_file_path (Path): The file path to the sql script
        """
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        self.cursor.executescript(sql_script)
        self.db.commit()

    def select_query(self, sql_query: str,
                     sql_parameters: Tuple | Any = tuple(),
                     fetch: Literal['all', 'many', 'one'] = "all",
                     num_fetch: int = 1) -> List[Dict[str, Any]] | Dict[str, Any] | None:
        """
        Creates a SELECT query

        Args:
            sql_query (str): An SQL Query to execute
            sql_parameters (Tuple | str): Parameters for an SQL query
            fetch (Literal['all', 'many', 'one']): If set to "all", fetches all the rows returned, 
                                                   If set to "one" returns only 1.
                                                   If set to "many" returns a set number of rows, specified by num_fetch
            num_fetch (int): The number of items to fetch if "many" selected for fetch

        Returns:
            List[Dict[str, Any]]: If multiple results are being fetched (fetch set to all/many),
                                  a list of the results are returned. If no results are found an empty list is returned.
            Dict[str, Any]: If only one result is fetched (fetch set to one), just a single result is returned.
            None: If only one result is expected (fetch set to one), but nothing was returned, None is returned.

        """
        if not isinstance(sql_parameters, tuple):
            sql_parameters = (sql_parameters,)
        self.execute(sql_query, sql_parameters)

        results = None
        if fetch == "all":
            results = [dict(row) for row in self.cursor.fetchall()]
        elif fetch == "many":
            results = [dict(row) for row in self.cursor.fetchmany(num_fetch)]
        elif fetch == "one":
            results = None if (result := self.cursor.fetchone()) is None else dict(result)

        return results

    def update_table(self, sql_query: str,
                     sql_parameters: Tuple | Any = tuple(),
                     commit=True) -> None | Exception:
        """
        Creates a INSERT/UPDATE/DELETE query

        Args:
            sql_query (str): An SQL Query to execute
            sql_parameters (Tuple | str): Parameters for an SQL query
            commit (bool): Commit changes to database immediately

        Returns:
            None: If the SQL Query is successful
            Exception: If the SQL Query fails
        """
        if not isinstance(sql_parameters, tuple):
            sql_parameters = (sql_parameters,)
        try:
            self.execute(sql_query, sql_parameters)
        except sqlite3.IntegrityError as e:
            self.db.rollback()
            return e
        except sqlite3.Error as e:
            self.db.rollback()
            print("Database Error!", e)
            return e
        if commit:
            self.db.commit()

    def close(self) -> None:
        self.db.close()


if __name__ == "__main__":
    sql = SqlWrapper(
        r"C:\Users\willb\Desktop\Uni\Modules\Second Year\COM519 Advanced Databases\Advanced-Databases-Project\database.db")
    print(sql)
