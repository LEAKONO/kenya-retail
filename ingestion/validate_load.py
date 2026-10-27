import config
from connection import get_connection


def count_csv_rows(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # minus the header line


def validate():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"USE WAREHOUSE {config.WAREHOUSE}")
    cur.execute(f"USE SCHEMA {config.DATABASE}.{config.SCHEMA}")

    all_ok = True
    print(f"{'table':20s} {'csv':>10s} {'snowflake':>10s}  result")

    for table in config.TABLES:
        csv_rows = count_csv_rows(config.DATA_DIR / f"{table}.csv")
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        sf_rows = cur.fetchone()[0]

        ok = csv_rows == sf_rows
        all_ok = all_ok and ok
        status = "OK" if ok else "MISMATCH"
        print(f"{table:20s} {csv_rows:>10,} {sf_rows:>10,}  {status}")

    cur.close()
    conn.close()
    return all_ok


if __name__ == "__main__":
    passed = validate()
    print("\nAll tables match." if passed else "\nSome tables do NOT match.")
    raise SystemExit(0 if passed else 1)