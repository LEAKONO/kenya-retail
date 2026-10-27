import config
from connection import get_connection


def upload_files(cur):
    for table in config.TABLES:
        path = config.DATA_DIR / f"{table}.csv"
        if not path.exists():
            raise SystemExit(f"Missing file: {path}")
        cur.execute(
            f"PUT 'file://{path.as_posix()}' @{config.STAGE} "
            "AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
        )
        print(f"Uploaded {path.name}")


def load_tables(cur):
    for table in config.TABLES:
        cur.execute(f"""
            CREATE OR REPLACE TABLE {table} USING TEMPLATE (
                SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
                FROM TABLE(INFER_SCHEMA(
                    LOCATION => '@{config.STAGE}/{table}.csv',
                    FILE_FORMAT => '{config.FILE_FORMAT}')))
        """)
        cur.execute(f"""
            COPY INTO {table}
            FROM @{config.STAGE}/{table}.csv
            FILE_FORMAT = (FORMAT_NAME = '{config.FILE_FORMAT}')
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
        """)
        print(f"Loaded {table}")


def main():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"USE WAREHOUSE {config.WAREHOUSE}")
    cur.execute(f"USE SCHEMA {config.DATABASE}.{config.SCHEMA}")

    upload_files(cur)
    load_tables(cur)

    cur.close()
    conn.close()
    print("Load complete.")


if __name__ == "__main__":
    main()