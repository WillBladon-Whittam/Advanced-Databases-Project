import sqlite3


class TestSuppliersTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Suppliers
            WHERE Supplier_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Suppliers 
                                     (Supplier_Name, Supplier_Email, Supplier_Phone, Supplier_HQ_Street_Number, 
                                     Supplier_HQ_Street, Supplier_HQ_Postcode)
                                     VALUES (?, ?, ?, ?, ?, ?)
                                     """, sql_parameters=data)

    def test_suppliers_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, (
            'Consoles Ltd.', 'console@techsupplies.co.uk', '+44 20 7946 0951', 13, 'Test Ave', 'WC2N 3DU'))

        result = self.select_latest_insert(setup_db)

        assert result["Supplier_Name"] == "Consoles Ltd."
        assert result["Supplier_Email"] == "console@techsupplies.co.uk"
        assert result["Supplier_Phone"] == "+44 20 7946 0951"
        assert result["Supplier_HQ_Street_Number"] == 13
        assert result["Supplier_HQ_Street"] == "Test Ave"
        assert result["Supplier_HQ_Postcode"] == "WC2N 3DU"

    def test_suppliers_table_not_null_constraints(self, setup_db):
        result = self.insert_data(
            setup_db, (None, 'console@techsupplies.co.uk', '+44 20 7946 0951', 13, 'Test Ave', 'WC2N 3DU'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ('Consoles Ltd.', None, '+44 20 7946 0951', 13, 'Test Ave', 'WC2N 3DU'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ('Consoles Ltd.', 'console@techsupplies.co.uk', None, 13, 'Test Ave', 'WC2N 3DU'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ('Consoles Ltd.', 'console@techsupplies.co.uk', '+44 20 7946 0951', None, 'Test Ave', 'WC2N 3DU'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ('Consoles Ltd.', 'console@techsupplies.co.uk', '+44 20 7946 0951', 13, None, 'WC2N 3DU'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ('Consoles Ltd.', 'console@techsupplies.co.uk', '+44 20 7946 0951', 13, 'Test Ave', None))
        assert type(result) == sqlite3.IntegrityError



