import sqlite3
from sqlite3 import Error
import pandas as pd
import argparse

# Python script to execute a SQL statement and store the results in a CSV file.
#
# Usage:
#   python3 run_sql.py [path_to_db] [path_to_sql] [path_to_csv]
#
# Where:
#
#   path_to_db: the path to the sqlite3 database file. default is 
#               "data/movies.db"
# 
#   path_to_sql: the path to the file containing the sql query. default is 
#               "sql/horror_movies.sql"
# 
#   path_to_csv: the path to the csv file that will be created with the results 
#               of the query. default is "data/movies.csv"


def get_paths() -> tuple:
    """Get the paths names from the arguments passed in
    @return a tuple containing (path_to_db, path_to_sql, path_to_csv)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("db", nargs="?",
                        help="path to the sqlite3 database file", 
                        default="db/movies.db")
    parser.add_argument("sql", nargs="?",
                        help="path to the file containing the sql query",
                        default="sql/horror_movies.sql")
    parser.add_argument("csv", nargs="?",
                        help="path to the csv file that will be created",
                        default="data/movies.csv")
    args = parser.parse_args()
    return args.db, args.sql, args.csv


def create_connection(path_to_db_file: str) -> sqlite3.Connection:
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(path_to_db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def get_sql(file_path: str) -> str:
    """retrieve the SQL commands from a text file
    @param: file_path - the path to the text file
    @return: str - a string containing the contents of the file"""
    fd = open(file_path, 'r')
    sql = fd.read()
    fd.close()

    return sql


def main() -> None:
    path_to_db, path_to_sql, path_to_csv = get_paths()
    conn = create_connection(path_to_db)
    sql = get_sql(path_to_sql)
    
    if sql == "-- Add your SQL here" or sql == "":
        print("Error: Add your sql to the sql/horror_movies.sql file before running.")
        exit(1)
    
    if conn is not None:
        movies = pd.read_sql(sql, conn)
        if len(movies) == 0:
            print("Error: query did not return any results")
            exit(1)
        movies.to_csv(path_to_csv, index=False)
    else:
        print("Error: Could not connect to database.")
        exit(1)
        
    conn.close()

    return None


if __name__ == "__main__":
    main()