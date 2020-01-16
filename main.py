#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15 Sep

@author: Jay Zern Ng

Main script that runs cap_api and cap_postgesql
"""

import os
import progressbar
import psycopg2

import cap_database as cap_db
import moml_database as moml_db
import cap_api as cap_api
import utility as util

from sqlalchemy import *
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

if __name__ == "__main__":
    if False:
        # Fetch data
        cap_api.download_cap_data()

    if False:
        # Print jurisdictions
        subfolders = [os.path.basename(f.path)
                      for f in os.scandir('../data/') if f.is_dir()]
        print(len(subfolders))

        # # Examples only
        # subfolders = [
        #     'Dakota Territory-20190718-xml'
        #     # 'American Samoa-20190927-xml'
        # ]

    # Tabulate CAP data
    if False:
        # Create table
        cap_db.create_tables()

        # Track progress
        bar = progressbar.ProgressBar(
            maxval=len(subfolders), widgets=[
                progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        """
        NOTE:
        Errors with
        Native American-20190927-xml
        Regional-20190927-xml
        """
        for i, name in enumerate(subfolders):
            bar.update(i + 1)
            try:
                # Parse each entity
                case, citations, jurisdiction, \
                    court, parties, judges, \
                    attorneys, headnotes, summary, \
                    opinion = util.get_all_cap_entities(name)

                cap_db.insert_cases(case)
                cap_db.insert_citations(citations)
                cap_db.insert_jurisdiction(jurisdiction)
                cap_db.insert_courts(court)
                cap_db.insert_parties(parties)
                cap_db.insert_judges(judges)
                cap_db.insert_attorneys(attorneys)
                cap_db.insert_headnotes(headnotes)
                cap_db.insert_summary(summary)
                cap_db.insert_opinion(opinion)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error in: " + name)
                print("Message: " + error)
        bar.finish()

    # Tabulate MOML data
    if True:
        moml_db.create_tables()
        book = util.get_book_metadata("20001735402_DocMetadata.xml")
        legal_treatises_metadata = util.get_legal_treatises_metadata()
        # print(output['bookInfo'])

        # Test insert list of dictionaries
        """
        NOTE: Create connection once only
        THEN close connection once only after insert many
        """

        # TRY: sqlalchemy
        # engine = create_engine("postgresql://postgres:amaurylovesalex@127.0.0.1/Legal_Modernism_Project")
        # connection = engine.connect()
        # Create table
        # metadata = MetaData()
        # book_info = Table('Book_Info', metadata,
        #     Column('PSMID', String(255), primary_key=True),
        #     Column('contentType', String(255)),
        #     Column('ID', String(255)),
        #     Column('FAID', String(255)),
        #     Column('COLID', String(255)),
        #     Column('ocr', String(255)),
        #     Column('assetID', String(255)),
        #     Column('assetIDeTOC', String(255)),
        #     Column('dviCollectionID', String(255)),
        #     Column('bibliographicID', String(255)),
        #     Column('bibliographicID_type', String(255)),
        #     Column('unit', String(255)),
        #     Column('ficheRange', String(255)),
        #     Column('mcode', String(255)),
        #     Column('pubDate_year', String(255)),
        #     Column('pubDate_composed', String(255)),
        #     Column('pubDate_pubDateStart', String(255)),
        #     Column('releaseDate', String(255)),
        #     Column('sourceLibrary_libraryName', String(255)),
        #     Column('sourceLibrary_libraryLocation', String(255)),
        #     Column('language', String(255)),
        #     Column('language_ocr', String(255)),
        #     Column('language_primary', String(255)),
        #     Column('documentType', String(255)),
        #     Column('notes', String(255)),
        #     Column('categoryCode', String(255)),
        #     Column('categoryCode_source', String(255)),
        #     Column('ProductLink', String)
        # )
        #
        #
        # connection.close()
        
        moml_db.insert_book_info(book['bookInfo'])
        moml_db.insert_book_citation(book['citation'])
        moml_db.insert_book_subject(book['subject_list'])
        moml_db.insert_book_volume_set(book['volumeSet_list'])
        moml_db.insert_book_loc_subject_head(book['locSubjectHead_list'])
        moml_db.insert_page(book['page_list'])
        moml_db.insert_page_content(book['pageContent_list'])
        moml_db.insert_page_ocr_text(book['ocrText_list'])

        moml_db.insert_legal_treatises_metadata(legal_treatises_metadata)
