#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15 Sep

@author: Jay Zern Ng

Utility functions to get or print JSON and XML files
"""

import requests
import os

import lzma
import json
import lxml.etree as etree # don't use lxml
import xml.etree.ElementTree as ET # Try this one instead!

from zipfile import ZipFile
from environs import Env

def get_case(case_name):
    '''
    Get a case (JSON) to insert into postgresql
    '''
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))
    key_list = [
        'id',
        'name',
        'name_abbreviation',
        'decision_date',
        'docket_number',
        'first_page',
        'last_page',
        'frontend_url'
    ]

    # Convert dictionary into a list
    case_list = [case[key] for key in key_list]

    return case_list

def get_casebody(case_name):
    '''
    Get a casebody (XML) to insert into postgresql
    '''
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    # Get the casebody from JSON
    casebody = case['casebody']['data']

    # Create lxml root
    root = ET.fromstring(casebody)
    #for child_of_root in root:
    #    print(child_of_root.tag, child_of_root.attrib)

    #for elem in root.iter():
    #    print(elem.tag, elem.attrib)

    ## O(N^2) NAIVE METHOD
    '''
    court = root.find("{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}court").text
    try:
        citation = root.find("{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}citation").text
    except:
        citation = None
    decisiondate = root.find("{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}decisiondate").text
    docketnumber = root.find("{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}docketnumber").text
    casebody_list = [court, citation, decisiondate, docketnumber]
    print(casebody_list)
    '''

    ## O(N) METHOD: Traverse the xml tree
    court = citation = decisiondate = docketnumber = None
    for elem in root.iter():
        #print(elem, elem.tag)
        if elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}court":
            court = elem.text
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}citation":
            citation = elem.text
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}decisiondate":
            decisiondate = elem.text
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}docketnumber":
            docketnumber = elem.text

    casebody_list = [court, citation, decisiondate, docketnumber]
    print(casebody_list)

def pretty_print_case(case_name):
    '''
    Utility function to pretty print a case.
    '''

    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    # Print pretty the JSON file
    print(json.dumps(case, indent=4, sort_keys=True))
    print('\n')
    # Access the casebody string
    casebody = case["casebody"]["data"]

    # Remove the last characters \n
    casebody = casebody[:-1]

    # Create lxml root
    root = etree.fromstring(casebody)

    # Print Pretty the XML File
    print(etree.tostring(root, pretty_print=True).decode())
    print('\n')
