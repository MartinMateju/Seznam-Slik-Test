import mysql.connector
import csv
import config as CONFIG

from concurrent.futures import ThreadPoolExecutor


def get_db_connecetion():
    """Returns db-connection"""
    try:
        config = {
            'user': CONFIG.USER,
            'password': CONFIG.PASSWORD,
            'host': CONFIG.HOST,
            'port': CONFIG.PORT,
            'database': CONFIG.DB_TEST
        }
        conn = mysql.connector.connect(**config)
    except Exception as exc:
        print('DB-connection failed due to err: %s', repr(exc))
    return conn


def create_db_scheme():
    """Creates db-scheme"""
    try:
        config = {
            'user': CONFIG.USER,
            'password': CONFIG.PASSWORD,
            'host': CONFIG.HOST,
            'port': CONFIG.PORT,
        }
        conn = mysql.connector.connect(**config)
        cur = conn.cursor(dictionary=True)
        with open('./db/init.sql', 'r') as sql_file:
            result_iterator = cur.execute(sql_file.read(), multi=True)
            for res in result_iterator:
                print("Running query: ", res)  # Will print out a short representation of the query
                print(f"Affected {res.rowcount} rows" )
            conn.commit()
    except Exception as exc:
        print('Failed to create db-scheme: %s', repr(exc))
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


def run_io_tasks_in_parallel(tasks):
    """Execute tasks in parallel"""
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def test_db_connection():
    """Validates db connection"""
    status = 'Failed'
    try:
        connection = get_db_connecetion()
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Exception as exc:
        print("Error while connecting to MySQL. err: %s", repr(exc))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            status = 'Success'
        return status


def load_csv(path):
    """Load csv data"""
    rows = []
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        headers = next(csvreader)
        for row in csvreader:
            rows.append(tuple(row))
    file.close()
    return {'rows': rows, 'headers': headers}


def db_import(data, table, query):
    """Imports data to mySql-db"""
    try:
        print('sql query: %s', query)
        connection = get_db_connecetion()
        cursor = connection.cursor()
        cursor.executemany(query, data)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into %s table", table)
    except Exception as exc:
        print("Failed to insert record into MySQL table %s, err %s", table, repr(exc))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def execute_query(query):
    """Executes mysql query"""
    try:
        connection = get_db_connecetion()
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
    except Exception as exc:
        print("Failed reading data from MySQL table", exc)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
        return records
