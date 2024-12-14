from advanced_database_project.backend.sql import SqlWrapper

import hashlib
from pathlib import Path
from typing import Tuple, Literal, List, Dict, Any
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import xml.etree.ElementTree as ET


class DatabaseConnection(SqlWrapper):
    """
    Database Connection to handle the SQL Logic
    """

    def __init__(self, db: str = r".\database.db") -> None:
        super().__init__(db)

        # Hard code the tables. This stops SQL injection attacks if these are pre-defined
        self.tables = ["Customers", "Category", "Suppliers", "Products", "Orders",
                       "Billing", "Shipping", "Customer_Basket", "Basket_Contents", "Reviews"]

    def clear_database(self) -> List[None | Exception]:
        """
        Clear the entire database

        Returns:
            List[None | Exception]: Returns a list of the DROP TABLE SQL Query's executed.
                                    None is returned if the query is successful
                                    An exception is returned if an error occurs.
        """
        results = []
        for table in reversed(self.tables):
            results.append(self.update_table(f"DROP TABLE IF EXISTS {table}"))
        return results

    def check_tables(self) -> bool:
        """
        Check all the tables exists in the database

        Returns:
            bool: Returns True if all the expected tables are presnet
                  Returns False if there are any missing tables in the database
        """
        results = []
        for table in self.tables:
            results.append(True if self.select_query("""
                                                     SELECT name 
                                                     FROM sqlite_master 
                                                     WHERE type='table' AND name=?
                                                     """, sql_parameters=table) else False)
        return all(results)

    def backup_database_to_xml(self, xml_output_path: Path, include_images: bool = True) -> None:
        """
        Generate an XML file to create a backup of the database

        Args:
            xml_output_path (Path): The file location of where to generate the XML file
            include_images (bool): Whether to save the image BLOB data to the xml file. This makes teh XML file quite large.
        """
        root = Element("DatabaseBackup")

        for table_name in self.tables:
            table_elem = SubElement(root, "Table", name=table_name)

            schema_info = self.select_query(f"PRAGMA table_info({table_name})")
            unique_list = []
            index_list = self.select_query(f"PRAGMA index_list({table_name})")
            for index in index_list:
                if index["origin"] == "u":
                    for constraint in self.select_query(f"PRAGMA index_info({index["name"]})"):
                        unique_list.append(constraint["name"])

            schema_element = ET.SubElement(table_elem, "Schema")
            for column in schema_info:
                col_element = ET.SubElement(schema_element, "Column",
                                            name=column["name"], type=column["type"],
                                            notnull=str(column["notnull"]),
                                            pk=str(column["pk"]), unique="1" if column["name"] in unique_list else "0")
                if column["dflt_value"] is not None:
                    col_element.set("default", column["dflt_value"])

            constraints_element = ET.SubElement(table_elem, "Constraints")
            foreign_keys = self.select_query(f"PRAGMA foreign_key_list({table_name})")

            for fk in foreign_keys:
                ET.SubElement(constraints_element, "ForeignKey",
                              column=fk["from"], ref_table=fk["table"], ref_column=fk["to"])

            data_element = ET.SubElement(table_elem, "Data")
            rows = self.select_query(f"SELECT * FROM {table_name}")

            for row in rows:
                row_elem = SubElement(data_element, "Row")
                for col_name, col_value in row.items():
                    if not include_images and "Image" in col_name:
                        continue
                    col_elem = SubElement(row_elem, col_name)
                    if isinstance(col_value, bytes):
                        col_elem.text = col_value.hex() if col_value is not None else "NULL"
                    else:
                        col_elem.text = str(col_value) if col_value is not None else "NULL"

        tree = ElementTree(root)
        with open(xml_output_path, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

    def restore_database_from_xml(self, xml_input_path: Path) -> None:
        """
        Restore a database from an XML backup

        Args:
            xml_input_path (str): The path to the XML file
        """
        self.clear_database()

        tree = ET.parse(xml_input_path)
        root = tree.getroot()

        for table_element in root.findall('Table'):
            table_name = table_element.get('name')

            schema_element = table_element.find('Schema')
            columns = []
            for column_element in schema_element.findall('Column'):
                name = column_element.get('name')
                col_type = column_element.get('type')
                not_null = 'NOT NULL' if column_element.get('notnull') == '1' else ''
                default = f"DEFAULT {column_element.get('default')}" if column_element.get('default') else ''
                unique = 'UNIQUE' if column_element.get('unique') == '1' else ''
                columns.append(f"{name} {col_type} {not_null} {default} {unique}")

            primary_keys = []
            for column_element in schema_element.findall('Column'):
                if column_element.get('pk') != '0':
                    primary_keys.append(column_element.get('name'))

            columns.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

            constraints_element = table_element.find('Constraints')
            for fk_element in constraints_element.findall('ForeignKey'):
                column = fk_element.get('column')
                ref_table = fk_element.get('ref_table')
                ref_column = fk_element.get('ref_column')
                columns.append(f"CONSTRAINT {column}_fk FOREIGN KEY ({column}) REFERENCES {ref_table}({ref_column})")

            self.update_table(f"CREATE TABLE {table_name} ({', '.join(columns)})")

            data_element = table_element.find('Data')
            for row_element in data_element.findall('Row'):
                columns_str = ', '.join([f"{v.tag}" for v in row_element])  # Column names
                values_str = []
                for v in row_element:
                    col_name = v.tag
                    col_type = schema_element.find(f"Column[@name='{col_name}']").get('type')

                    if col_type.upper() == 'BLOB':
                        value = f"X'{v.text}'" if v.text else 'NULL'
                    else:
                        value = f"'{v.text}'" if v.text and v.text != 'NULL' else 'NULL'

                    values_str.append(value)
                values_str = ', '.join(values_str)
                self.update_table(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})")

        self.db.commit()

    def insert_image(self, image_path: Path) -> None | Exception:
        """
        Insert an Image into the products table.
        This takes the images stored in the assets file, and adds the BLOB data to the database.
        Storing binary hex for the images in the .sql script file is too large.

        Args:
            image_path (Path): _description_

        Returns:
            None: If the SQL Query is successful
            Exception: If the SQL Query fails
        """

        with open(image_path, 'rb') as img_file:
            binary_data = img_file.read()

        return self.update_table("UPDATE Products SET Product_Image = ? WHERE Product_Name = ?",
                                 sql_parameters=(binary_data, image_path.stem))

    def get_customer_by_login(self, username: str, password: str) -> Dict[str, Any] | False | None:
        """
        Get Customers Information from Username and Password
        
        Using SHA256 Hashing for the password

        Args:
            username (str): Users Username
            password (str): Users Password (raw string, not the hash)

        Returns:
             Dict[str, Any]: Returning a dict means that the information about the table has been returned successfully
            False: Returning False means that the username was found, but the password was incorrect
            None: Returning None means the username was not found.
        """
        password_hash = self.select_query("""
                                          SELECT Customer_Password 
                                          FROM Customers 
                                          WHERE Customer_Username = ?
                                          """, sql_parameters=username, fetch="one")
        if password_hash:
            if password_hash["Customer_Password"].hex() == hashlib.sha256(password.encode()).hexdigest():
                return self.select_query("""
                                         SELECT * 
                                         FROM Customers 
                                         WHERE Customer_Username = ?
                                         """, sql_parameters=username, fetch="one")
            else:
                return False
        else:
            return None

    def select_products(self, filter_name: str = "",
                        filter_category: str = "",
                        filter_price: Tuple[float, float] = (0, 5000),
                        sort_by: Literal["Name", "Category", "Price"] = "Name",
                        sort_order: Literal["ASC", "DSC"] = "ASC") -> List[Dict[str, Any]]:
        """
        Select Products from the products table, with the option to filter and sort the results.
        To avoid SQL injection attacks I have used SQL parametrization.
        As SQL parametrization only accepts literal values, this cannot be used for ORDER BY.
        Instead, the ORDER BY paramters are generated from a controlled dict.
        Since these values are not from direct user input, they are safe from SQL injection. 
        Only the actual filtered values are passed as parameters to the query execution.

        Args:
            filter_name (str): Filters the products by Name.
            filter_category (str):  Filters the products by Category.
            filter_price (Tuple[float, float]): Filters the products by Price.
            sort_by (Literal["Name", "Category", "Price"]): Sorts by either the Name, Category or Price field
            sort_order (Literal["ASC", "DSC"]): Sorts the sort_by field by either ASC or DESC order

        Returns:
            List[Dict[str, Any]]: Returns a List of Dicts of all the results found. List will be empty if nothing is found.
        """
        # Controlled Dict to store what to sort by
        sort_by_map = {
            "Name": "p.Product_Name",
            "Category": "c.Category_Name",
            "Price": "p.Price",
        }
        # Validation to ensure only ASC and DESC can be entered
        sort_order = "ASC" if sort_order.upper() == "ASC" else "DESC"

        return self.select_query(f"""
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
                                                 filter_price[1]))

    def get_basket_by_customer_id(self, customer_id: int) -> Dict[str, Any] | None:
        """
        Returns the customers basket

        Args:
            customer_id (int): The Customer ID to get the basket for

        Returns:
             Dict[str, Any]: Returns a dict of the customers basket
            None: If no customer basket is found with that Customer ID
        """
        return self.select_query(f"""SELECT * FROM Customer_Basket WHERE Customer_ID = ?""",
                                 sql_parameters=customer_id,
                                 fetch='one')

    def create_basket_by_customer_id(self, customer_id: int, date: str) -> Exception | None:
        """
        Create a basket for a customer

        Args:
            customer_id (int): The Customer ID to create the basket for
            date (str): The Date the basket was created

        Returns:
            None: If the SQL Query is successful
            Exception: If the SQL Query fails
        """
        return self.update_table(f"""INSERT INTO Customer_Basket (Customer_ID, Basket_Created_Date) VALUES (?, ?)""",
                                 sql_parameters=(customer_id, date))

    def add_item_to_basket(self, basket_id: int, product_id: int, quantity: int) -> Exception | None:
        """
        Add an item to the basket - If the item is already in the basket, add to the quantity

        Args:
            basket_id (int): The Basket ID
            product_id (int): The Product ID of the item to add
            quantity (int): The quantity of the item to add

        Returns:
            None: If the SQL Query is successful
            Exception: If the SQL Query fails
        """
        basket_items = self.get_basket_items_by_basket_id(basket_id)
        for item in basket_items:
            if item["Product_ID"] == product_id:
                self.update_basket_item(basket_id, product_id, quantity + int(item["Quantity"]))
                return
        return self.update_table(f"""INSERT INTO Basket_Contents (Basket_ID, Product_ID, Quantity) VALUES (?, ?, ?)""",
                                 sql_parameters=(basket_id, product_id, quantity))

    def get_basket_items_by_basket_id(self, basket_id: int) -> List[Dict[str, Any]]:
        """
        Get all the items in a basket

        Args:
            basket_id (int): The Basket ID to get the items for

        Returns:
             Dict[str, Any]: Returns a dict of the customers basket items
            None: If no customer basket is found with that Basket ID
        """
        return self.select_query("""
                                 SELECT 
                                    bc.Product_ID,
                                    p.Product_Name,
                                    p.Price,
                                    P.Product_Image,
                                    bc.Quantity,
                                    (p.Price * bc.Quantity) AS Total_Cost
                                 FROM 
                                    Basket_Contents AS bc
                                 JOIN 
                                    Products AS p ON bc.Product_ID = p.Product_ID
                                 WHERE 
                                    bc.Basket_ID = ?
                                 """, sql_parameters=basket_id)

    def remove_basket_item(self, basket_id: int, product_id: int) -> Exception | None:
        """
        Remove an item from a basket

        Args:
            basket_id (int): The Basket ID to remove the item from
            product_id (int): The Product ID to remove from that basket

        Returns:
            None: If the SQL Query is successful
            Exception: If the SQL Query fails
        """
        return self.update_table("""
                                 DELETE FROM Basket_Contents WHERE Basket_ID = ? AND Product_ID = ?
                                 """, sql_parameters=(basket_id, product_id))

    def update_basket_item(self, basket_id: int, product_id: int, quantity: int) -> Exception | None:
        """
        Update the Quantity of a basket. Only the quantity can be changed as the basket_id and
        product_id are both primary keys
        
        Args:
            basket_id (int): The Basket ID for the item
            product_id (int): The Product ID for the item to be updated
            quantity (int): The new quantity of the item

        Returns:
            None: If the SQL Query is successful
            Exception: If the SQL Query fails
        """
        return self.update_table("""
                                 UPDATE Basket_Contents
                                 SET Quantity = ?
                                 WHERE Basket_ID = ? AND Product_ID = ?
                                 """, sql_parameters=(quantity, basket_id, product_id))

    def get_customer_basket_value(self, basket_id: int) -> Dict[str, Any] | None:
        """
        Get the total basket value of a customer.
        Use the SQL View, this is defined in the .sql script.
        
        Args:
            basket_id (int): The Basket ID for the customer

        Returns:
             Dict[str, Any]: Returns a dict of the customers  value
            None: If no customer basket is found with that Customer ID
        """
        return self.select_query("""
                                 SELECT * FROM CustomerBasketValue WHERE Basket_ID = ?
                                 """, sql_parameters=basket_id, fetch='one')

    def select_categories(self) -> List[Dict[str, Any]]:
        """
        Returns all the product categories

        Returns:
            List[Dict[str, Any]]: Returns a List of dicts of all the results found.
                                  List will be empty if nothing is found.
        """
        return self.select_query(f"""SELECT * FROM category""")

    def select_customer_by_id(self, customer_id: int) -> Dict[str, Any] | None:
        """
        Returns a customer based on the Customer ID
        
        Args:
            customer_id (int): The Customer ID of the customer to get.

        Returns:
            Dict[str, Any]: Returns a dict of the customer
            None: If no customer is found with that Customer ID
        """
        return self.select_query(f"""SELECT * FROM Customers WHERE Customer_ID = ?""", sql_parameters=customer_id,
                                 fetch='one')

    def select_categories_by_id(self, category_id: int) -> Dict[str, Any] | None:
        """
        Returns a category based on the Category ID
        
        Args:
            category_id (int): The Category ID of the category to get.

        Returns:
            Dict[str, Any]: Returns a dict of categories
            None: If no categories is found with that Category ID
        """
        return self.select_query(f"""SELECT * FROM category WHERE Category_ID = ?""", sql_parameters=category_id,
                                 fetch='one')

    def select_suppliers_by_id(self, supplier_id: int) -> Dict[str, Any] | None:
        """
        Returns a supplier based on the Supplier ID
        
        Args:
            supplier_id (int): The Supplier ID of the supplier to get.

        Returns:
            Dict[str, Any]: Returns a dict of suppliers
            None: If no suppliers are found with that Supplier ID
        """
        return self.select_query(f"""SELECT * FROM Suppliers WHERE Supplier_ID = ?""", sql_parameters=supplier_id,
                                 fetch='one')

    def select_reviews_by_product_id(self, product_id: int) -> List[Dict[str, Any]]:
        """
        Returns reviews based on the Product ID
        
        Args:
            product_id (int): The Product ID of the reviews to get.

        Returns:
            List[Dict[str, Any]]: Returns a List of dicts of all the results found.
                                  List will be empty if nothing is found.
        """
        return self.select_query(f"""SELECT * FROM Reviews WHERE Product_ID = ?""", sql_parameters=product_id)

    def add_review(self, customer_id: int, product_id: int, review_stars: int, review_comment: str,
                   review_date: str) -> None | Exception:
        """
        Creates a New Review

        Args:
            customer_id (int): The Customer ID of customer leaving the review
            product_id (int): The Product ID of thr product
            review_stars (int): The number of stars out of 5
            review_comment (str): The review comment
            review_date (str): The review date

        Returns:
            None: If the SQL Query is successful
            Exception: If the SQL Query fails
        """
        return self.update_table("""
                                 INSERT INTO Reviews (Customer_ID, Product_ID, Review_Stars, Review_Comment, Review_Date)
                                 VALUES
                                 (?, ?, ?, ?, ?)
                                 """,
                                 sql_parameters=(customer_id, product_id, review_stars, review_comment, review_date))

    def select_best_selling_products(self) -> List[Dict[str, Any]]:
        """
        Returns the Top 6 best-selling products.
        This looks at all the orders and returns the top 6 that have been purchased the most.

        Returns:
            List[Dict[str, Any]]: Returns a List of dicts of all the results found.
                                  List will be empty if nothing is found.
        """
        return self.select_query("""
                                 SELECT 
                                    Products.Product_ID,
                                    Products.Product_Name,
                                    Products.Category_ID,
                                    Products.Price,
                                    Products.Stock_Level,
                                    Products.Supplier_ID,
                                    Products.Product_Image,
                                 SUM(Orders.Order_Quantity) AS Total_Ordered
                                 FROM Orders
                                 JOIN Products ON Orders.Product_ID = Products.Product_ID
                                 GROUP BY Products.Product_ID
                                 HAVING  Total_Ordered > 0
                                 ORDER BY Total_Ordered DESC
                                 LIMIT 6
                                 """)

    def insert_customer(self, firstname: str,
                        surname: str,
                        gender: Literal["Male", "Female"],
                        email: str,
                        username: str,
                        password: str) -> None | Exception:
        """
        Create a new customer in the customer table.
        Use SHA246 Hashing for the password.

        Args:
            firstname (str): The new users first name
            surname (str): The new users last name
            gender ("Male" or "Female"): The gender of the new user
            email (str): The email of the new user
            username (str): The username of the new user (This must be unique)
            password (str): The password of the user. Passed as a string, the SHA256 hash is applied in the method.

        Returns:
            Exception: Returns the SQLite exception if there is an error.
            None: Returns None of the insertion was successful
        """
        return self.update_table("""
                                 INSERT INTO Customers (Customer_Firstname, Customer_Surname, Customer_Gender, Customer_Email, Customer_Username, Customer_Password) 
                                 VALUES (?, ?, ?, ?, ?, ?)
                                 """, sql_parameters=(
            firstname, surname, gender, email, username, hashlib.sha256(password.encode()).digest()))

    def update_customer(self, current_username: str = None,
                        firstname: str = None,
                        surname: str = None,
                        gender: Literal["Male", "Female"] = None,
                        email: str = None,
                        new_username: str = None,
                        password: str = None) -> None | Exception:
        """
        Update an existing customer in the customer table.
        Use SHA246 Hashing for the password.

        Args:
            current_username (str): The current username of the user to be updated
            firstname (str): The new users first name
            surname (str): The new users last name
            gender ("Male" or "Female"): The gender of the new user
            email (str): The email of the new user
            new_username (str): The new username of the new user (This must be unique)
            password (str): The new password of the user. Passed as a string, the SHA256 hash is applied in the method.

        Returns:
            Exception: Returns the SQLite exception if there is an error.
            None: Returns None of the insertion was successful
        """
        if not current_username:
            raise ValueError("The current username is required.")

        set_clauses = []
        parameters = []

        if firstname is not None:
            set_clauses.append("Customer_Firstname = ?")
            parameters.append(firstname)

        if surname is not None:
            set_clauses.append("Customer_Surname = ?")
            parameters.append(surname)

        if gender is not None:
            set_clauses.append("Customer_Gender = ?")
            parameters.append(gender)

        if email is not None:
            set_clauses.append("Customer_Email = ?")
            parameters.append(email)

        if new_username is not None:
            set_clauses.append("Customer_Username = ?")
            parameters.append(new_username)

        if password is not None:
            set_clauses.append("Customer_Password = ?")
            parameters.append(hashlib.sha256(password.encode()).digest())

        if not set_clauses:
            raise ValueError("At least one field must be provided to update.")

        # Construct the SQL query
        query = f"""
                 UPDATE Customers
                 SET {', '.join(set_clauses)}
                 WHERE Customer_Username = ?
                 """
        parameters.append(current_username)

        # Execute the query
        return self.update_table(query, sql_parameters=tuple(parameters))


if __name__ == "__main__":
    connection = DatabaseConnection()
    products = connection.select_products()
    print(products)
