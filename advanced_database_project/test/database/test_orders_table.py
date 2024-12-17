import sqlite3


class TestOrdersTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Orders
            WHERE Order_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Orders 
                                     (Order_Date, Customer_ID, Product_ID, Shipping_ID, Billing_ID, 
                                     Order_Quantity, Order_Status)
                                     VALUES (?, ?, ?, ?, ?, ?, ?)
                                     """, sql_parameters=data)

    def test_orders_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, ('2024-01-13', 1, 1, 1, 1, 1, 'Delivered'))

        result = self.select_latest_insert(setup_db)

        assert result["Order_Date"] == '2024-01-13'
        assert result["Customer_ID"] == 1
        assert result["Product_ID"] == 1
        assert result["Shipping_ID"] == 1
        assert result["Billing_ID"] == 1
        assert result["Order_Quantity"] == 1
        assert result["Order_Status"] == 'Delivered'

    def test_orders_table_referential_integrity(self, setup_db):
        result = self.insert_data(setup_db, ('2024-01-13', 1000, 1, 1, 1, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, 1000, 1, 1, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, 1, 1000, 1, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, 1, 1, 1000, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError

    def test_orders_table_not_null_constraints(self, setup_db):
        result = self.insert_data(setup_db, (None, 1, 1, 1, 1, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', None, 1, 1, 1, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, None, 1, 1, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, 1, None, 1, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, 1, 1, None, 1, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, 1, 1, 1, None, 'Delivered'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, ('2024-01-13', 1, 1, 1, 1, 1, None))
        assert type(result) == sqlite3.IntegrityError



