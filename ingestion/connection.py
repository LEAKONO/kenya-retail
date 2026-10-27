import snowflake.connector

import config


def get_connection():
    if not config.SNOWFLAKE_ACCOUNT or not config.SNOWFLAKE_USER:
        raise SystemExit("Set SNOWFLAKE_ACCOUNT and SNOWFLAKE_USER in your .env file")

    settings = {
        "account": config.SNOWFLAKE_ACCOUNT,
        "user": config.SNOWFLAKE_USER,
        "role": config.SNOWFLAKE_ROLE,
    }

    if config.SNOWFLAKE_PRIVATE_KEY_PATH:
        settings["private_key_file"] = config.SNOWFLAKE_PRIVATE_KEY_PATH
    elif config.SNOWFLAKE_PASSWORD:
        settings["password"] = config.SNOWFLAKE_PASSWORD
    else:
        raise SystemExit("Set SNOWFLAKE_PASSWORD or SNOWFLAKE_PRIVATE_KEY_PATH in your .env file")

    return snowflake.connector.connect(**settings)


if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_ACCOUNT()")
    print(cur.fetchone())
    cur.close()
    conn.close()