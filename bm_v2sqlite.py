#! /usr/bin/env python3
"""SQLite importer."""
import sqlite3


def create_connection(db_file):
    """Create a database connection to SQLite specified by db_file.

    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as err:
        print(err)
    return None


def run_sql(conn, sql, entities=None):
    """Execute the sql statement.

    :param conn: Connection object
    :param sql: SQL statement to execute
    :return:
    """
    try:
        cur = conn.cursor()
        if entities is not None:
            cur.execute(sql, entities)
        else:
            cur.execute(sql)
    except sqlite3.Error as err:
        print(err)


def insert(conn, values):
    """Insert values into according columns."""
    statement = """INSERT INTO bookmarks(url, title, date, todo)
                    VALUES(?, ?, ?, ?)"""
    run_sql(conn, statement, values)


def create(conn):
    """Create table."""
    statement = """ CREATE TABLE IF NOT EXISTS bookmarks (
                    url text NOT NULL,
                    title text NOT NULL,
                    date text NOT NULL,
                    todo boolean NOT NULL);"""
    run_sql(conn, statement)


if __name__ == "__main__":
    import sys
    import json

    FNAME = sys.argv[1]
    DB = r"bookmarks.db"

    # create a database connection
    CONN = create_connection(DB)

    # create bookmarks table
    if CONN is not None:
        create(CONN)
    else:
        print("Error! cannot create the database connection.")

    with open(FNAME, encoding="utf-8") as infile:
        DATA = json.load(infile)
    for entry in DATA:
        insert(CONN,
               (entry["url"],
                entry["title"][0],
                entry["date"][0],
                "todo" in entry["tags"]))
    CONN.commit()
    CONN.close()
