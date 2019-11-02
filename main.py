#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15 Sep

@author: Jay Zern Ng

Main script that runs cap_api and cap_postgesql

"""

import cap_api as capapi
import cap_postgresql as capdb
import utility as util

if __name__ == "__main__":
    # Fetch data
    if False:
        capapi.download_cap_data()

    # Print subfolers
    if False:
        subfolders = [f.path for f in os.scandir('../data/') if f.is_dir() ]
        print(subfolders)

    # Examples only
    case_names = [
        'Dakota Territory-20190718-xml'
    ]

    # Print a case to see
    if False:
        capapi.print_case(case_name)

    # Test your connection
    if False:
        capdb.test_connect()

    # Refresh tables
    if False:
        capdb.drop_all_tables()

    # Create table
    if False:
        capdb.create_tables()

    for name in case_names:
        print(name)
        util.get_all_entities(name)

    # """DONE"""
    # INSERT cases table
    #case_list = []
    #for name in case_names:
    #    case = util.get_case(name)
    #    case_list.append(case)
    #capdb.insert_cases_list(case_list)

    # """DONE"""
    # # INSERT citations table
    # citation_list = []
    # for name in case_names:
    #     citation = util.get_citations(name)
    #     citation_list = citation_list + citation
    # capdb.insert_citations_list(citation_list)
    #
    #
    # """DONE"""
    # # INSERT courts table
    # court_list = []
    # for name in case_names:
    #     court = util.get_court(name)
    #     court_list.append(court)
    # capdb.insert_courts_list(court_list)
    #
    # """DONE"""
    # # INSERT Jurisdiction table
    # jurisdiction_list = []
    # for name in case_names:
    #     jurisdiction = util.get_jurisdiction(name)
    #     jurisdiction_list.append(jurisdiction)
    # capdb.insert_jurisdiction_list(jurisdiction_list)
    #
    # """DONE"""
    # # Get the corresponding casebody
    # casebody_list = []
    # for name in case_names:
    #     casebody = util.get_casebody(name)
    #     casebody_list.append(casebody)
    # capdb.insert_casebody_list(casebody_list)
