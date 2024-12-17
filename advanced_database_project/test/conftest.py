import pytest
from pathlib import Path

from advanced_database_project.backend.db_connection import DatabaseConnection


@pytest.fixture(scope="module")
def setup_db():
    """
    Set up the database for testing
    Run the .sql script to create the database.
    Clear the contents of the database, so no data is present
    Then run the tests.
    After the tests are run, rebuild the database again to clear anything changed from the test
    """
    db = DatabaseConnection()
    db.run_sql_script(Path("create_database_script.sql"))

    yield db

    db.run_sql_script(Path("create_database_script.sql"))
