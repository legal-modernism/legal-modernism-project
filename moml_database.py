#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created Dec 2019

@author: Jay Zern Ng
"""

import psycopg2

from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    """Utility function for configuring psycopg2"""
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
    return db


def create_tables():
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Create schema from local SQL file
        schema_file = open('schema/moml_schema.sql', 'r')
        cur.execute(schema_file.read())
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_book_info(list):
    sql = """INSERT INTO Cases
                (case_id,
                name,
                name_abbreviation,
                decision_date,
                docket_number,
                first_page,
                last_page,
                frontend_url,
                volume_number,
                reporter_full_name)
             VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
