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
import logging
import lzma
import json

import cap_database as cap_db
import moml_database as moml_db
import cap_api as cap_api
import utility as util

if __name__ == "__main__":

    # Directory of CAP
    CAP_DIR = '../cap/'
    MOML_DIR = '../moml/'

    # Download CAP data
    if False:
        cap_api.download_cap_data()

    if True:
        # Get files
        subfolders = [os.path.basename(f.path)
                      for f in os.scandir(CAP_DIR) if f.is_dir()]

    # Tabulates CAP data
    if True:
        # Run schema
        cap_db.create_tables()

        # Track progress
        bar = progressbar.ProgressBar(
            maxval=len(subfolders), widgets=[
                progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        # Add logging for files that failed
        CAP_LOG_FILENAME = 'cap_errors.log'
        logging.basicConfig(filename=CAP_LOG_FILENAME, level=logging.DEBUG)

        # Iterate through all subfolders
        for i, name in enumerate(subfolders):
            bar.update(i + 1)

            # Get filepath of subfolder
            filepath = os.path.join(CAP_DIR, name, 'data', 'data.jsonl.xz')

            with lzma.open(filepath, mode='rt') as file:
                # For each subfolder, iterate through all cases
                for line in file:
                    data = json.loads(line)
                    case = util.get_all_cap_entities(data)
                    try:
                        # Get a dictionary of entities
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
                        # print(traceback.format_exc())
                        # print("Error in: " + name)
                        # print(error)
                        logging.debug(traceback.format_exc())
        bar.finish()

    # Tabulate MOML data
    if True:
        # Run schema
        moml_db.create_tables()

        # Tabulate legal treatises metadata
        filepath_legal_treatises_metadata = os.path.join(
            './example_moml/',
            'TheMakingofModernLaw_LegalTreatises.csv'
        )
        legal_treatises_metadata = util.get_legal_treatises_metadata(filepath_legal_treatises_metadata)
        moml_db.insert_legal_treatises_metadata(legal_treatises_metadata)

        # Add logging for files that failed
        MOML_LOG_FILENAME = 'moml_errors.log'
        logging.basicConfig(filename=MOML_LOG_FILENAME, level=logging.DEBUG)


        # Get file dir for first folder
        path_moml_f1 = os.path.join(MOML_DIR, 'MOMLF0001-C00000', 'MONOGRAPHS')
        # Track progress
        bar = progressbar.ProgressBar(
            maxval=len(os.listdir(path_moml_f1)), widgets=[
                progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for i, filename_meta in enumerate(os.listdir(path_moml_f1)):
            bar.update(i + 1)

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

                    moml_db.insert_book_info(book['bookInfo'])
                    moml_db.insert_book_citation(book['citation'])
                    moml_db.insert_book_subject(book['subject_list'])
                    moml_db.insert_book_volume_set(book['volumeSet_list'])
                    moml_db.insert_book_loc_subject_head(
                        book['locSubjectHead_list'])
                    moml_db.insert_page(book['page_list'])
                    moml_db.insert_page_content(book['pageContent_list'])
                    moml_db.insert_page_ocr_text(book['ocrText_list'])
                except (Exception, psycopg2.DatabaseError) as error:
                    # print(traceback.format_exc())
                    # print("Error in: " + filename_meta)
                    # print("Message: " + str(error))
                    logging.debug(traceback.format_exc())
        bar.finish()

        # Repeat for second folder of MOML
        path_moml_f2 = os.path.join(MOML_DIR, 'MOMLF0002-C00000', 'MONOGRAPHS')
        # Track progress
        bar = progressbar.ProgressBar(
            maxval=len(os.listdir(path_moml_f2)), widgets=[
                progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()

        for i, filename_meta in enumerate(os.listdir(path_moml_f2)):
            bar.update(i + 1)

            # Handle Metadata first
            if filename_meta.endswith('_DocMetadata.xml'):
                # Then get PageText using regex
                filename_page = re.search('[^(.*?)\_]*', filename_meta).group()
                filename_page += '_PageText.xml'

                # Get file directory here instead of filename
                filepath_meta = os.path.join(path_moml_f2, filename_meta)
                filepath_page = os.path.join(path_moml_f2, filename_page)

                try:
                    book = util.get_book_metadata(filepath_meta, filepath_page)
                    moml_db.insert_book_info(book['bookInfo'])
                    moml_db.insert_book_citation(book['citation'])
                    moml_db.insert_book_subject(book['subject_list'])
                    moml_db.insert_book_volume_set(book['volumeSet_list'])
                    moml_db.insert_book_loc_subject_head(
                        book['locSubjectHead_list'])
                    moml_db.insert_page(book['page_list'])
                    moml_db.insert_page_content(book['pageContent_list'])
                    moml_db.insert_page_ocr_text(book['ocrText_list'])
                except (Exception, psycopg2.DatabaseError) as error:
                    # print(traceback.format_exc())
                    # print("Error in: " + filename_meta)
                    # print("Message: " + str(error))
                    logging.debug(traceback.format_exc())

        bar.finish()
