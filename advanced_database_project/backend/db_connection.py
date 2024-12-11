from advanced_database_project.backend.sql import SqlWrapper

import hashlib
from pathlib import Path
from typing import Tuple, Literal, List
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
        Clear the entire databaase
        """
        results = []
        for table in reversed(self.tables):
            results.append(self.update_table(f"DROP TABLE IF EXISTS {table};"))
        return results
        
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

            schema_element = ET.SubElement(table_elem, "Schema")
            for column in schema_info:
                col_element = ET.SubElement(schema_element, "Column", 
                                            name=column[1], type=column[2], 
                                            notnull=str(column[3]), 
                                            pk=str(column[5]))
                if column[4] is not None:
                    col_element.set("default", column[4])

            constraints_element = ET.SubElement(table_elem, "Constraints")
            foreign_keys = self.select_query(f"PRAGMA foreign_key_list({table_name})")

            for fk in foreign_keys:
                ET.SubElement(constraints_element, "ForeignKey",
                            column=fk[3], ref_table=fk[2], ref_column=fk[4])
                
            data_element = ET.SubElement(table_elem, "Data")            
            rows, description = self.select_query(f"SELECT * FROM {table_name}", get_description=True)
            column_names = [desc[0] for desc in description]

            for row in rows:
                row_elem = SubElement(data_element, "Row")
                for col_name, col_value in zip(column_names, row):
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
            
    def restore_database_from_xml(self, xml_input_path: str):
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
                pk = 'PRIMARY KEY' if column_element.get('pk') == '1' else ''
                columns.append(f"{name} {col_type} {not_null} {default} {pk}")

            constraints_element = table_element.find('Constraints')
            for fk_element in constraints_element.findall('ForeignKey'):
                column = fk_element.get('column')
                ref_table = fk_element.get('ref_table')
                ref_column = fk_element.get('ref_column')
                columns.append(f"CONSTRAINT {column}_fk FOREIGN KEY ({column}) REFERENCES {ref_table}({ref_column})")
                
            self.update_table(f"CREATE TABLE {table_name} ({', '.join(columns)});")

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
                self.update_table(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});")
                
        self.db.commit()
                
    def insert_image(self, image_path: Path):
        """
        Insert an Image into the products table.
        This takes the images stored in the assets file, and adds the BLOB data to the database.
        Storing binary hex for the images in the .sql script file is too large.

        Args:
            image_path (Path): _description_
        """
        
        with open(image_path, 'rb') as img_file:
            binary_data = img_file.read()

        self.update_table("UPDATE Products SET Product_Image = ? WHERE Product_Name = ?",
                              sql_parameters=(binary_data, image_path.stem))
        
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
        password_hash = self.select_query("""
                                              SELECT Customer_Password 
                                              FROM Customers 
                                              WHERE Customer_Username = ?
                                              """, sql_parameters=(username,),
                                                   fetch="one")
        if password_hash:
            if password_hash[0].hex() == hashlib.sha256(password.encode()).hexdigest():
                return self.select_query("""
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
                                                    filter_price[1],))
        
    def selectCategories(self) -> List[Tuple]:
        """
        Returns all the product categories

        Returns:
            List[Tuple]: Returns a List of Tuples of all the results found. List will be empty if nothing is found.
        """        
        return self.select_query(f"""SELECT * FROM category""")
    
    def selectBestSellingProducts(self) -> List[Tuple]:
        """
        Returns the Top 6 best selling products.
        This looks at all the orders and returns the top 6 that have been purchased the most.

        Returns:
            List[Tuple]: Returns a List of Tuples of all the results found. List will be empty if nothing is found.
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
                                     LIMIT 6;
                                     """)
        
    def insertCustomer(self, firstname: str, 
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
                                     """, sql_parameters=(firstname, surname, gender, email, username, hashlib.sha256(password.encode()).digest()))
        
    def updateCustomer(self, current_username: str,
                       firstname: str, 
                       surname: str, 
                       gender: Literal["Male", "Female"], 
                       email: str, 
                       new_username: str, 
                       password: str) -> None | Exception:
        """
        Update an existing customer in the customer table.
        Use SHA246 Hashing for the password.

        Args:
            current_username (str): The current username of the user to be updated
            firstname (str): The new users first name
            surname (str): The new users last name
            gender ("Male" or "Female"): The gender of the new user
            email (str): The email of the new user
            username (str): The new username of the new user (This must be unique)
            password (str): The new password of the user. Passed as a string, the SHA256 hash is applied in the method.

        Returns:
            Exception: Returns the SQLite exception if there is an error.
            None: Returns None of the insertion was successful
        """
        return self.update_table("""
                                     UPDATE Customers
                                     SET Customer_Firstname = ?,
                                         Customer_Surname = ?,
                                         Customer_Gender = ?,
                                         Customer_Email = ?,
                                         Customer_Username = ?,
                                         Customer_Password = ?
                                     WHERE Customer_Username = ?
                                     """, sql_parameters=(firstname, surname, gender, email, new_username, hashlib.sha256(password.encode()).digest(), current_username))
        
    
if __name__ == "__main__":
    connection = DatabaseConnection()
    products = connection.selectProducts()
    print(products)
    
    