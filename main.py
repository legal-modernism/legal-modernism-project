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
    #capapi.download_cap_data()

    # Print subfolers
    #subfolders = [f.path for f in os.scandir('../data/') if f.is_dir() ]
    #print(subfolders)

    # Examples only
    #case_name = 'New Mexico-20190723-xml'
    #case_name = 'Illinois-20190718-xml'
    #case_name = 'Arkansas-20190718-xml'
    #case_name = 'Idaho-20190718-xml'
    #case_name = 'Alaska-20190718-xml'
    #case_name = 'American Samoa-20190718-xml'
    #case_name = 'Dakota Territory-20190718-xml'
    #case_name = 'Hawaii-20190718-xml'
    #case_name = 'Delaware-20190718-xml'
    case_name = 'Guam-20190718-xml'

    # Examples only
    case_names = [
        #'Idaho-20190718-xml',
        #'Alaska-20190718-xml',
        #'American Samoa-20190718-xml',
        #'Dakota Territory-20190718-xml',
        #'Hawaii-20190718-xml',
        'Delaware-20190718-xml',
        'Guam-20190718-xml'
    ]

    # Print a case to see
    #capapi.print_case(case_name)

    # Test your connection
    #capdb.test_connect()

    # Refresh tables
    capdb.drop_all_tables()

    # Create table
    capdb.create_tables()

    # Get case
    case_list = []
    for name in case_names:
        case = util.get_case(name)
        case_list.append(case)

    # Insert JSON into database
    capdb.insert_cases_list(case_list)

    # Get the corresponding casebody
    # Get case
    casebody = util.get_casebody(case_name)
    print(type(casebody))
