import sqlite3
from typing import Literal, Tuple


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
        
    def select_query(self, sql_query, sql_parameters: Tuple[str, int] = tuple(), fetch: Literal['all', 'many', 'one'] = "all", num_fetch: int = 1):
        """
        Creates a SELECT query

        Args:
            sql_query: An SQL Query to execute
            sql_parameters: Parameters for an SQL query
            fetch: If set to "all", fetches all the rows returned, 
                   If set to "one" returns only 1.
                   If set to "many" returns a set number of rows, specified by num_fetch
        """
        if not isinstance(sql_parameters, tuple):
            sql_parameters = (sql_parameters,)
        self.execute(sql_query, sql_parameters)
        if fetch == "all":
            return self.cursor.fetchall()
        elif fetch == "many":
            return self.cursor.fetchmany(num_fetch)
        elif fetch == "one":
            return self.cursor.fetchone()
        
    def update_table(self, sql_query, sql_parameters: Tuple[str, int] = tuple(), commit=True) -> None | Exception:
        """
        Creates a INSERT/UPDATE/DELETE query

        Args:
            sql_query: An SQL Query to execute
            sql_parameters: Parameters for an SQL query
            commit: Commit changes to database immediatly
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
            print("Database Error!")
            return e
        if commit:
            self.db.commit()
 
    def close(self) -> None:
        self.db.close()
    
if __name__ == "__main__":
    sql = SqlWrapper(r"C:\Users\willb\Desktop\Uni\Modules\Second Year\COM519 Advanced Databases\Advanced-Databases-Project\database.db")
    print(sql)