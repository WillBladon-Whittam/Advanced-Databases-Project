from advanced_database_project.backend.sql import SqlWrapper

import hashlib
from typing import Tuple, Literal, List


class DatabaseConnection():
    """
    Database Connection to handle the SQL Logic
    """
    def __init__(self, db: str = r".\database.db") -> None:
        self.sql = SqlWrapper(db)
        
    def getCustomerByLogin(self, username: str, password: str) -> Tuple | False | None:
        """
        Get Customers Information from Username and Password
        
        Using SHA256 Hashing for the password

        Args:
            username (str): Users Username
            password (str): Users Password (raw string, not the hash)

        Returns:
            Tuple: Returning a tuple means that the information about the table has been returned successfully
            False: Returning False means that the username was found, but the password was incorrect
            None: Returning None means the username was not found.
        """        
        password_hash = self.sql.select_query("""
                                              SELECT Customer_Password 
                                              FROM Customers 
                                              WHERE Customer_Username = ?
                                              """, sql_parameters=(username,),
                                                   fetch="one")
        if password_hash:
            if password_hash[0].hex() == hashlib.sha256(password.encode()).hexdigest():
                return self.sql.select_query("""
                                              SELECT * 
                                              FROM Customers 
                                              WHERE Customer_Username = ?
                                              """, sql_parameters=(username,),
                                                   fetch="one")
            else:
                return False
        else:
            return None
        
    def selectProducts(self, filter_name: str = "", 
                       filter_category: str = "", 
                       filter_price: Tuple[float, float] = (0, 5000),
                       sort_by: Literal["Name", "Category", "Price"] = "Name",
                       sort_order: Literal["ASC", "DSC"] = "ASC") -> List[Tuple]:
        """
        Select Products from the products table, with the option to filter and sort the results.
        To avoid SQL injection attacks I have used SQL paramatization.
        As SQL paramatization only accepts literal values, this cannot be used for ORDER BY.
        Instead the ORDER BY paramters are generated from a controlled dict. 
        Since these values are not from direct user input, they are safe from SQL injection. 
        Only the actual filtered values are passed as parameters to the query execution.

        Args:
            filter_name (str): Filters the products by Name.
            filter_category (str):  Filters the products by Category.
            filter_price (Tuple[float, float]): Filters the products by Price.
            sort_by (Literal["Name", "Category", "Price"]): Sorts by either the Name, Category or Price field
            sort_order (Literal["ASC", "DSC"]): Sorts the sort_by field by either ASC or DESC order

        Returns:
            List[Tuple]: Returns a List of Tuples of all the results found. List will be empty if nothing is found.
        """        
        # Controlled Dict to store what to sort by
        sort_by_map = {
            "Name": "p.Product_Name",
            "Category": "c.Category_Name",
            "Price": "p.Price",
        }
        # Validation to ensure only ASC and DESC can be entered
        sort_order = "ASC" if sort_order.upper() == "ASC" else "DESC"
        
        return self.sql.select_query(f"""
                                    SELECT * FROM products as p
                                    INNER JOIN category c ON p.Category_ID = c.Category_ID
                                    WHERE p.Product_Name LIKE ? AND
                                          c.Category_Name LIKE ? AND
                                          p.Price >= ? AND
                                          p.Price <= ?
                                    ORDER BY {sort_by_map[sort_by]} {sort_order}
                                    """,
                                    sql_parameters=(f"%{filter_name}%",
                                                    f"%{filter_category}%",
                                                    filter_price[0],
                                                    filter_price[1],))
        
    def selectCategories(self) -> List[Tuple]:
        """
        Returns all the product categories

        Returns:
            List[Tuple]: Returns a List of Tuples of all the results found. List will be empty if nothing is found.
        """        
        return self.sql.select_query(f"""SELECT * FROM category""")
    
    def selectBestSellingProducts(self) -> List[Tuple]:
        """
        Returns the Top 6 best selling products.
        This looks at all the orders and returns the top 6 that have been purchased the most.

        Returns:
            List[Tuple]: Returns a List of Tuples of all the results found. List will be empty if nothing is found.
        """        
        return self.sql.select_query("""
                                     SELECT 
                                        Products.Product_ID,
                                        Products.Product_Name,
                                        Products.Price,
                                     SUM(Orders.Order_Quantity) AS Total_Ordered
                                     FROM Orders
                                     JOIN Products ON Orders.Product_ID = Products.Product_ID
                                     GROUP BY Products.Product_ID
                                     HAVING  Total_Ordered > 0
                                     ORDER BY Total_Ordered DESC
                                     LIMIT 6;
                                     """)
        
if __name__ == "__main__":
    connection = DatabaseConnection()
    products = connection.selectProducts()
    print(products)
    
    