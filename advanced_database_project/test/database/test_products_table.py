import sqlite3


class TestProdoctsTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Products
            WHERE Product_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Products 
                                     (Product_Name, Category_ID, Price, Stock_Level, Supplier_ID, Product_Image)
                                     VALUES (?, ?, ?, ?, ?, ?)
                                     """, sql_parameters=data)

    def test_products_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, ('Gaming Laptop', 1, 1500, 50, 1, b'test'))

        result = self.select_latest_insert(setup_db)

        assert result["Product_Name"] == "Gaming Laptop"
        assert result["Category_ID"] == 1
        assert result["Price"] == 1500
        assert result["Stock_Level"] == 50
        assert result["Supplier_ID"] == 1
        assert result["Product_Image"] == b'test'

    def test_products_table_referential_integrity(self, setup_db):
        result = self.insert_data(setup_db, ('Gaming Laptop', 1000, 1500, 50, 1, None))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('Gaming Laptop', 1, 1500, 50, 1000, None))
        assert type(result) == sqlite3.IntegrityError

    def test_products_table_not_null_constraints(self, setup_db):
        result = self.insert_data(setup_db, (None, 1000, 1500, 50, 1, None))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('Gaming Laptop', None, 1500, 50, 1, None))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('Gaming Laptop', 1000, None, 50, 1, None))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('Gaming Laptop', 1000, 1500, None, 1, None))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('Gaming Laptop', 1000, 1500, 50, None, None))
        assert type(result) == sqlite3.IntegrityError



