from IPython import start_ipython
from traitlets.config import Config

from xobis.setup import setup_connection  # wherever it lives

IPYTHON_BANNER = """
OBIS Repl
  `conn` is the duckdb connection
  `obis` is a view at the occurrence data

Example query:
  conn.sql("SELECT count(*) FROM obis").fetchall()[0][0]

"""


def main() -> None:
    print("Hello from xobis!")


def ipython_repl() -> None:
    conn = setup_connection()
    try:
        c = Config()
        c.HistoryManager.hist_file = (
            ".repl_history.sqlite"  # per-project history (optional)
        )
        c.TerminalInteractiveShell.banner1 = IPYTHON_BANNER
        start_ipython(argv=[], config=c, user_ns={"conn": conn})
    finally:
        conn.close()
