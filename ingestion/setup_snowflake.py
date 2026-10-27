import config
from connection import get_connection


def setup():
    conn = get_connection()
    cur = conn.cursor()

    statements = [
        f"""CREATE WAREHOUSE IF NOT EXISTS {config.WAREHOUSE}
              WAREHOUSE_SIZE = 'XSMALL'
              AUTO_SUSPEND = 60
              AUTO_RESUME = TRUE""",
        f"CREATE DATABASE IF NOT EXISTS {config.DATABASE}",
        f"CREATE SCHEMA IF NOT EXISTS {config.DATABASE}.{config.SCHEMA}",
        f"USE WAREHOUSE {config.WAREHOUSE}",
        f"USE SCHEMA {config.DATABASE}.{config.SCHEMA}",
        f"""CREATE OR REPLACE FILE FORMAT {config.FILE_FORMAT}
              TYPE = 'CSV'
              PARSE_HEADER = TRUE
              FIELD_OPTIONALLY_ENCLOSED_BY = '"'""",
        f"""CREATE STAGE IF NOT EXISTS {config.STAGE}
              FILE_FORMAT = {config.FILE_FORMAT}""",
    ]

    for sql in statements:
        print("Running:", sql.split("\n")[0])
        cur.execute(sql)

    cur.close()
    conn.close()
    print("Setup complete.")


if __name__ == "__main__":
    setup()