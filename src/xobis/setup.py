import duckdb
import pathlib

OBIS_OCCURRENCE_PATH = "obis-open-data/occurrence"


def setup_connection() -> duckdb.DuckDBPyConnection:
    """
    Return a connection configured with a view named 'obis' that can be used to query the obis parquet files
    """
    conn: duckdb.DuckDBPyConnection = duckdb.connect()
    datadir = pathlib.Path(OBIS_OCCURRENCE_PATH)
    datapath = datadir.absolute()
    view_query = f"""
      CREATE VIEW obis AS
      SELECT * FROM read_parquet('{datapath}', hive_partitioning=true)
      """
    conn.query(view_query)
    return conn
