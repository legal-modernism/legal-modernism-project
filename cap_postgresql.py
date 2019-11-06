#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created on 15 Sep

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
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def test_connect():
    """Test if postgresql server works"""
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
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Create schema from local SQL file
        schema_file = open('legal_modernism_schema.sql', 'r')
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

def drop_all_tables():
    """Drop tables to refresh"""
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute('DROP TABLE Cases CASCADE;')
    cur.execute('DROP TABLE Citations CASCADE;')
    cur.execute('DROP TABLE Jurisdiction CASCADE;')
    cur.execute('DROP TABLE Courts CASCADE;')
    cur.execute('DROP TABLE Parties CASCADE;')
    cur.execute('DROP TABLE Judges CASCADE;')
    cur.execute('DROP TABLE Attorneys CASCADE;')
    cur.execute('DROP TABLE Headnotes CASCADE;')
    cur.execute('DROP TABLE Summaries CASCADE;')
    cur.execute('DROP TABLE Opinions CASCADE;')
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

def insert_citations_list(clist):
    '''
    Inserts a list of list into the citations table
    '''
    sql = """INSERT INTO citations
                (case_id,
                cite,
                type)
             VALUES
                (%s, %s, %s);"""
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

def insert_courts_list(clist):
    '''
    Inserts a list of list into the courts table
    '''
    sql = """INSERT INTO courts
                (case_id,
                court_id,
                jurisdiction_url,
                name,
                name_abbreviation,
                slug)
             VALUES
                (%s, %s, %s, %s, %s, %s);"""
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

def insert_jurisdiction_list(jlist):
    '''
    Inserts a list of list into the insert_jurisdiction_list table
    '''
    sql = """INSERT INTO jurisdiction
                (case_id,
                jurisdiction_id,
                name,
                name_long,
                slug,
                whitelisted)
             VALUES
                (%s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, jlist)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_casebody_list(clist):
    '''
    Inserts a list of list into the insert_jurisdiction_list table
    '''
    sql = """INSERT INTO Casebody
                (case_id,
                court,
                citation,
                decisiondate,
                docket_number,
                judges,
                parties,
                headnotes,
                summaries,
                opinions)
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
