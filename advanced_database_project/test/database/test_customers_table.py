import sqlite3


class TestCustomerTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Customers
            WHERE Customer_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Customers 
                                     (Customer_Firstname, Customer_Surname, Customer_Gender, Customer_Email, 
                                     Customer_Username, Customer_Password) 
                                     VALUES (?, ?, ?, ?, ?, ?)
                                     """, sql_parameters=data)

    def test_customer_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, ("David", "Smith", "Female", "david.smith@example.com","dsmith", b"securepassword"))

        result = self.select_latest_insert(setup_db)

        assert result["Customer_Firstname"] == "David"
        assert result["Customer_Surname"] == "Smith"
        assert result["Customer_Gender"] == "Female"
        assert result["Customer_Email"] == "david.smith@example.com"
        assert result["Customer_Username"] == "dsmith"
        assert isinstance(result["Customer_Password"], bytes)

    def test_customer_table_unique_constraints(self, setup_db):
        self.insert_data(
            setup_db, ("David", "Smith", "Female", "david.smith@example.com", "dsmith", b"securepassword"))
        result = self.insert_data(
            setup_db, ("David", "Smith", "Female", "david.smith@example.com","dsmith", b"securepassword"))

        assert type(result) == sqlite3.IntegrityError

    def test_customer_table_not_null_constraints(self, setup_db):
        result = self.insert_data(
            setup_db, (None, "Smith", "Female", "david.smith@example.com", "dsmith", b"securepassword"))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ("David", None, "Female", "david.smith@example.com", "dsmith", b"securepassword"))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ("David", "Smith", None, "david.smith@example.com", "dsmith", b"securepassword"))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ("David", "Smith", "Female", None, "dsmith", b"securepassword"))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ("David", "Smith", "Female", "david.smith@example.com", None, b"securepassword"))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(
            setup_db, ("David", "Smith", "Female", "david.smith@example.com", "dsmith", None))
        assert type(result) == sqlite3.IntegrityError



