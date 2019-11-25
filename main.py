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


from cap_api import *
from cap_postgresql import *
from utility import *

if __name__ == "__main__":
    if False:
        # Fetch data
        download_cap_data()

    if True:
        # Print jurisdictions
        subfolders = [os.path.basename(f.path)
            for f in os.scandir('../data/') if f.is_dir()]
        print(len(subfolders))
    else:
        # Examples only
        subfolders = [
            'Dakota Territory-20190718-xml'
            # 'American Samoa-20190927-xml'
        ]

    if True:
        # Create table
        create_tables()

    # Track progress
    bar = progressbar.ProgressBar(
        maxval=len(subfolders), widgets=[
            progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    """
    Errors:
    Native American-20190927-xml
    Regional-20190927-xml
    """

    for i, name in enumerate(subfolders):
        bar.update(i+1)
        try:
            case, citations, jurisdiction, court, parties, judges, \
                attorneys, headnotes, summary, opinion = get_all_entities(name)
            insert_cases(case)
            insert_citations(citations)
            insert_jurisdiction(jurisdiction)
            insert_courts(court)
            insert_parties(parties)
            insert_judges(judges)
            insert_attorneys(attorneys)
            insert_headnotes(headnotes)
            insert_summary(summary)
            insert_opinion(opinion)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: "+name)
    bar.finish()
