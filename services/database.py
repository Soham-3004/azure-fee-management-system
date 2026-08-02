import pyodbc
from config.settings import SQL_CONNECTION_STRING

def get_connection():
    return pyodbc.connect(SQL_CONNECTION_STRING)

def execute_query(query, params = None):
    con = get_connection()
    try:   
        cursor = con.cursor()
        cursor.execute(query,params or [])
        row = cursor.fetchone()
        return row
    finally:
        con.close()
    
def execute_non_query(query, params = None):
    con = get_connection()
    try:   
        cursor = con.cursor()
        cursor.execute(query,params or [])
        con.commit()
        rows_affected = cursor.rowcount
        return rows_affected
    finally:
        con.close()