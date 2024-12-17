import sqlite3


class TestCustomerBasketTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Customer_Basket
            WHERE Basket_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Customer_Basket (Customer_ID, Basket_Created_Date) VALUES (?, ?)
                                     """, sql_parameters=data)

    def test_customer_basket_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, (1, '2024-01-13'))

        result = self.select_latest_insert(setup_db)

        assert result["Customer_ID"] == 1
        assert result["Basket_Created_Date"] == '2024-01-13'

    def test_customer_basket_table_referential_integrity(self, setup_db):
        result = self.insert_data(setup_db, (1000, '2024-01-13'))
        assert type(result) == sqlite3.IntegrityError

    def test_customer_basket_table_not_null_constraints(self, setup_db):
        result = self.insert_data(setup_db, (None, '2024-01-13'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1000, None))
        assert type(result) == sqlite3.IntegrityError



