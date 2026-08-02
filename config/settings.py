import os

SQL_CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")

if SQL_CONNECTION_STRING is None:
    raise ValueError("SQL_CONNECTION_STRING environment variable is not set.")