import sqlite3


class TestBasketContentsTable:

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Basket_Contents (Basket_ID, Product_ID, Quantity) VALUES (?, ?, ?)
                                     """, sql_parameters=data)

    def test_customer_contents_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, (1, 2, 1))

        result = setup_db.select_query(
            """
            SELECT * FROM Basket_Contents
            WHERE Basket_ID = ? AND Product_ID = ?
            """, sql_parameters=(1, 2), fetch="one",
        )

        assert result["Basket_ID"] == 1
        assert result["Product_ID"] == 2
        assert result["Quantity"] == 1

    def test_basket_contents_table_referential_integrity(self, setup_db):
        result = self.insert_data(setup_db, (1000, 2, 1))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1, 1000, 1))
        assert type(result) == sqlite3.IntegrityError

    def test_basket_contents_table_not_null_constraints(self, setup_db):
        result = self.insert_data(setup_db, (None, 2, 1))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1000, None, 1))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1000, 2, None))
        assert type(result) == sqlite3.IntegrityError



