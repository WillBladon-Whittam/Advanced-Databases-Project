import sqlite3
from pathlib import Path
from typing import Literal, Tuple, List


class SqlWrapper:
    """
    SQL Wrapper to create a connection to the database automatically and handle queries
    """
    def __init__(self, db_file: str = r".\database") -> None:
        self.db_file = db_file
        self.db = sqlite3.connect(self.db_file)
        self.cursor = self.db.cursor()
        self.cursor.execute("PRAGMA foreign_keys=ON")
        
    def __str__(self):
        return f"SQL Database wrapper for: {self.db_file}"
        
    def execute(self, sql_query: str, sql_parameters: Tuple[str, int] = tuple()) -> None:
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
                     sql_parameters: Tuple[str, int] = tuple(), 
                     fetch: Literal['all', 'many', 'one'] = "all", 
                     num_fetch: int = 1,
                     get_description: bool = False) -> List[tuple] | Tuple[List[tuple], Tuple[tuple]]:
        """
        Creates a SELECT query

        Args:
            sql_query (str): An SQL Query to execute
            sql_parameters (Tuple[str, int]): Parameters for an SQL query
            fetch (Literal['all', 'many', 'one']): If set to "all", fetches all the rows returned, 
                                                   If set to "one" returns only 1.
                                                   If set to "many" returns a set number of rows, specified by num_fetch
            get_description (bool): Get the description of the database
        """
        if not isinstance(sql_parameters, tuple):
            sql_parameters = (sql_parameters,)
        self.execute(sql_query, sql_parameters)
        
        if fetch == "all":
            results = self.cursor.fetchall()
        elif fetch == "many":
            results = self.cursor.fetchmany(num_fetch)
        elif fetch == "one":
            results = self.cursor.fetchone()
        
        if get_description:
            return results, self.cursor.description
        return results
        
    def update_table(self, sql_query: str, 
                     sql_parameters: Tuple[str, int] = tuple(), 
                     commit=True) -> None | Exception:
        """
        Creates a INSERT/UPDATE/DELETE query

        Args:
            sql_query (str): An SQL Query to execute
            sql_parameters (Tuple[str, int]): Parameters for an SQL query
            commit (bool): Commit changes to database immediatly
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
    sql = SqlWrapper(r"C:\Users\willb\Desktop\Uni\Modules\Second Year\COM519 Advanced Databases\Advanced-Databases-Project\database.db")
    print(sql)