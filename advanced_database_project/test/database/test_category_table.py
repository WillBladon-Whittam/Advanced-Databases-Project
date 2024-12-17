import sqlite3


class TestCategoryTable:

    @staticmethod
    def select_latest_insert(setup_db):
        return setup_db.select_query(
            """
            SELECT * FROM Category
            WHERE Category_ID = ?
            """, sql_parameters=setup_db.cursor.lastrowid, fetch="one",
        )

    @staticmethod
    def insert_data(setup_db, data):
        return setup_db.update_table("""
                                     INSERT INTO Category (Category_Name) VALUES (?)
                                     """, sql_parameters=data)

    def test_category_table_valid_data_insertion(self, setup_db):
        self.insert_data(setup_db, "Console")

        result = self.select_latest_insert(setup_db)

        assert result["Category_Name"] == "Console"

    def test_category_table_not_null_constraints(self, setup_db):
        result = self.insert_data(setup_db, None)
        assert type(result) == sqlite3.IntegrityError

