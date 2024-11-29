from advanced_database_project.backend.sql import SqlWrapper

from typing import Tuple, Literal


class DatabaseConnection():
    """
    Database Connection to handle the SQL Logic
    """
    def __init__(self, db: str = r".\database.db") -> None:
        self.sql = SqlWrapper(db)
        
    def selectProducts(self, filter_name: str = "", 
                       filter_category: str = "", 
                       filter_price: Tuple[float, float] = (0, 5000),
                       sort_by: Literal["Name", "Category", "Price"] = "Name",
                       sort_order: Literal["ASC", "DSC"] = "ASC"):
        """
        Select Products from the products table, with the option to filter and sort the results.
        To avoid SQL injection attacks I have used SQL paramatization.
        As SQL paramatization only accepts literal values, this cannot be used for ORDER BY.
        Instead the ORDER BY paramters are generated from a controlled mapping. 
        Since these values are not derived directly from user input, they are safe from SQL injection. 
        Only the actual filtered values are passed as parameters to the query execution.
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
        
    def selectCategories(self):
        return self.sql.select_query(f"""SELECT * FROM category""")
    
    def selectBestSellingProducts(self):
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
    
    