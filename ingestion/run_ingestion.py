import sys

from setup_snowflake import setup
from load_files import main as load
from validate_load import validate


def run():
    print("Step 1/3: set up Snowflake objects")
    setup()

    print("\nStep 2/3: upload CSVs and load tables")
    load()

    print("\nStep 3/3: validate row counts")
    if not validate():
        sys.exit("Validation failed - stopping.")

    print("\nIngestion finished successfully.")


if __name__ == "__main__":
    run()