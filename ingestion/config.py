import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

WAREHOUSE = "RETAIL_WH"
DATABASE = "KENYA_RETAIL"
SCHEMA = "RAW"
STAGE = "RETAIL_STAGE"
FILE_FORMAT = "CSV_FF"

TABLES = [
    "categories", "products", "stores", "customers", "customers_updates",
    "orders", "order_items", "payments", "deliveries", "reviews",
]

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_PRIVATE_KEY_PATH = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "SYSADMIN")