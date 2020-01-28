#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Created Dec 2019

@author: Jay Zern Ng
"""

import psycopg2

from configparser import ConfigParser


def config(filename='database_moml.ini', section='postgresql'):
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
    sql = """INSERT INTO Book_Info
                (PSMID,
                contentType,
                ID,
                FAID,
                COLID,
                ocr,
                assetID,
                assetIDeTOC,
                dviCollectionID,
                bibliographicID,
                bibliographicID_type,
                unit,
                ficheRange,
                mcode,
                pubDate_year,
                pubDate_composed,
                pubDate_pubDateStart,
                releaseDate,
                sourceLibrary_libraryName,
                sourceLibrary_libraryLocation,
                language,
                language_ocr,
                language_primary,
                documentType,
                notes,
                categoryCode,
                categoryCode_source,
                ProductLink)
             VALUES
                (%s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s);"""
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


def insert_book_citation(list):
    sql = """INSERT INTO Book_Citation
                (PSMID,
                author_role,
                author_composed,
                author_first,
                author_middle,
                author_last,
                author_birthDate,
                author_deathDate,
                fullTitle,
                displayTitle,
                variantTitle,
                edition,
                editionStatement,
                currentVolume,
                volume,
                totalVolume,
                imprintFull,
                imprintPublisher,
                book_collation,
                publicationPlaceCity,
                publicationPlaceComposed,
                totalPages)
             VALUES
                (%s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s);"""
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


def insert_book_subject(list):
    sql = """INSERT INTO Book_Subject
                (PSMID,
                subject,
                source)
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
        cur.executemany(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_book_volume_set(list):
    sql = """INSERT INTO Book_volumeSet
                (PSMID,
                volumeID,
                assetID,
                filmedVolume)
             VALUES
                (%s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_book_loc_subject_head(list):
    sql = """INSERT INTO Book_locSubjectHead
                (PSMID,
                type,
                subField,
                locSubject)
             VALUES
                (%s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_page(list):
    sql = """INSERT INTO Page
                (pageID,
                PSMID,
                type,
                firstPage,
                assetID,
                ocrLanguage,
                sourcePage,
                ocr,
                imageLink_pageIndicator,
                imageLink_width,
                imageLink_height,
                imageLink_type,
                imageLink_colorimage,
                imageLink)
             VALUES
                (%s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_page_content(list):
    sql = """INSERT INTO Page_Content
                (pageID,
                PSMID,
                sectionHeader_type,
                sectionHeader)
             VALUES
                (%s, %s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_page_ocr_text(list):
    sql = """INSERT INTO Page_ocrText
                (pageID,
                PSMID,
                ocrText)
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
        cur.executemany(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_legal_treatises_metadata(list):
    sql = """INSERT INTO Legal_Treatises_Metadata
                (PSMID,
                author_by_line,
                title,
                edition,
                current_volume,
                imprint,
                book_collation,
                pages)
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
        cur.executemany(sql, list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
