import sqlite3


class TestReviewsTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Reviews
            WHERE Review_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Reviews 
                                     (Customer_ID, Product_ID, Review_Stars, Review_Comment, Review_Date) 
                                     VALUES (?, ?, ?, ?, ?)
                                     """, sql_parameters=data)

    def test_reviews_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, (1, 1, 5, 'Excellent product!', '14/01/2024'))

        result = self.select_latest_insert(setup_db)

        assert result["Customer_ID"] == 1
        assert result["Product_ID"] == 1
        assert result["Review_Stars"] == 5
        assert result["Review_Comment"] == 'Excellent product!'
        assert result["Review_Date"] == '14/01/2024'

    def test_reviews_table_referential_integrity(self, setup_db):
        result = self.insert_data(setup_db, (1000, 1, 5, 'Excellent product!', '14/01/2024'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1, 1000, 5, 'Excellent product!', '14/01/2024'))
        assert type(result) == sqlite3.IntegrityError

    def test_reviews_table_not_null_constraints(self, setup_db):
        result = self.insert_data(setup_db, (None, 1, 5, 'Excellent product!', '14/01/2024'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1000, None, 5, 'Excellent product!', '14/01/2024'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1000, 1, None, 'Excellent product!', '14/01/2024'))
        assert type(result) == sqlite3.IntegrityError
        result = self.insert_data(setup_db, (1000, 1, 5, 'Excellent product!', None))
        assert type(result) == sqlite3.IntegrityError



