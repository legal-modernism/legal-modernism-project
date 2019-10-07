#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 15 Sep

@author: Jay Zern Ng

"""

import psycopg2

from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    '''
    Utility function for configuring psycopg2
    '''
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
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def test_connect():
    '''
    Test if postgresql server works
    '''
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

       # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def create_tables():
    '''
    Initialize table from schema
    '''
    commands = (
        """
        CREATE TABLE Cases (
            case_id VARCHAR(256),
            name VARCHAR(256),
            name_abbreviation VARCHAR(256),
            decision_date DATE,
            docket_number VARCHAR(256),
            first_page INTEGER,
            last_page INTEGER,
            frontend_url VARCHAR(256),
            PRIMARY KEY (case_id)
        )
        """,
        """
        CREATE TABLE Casebody (
            case_id VARCHAR(256),
            court VARCHAR(256),
            citation VARCHAR(256),
            decisiondate DATE,
            docket_number VARCHAR(256),
            FOREIGN KEY (case_id)
                REFERENCES Cases
                    ON DELETE CASCADE
                    ON UPDATE SET DEFAULT
        )
        """
    )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def drop_all_tables():
    '''
    Drop tables to refresh
    '''
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute('DROP TABLE Cases CASCADE;')
    cur.execute('DROP TABLE Casebody CASCADE;')
    conn.commit()
    conn.close()

def insert_cases_list(clist):
    '''
    Inserts a list of list into the cases table
    '''
    sql = """INSERT INTO cases
                (case_id,
                name,
                name_abbreviation,
                decision_date,
                docket_number,
                first_page,
                last_page,
                frontend_url)
             VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, clist)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_all_cases():
    '''
    Returns all cases using fetchall()
    '''
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM cases;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
