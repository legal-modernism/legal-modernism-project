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
        
        util.get_book_metadata("20001735402_DocMetadata.xml")
