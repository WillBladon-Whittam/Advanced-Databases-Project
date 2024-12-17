import sqlite3


class TestBillingTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Billing
            WHERE Billing_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Billing 
                                     (Customer_ID, Billing_Address_Street_Number, Billing_Address_Street, 
                                     Billing_Address_Postcode, Card_Number, Card_Expiry, Name_on_Card, CVC)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                     """, sql_parameters=data)

    def test_billing_table_valid_data_insertion(self, setup_db):
        self.insert_data(
            setup_db, (1, 123, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', "123"))

        result = self.select_latest_insert(setup_db)

        assert result["Customer_ID"] == 1
        assert result["Billing_Address_Street_Number"] == 123
        assert result["Billing_Address_Street"] == 'Main St'
        assert result["Billing_Address_Postcode"] == 'SW1A 1AA'
        assert result["Card_Number"] == '1234 5678 9101 1123'
        assert result["Card_Expiry"] == 'Dec-25'
        assert result["Name_on_Card"] == 'MrJohn V Doe'
        assert result["CVC"] == "123"

    def test_billing_table_referential_integrity(self, setup_db):
        result = self.insert_data(
            setup_db, (1000, 123, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', 123))
        assert type(result) == sqlite3.IntegrityError

    def test_billing_table_not_null_constraints(self, setup_db):
        result = self.insert_data(
            setup_db, (None, 123, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', 123))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, (1000, None, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', 123))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, (1000, 123, None, 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', 123))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, (1000, 123, 'Main St', None, '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', 123))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, (1000, 123, 'Main St', 'SW1A 1AA', None, 'Dec-25', 'MrJohn V Doe', 123))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, (1000, 123, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', None, 'MrJohn V Doe', 123))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, (1000, 123, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', None, 123))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, (1000, 123, 'Main St', 'SW1A 1AA', '1234 5678 9101 1123', 'Dec-25', 'MrJohn V Doe', None))
        assert type(result) == sqlite3.IntegrityError



