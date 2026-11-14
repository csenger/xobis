from xobis.setup import setup_connection
import pytest
import duckdb


@pytest.fixture
def connection() -> duckdb.DuckDBPyConnection:
    return setup_connection()
