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
import re
import traceback

import cap_database as cap_db
import moml_database as moml_db
import cap_api as cap_api
import utility as util

if __name__ == "__main__":

    if False:
        # Download CAP data
        cap_api.download_cap_data()

    if False:
        # Get files
        subfolders = [os.path.basename(f.path)
                      for f in os.scandir('../data/') if f.is_dir()]

    if False:
        # Tabulates CAP data
        # Run schema
        cap_db.create_tables()

        # Track progress
        bar = progressbar.ProgressBar(
            maxval=len(subfolders), widgets=[
                progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        """
        TODO: create a log file for errors
        """
        for i, name in enumerate(subfolders):
            bar.update(i + 1)
            try:
                # Get filepath
                filepath = os.path.join('../data/', name, 'data', 'data.jsonl.xz')

                # Get a dictionary of entities
                case = util.get_all_cap_entities(filepath)

                # Tabulate
                cap_db.insert_cases(case["case"])
                cap_db.insert_citations(case["citations"])
                cap_db.insert_jurisdiction(case["jurisdiction"])
                cap_db.insert_courts(case["court"])
                cap_db.insert_parties(case["parties"])
                cap_db.insert_judges(case["judges"])
                cap_db.insert_attorneys(case["attorneys"])
                cap_db.insert_headnotes(case["headnotes"])
                cap_db.insert_summary(case["summary"])
                cap_db.insert_opinion(case["opinion"])
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error in: " + name)
                print("Message: " + error)
        bar.finish()


    moml_db.create_tables()

    if False:
        # Tabulate MOML data
        # Run schema
        moml_db.create_tables()

        # Tabulate legal treatises metadata
        filepath_legal_treatises_metadata = os.path.join(
            './example_moml/',
            'TheMakingofModernLaw_LegalTreatises.csv'
        )
        legal_treatises_metadata = util.get_legal_treatises_metadata(filepath_legal_treatises_metadata)
        moml_db.insert_legal_treatises_metadata(legal_treatises_metadata)

        # Get file dir
        path_moml_f1 = os.path.join('../moml/', 'MOMLF0001-C00000', 'MONOGRAPHS')
        path_moml_f2 = os.path.join('../moml/', 'MOMLF00012-C00000', 'MONOGRAPHS')

        # Get all .xml files
        i = 0
        for filename_meta in os.listdir(path_moml_f1):
            # Handle Metadata first
            if filename_meta.endswith('_DocMetadata.xml'):
                # Then get PageText using regex
                filename_page = re.search('[^(.*?)\_]*', filename_meta).group()
                filename_page += '_PageText.xml'

                # Get file directory here instead of filename
                filepath_meta = os.path.join(path_moml_f1, filename_meta)
                filepath_page = os.path.join(path_moml_f1, filename_page)

                try:
                    book = util.get_book_metadata(filepath_meta, filepath_page)

                    """
                    NOTE: Create connection once only
                    THEN close connection once only after insert many
                    """
                    moml_db.insert_book_info(book['bookInfo'])
                    moml_db.insert_book_citation(book['citation'])
                    moml_db.insert_book_subject(book['subject_list'])
                    moml_db.insert_book_volume_set(book['volumeSet_list'])
                    moml_db.insert_book_loc_subject_head(book['locSubjectHead_list'])
                    moml_db.insert_page(book['page_list'])
                    moml_db.insert_page_content(book['pageContent_list'])
                    moml_db.insert_page_ocr_text(book['ocrText_list'])
                except (Exception, psycopg2.DatabaseError) as error:
                    print(traceback.format_exc())
                    print("Error in: " + filename_meta)
                    print("Message: " + str(error))

                i += 1
                print(i)
                if i == 3:
                    break
