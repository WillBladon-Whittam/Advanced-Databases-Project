import sqlite3


class TestShippingTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Shipping
            WHERE Shipping_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Shipping 
                                     (Customer_ID, Shipping_Address_Street_Number, Shipping_Address_Street, 
                                     Shipping_Address_Postcode, Delivery_Date)
                                     VALUES (?, ?, ?, ?, ?)
                                     """, sql_parameters=data)

    def test_shipping_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, (1, 123, 'Main St', 'SW1A 1AA', '2024-01-13'))

        result = self.select_latest_insert(setup_db)

        assert result["Customer_ID"] == 1
        assert result["Shipping_Address_Street_Number"] == 123
        assert result["Shipping_Address_Street"] == 'Main St'
        assert result["Shipping_Address_Postcode"] == 'SW1A 1AA'
        assert result["Delivery_Date"] == '2024-01-13'

    def test_shipping_table_referential_integrity(self, setup_db):
        result = self.insert_data(setup_db, (1000, 123, 'Main St', 'SW1A 1AA', '2024-01-13'))
        assert type(result) == sqlite3.IntegrityError

    def test_shipping_table_not_null_constraints(self, setup_db):
        result = self.insert_data(setup_db, (None, 123, 'Main St', 'SW1A 1AA', '2024-01-13'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1, None, 'Main St', 'SW1A 1AA', '2024-01-13'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1, 123, None, 'SW1A 1AA', '2024-01-13'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1, 123, 'Main St', None, '2024-01-13'))
        assert type(result) == sqlite3.IntegrityError
