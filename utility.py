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

def get_all_entities(case_name):
    """Implements all functions below. Use this for O(N)."""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))


    """PART 1. Handle JSON files"""
    # Get the case_id
    case_id = case['id']

    # Get cases
    # TODO: Not done yet
    case_key_list = [
        'id',
        'name',
        'name_abbreviation',
        'decision_date',
        'docket_number',
        'first_page',
        'last_page',
        'frontend_url'
    ]
    case_list = [case[key] for key in case_key_list]

    # Get citations
    citation_dict = case['citations']
    citation_list = []
    for citation in citation_dict:
        citation_list.append([case_id, citation['cite'], citation['type']])

    # Get jurisdictions
    jurisdiction_dict = case['jurisdiction']
    jurisdiction_list = [
        case_id,
        jurisdiction_dict['id'],
        jurisdiction_dict['name'],
        jurisdiction_dict['name_long'],
        jurisdiction_dict['slug'],
        jurisdiction_dict['whitelisted']
    ]

    # Get courts
    court_dict = case['court']
    court_list = [
        case_id,
        court_dict['id'],
        court_dict['jurisdiction_url'],
        court_dict['name'],
        court_dict['name_abbreviation'],
        court_dict['slug']
    ]

    # DEBUG:
    #print(case_list, citation_list, jurisdiction_list, court_list)

    """PART 2. Handle XML files"""
    # Get the casebody from JSON
    casebody = case['casebody']['data']

    # Create Element Tree
    root = ET.fromstring(casebody)

    ## O(N) METHOD: Traverse the xml tree
    court = citation = decisiondate = docketnumber = judges = parties = None
    # List of list
    headnotes = []
    summaries = []
    opinions = []
    attorneys = []
    """TODO: Fix this:
    1. multiple attorneys
    2. multiple Headnotes
    3. multiple Summaries
    4. multiple Opinions
    5. for cases, need to get call casebody attributes and store it in cases
    """
    tag_prefix = "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}"
    for elem in root.iter():
        #print(elem, elem.tag)
        if elem.tag == tag_prefix+"court":
            court = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix+"citation":
            citation = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix+"decisiondate":
            decisiondate = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix+"docketnumber":
            docketnumber = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix+"judges":
            judges = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix+"parties":
            parties = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix+"headnotes":
            headnotes.append([case_id, ET.tostring(elem, method='text')])
        elif elem.tag == tag_prefix+"summaries":
            summaries.append([case_id, ET.tostring(elem, method='text')])
        elif elem.tag == tag_prefix+"opinions":
            opinions.append([case_id, ET.tostring(elem, method='text')])
        elif elem.tag == tag_prefix+"attorneys":
            attorneys.append([case_id, ET.tostring(elem, method='text')])

    # Get parties
    parties_list = [
        case_id,
        parties
    ]

    # Get judges
    judges_list = [
        case_id,
        judges
    ]

    # DEBUG:
    for pair in attorneys:
        print(pair)

def get_case(case_name):
    """Get a case (JSON) to insert into postgresql"""
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

def get_citations(case_name):
    '''
    Get citations (could be more than 1) from a case (JSON) to insert into postgresql
    '''
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    # First get the case id
    case_id = case['id']

    # Then get multiple citations
    citation_dict = case['citations']

    # Convert a list of dicts into a list of list
    citation_list = []
    for citation in citation_dict:
        # add the case_id here
        citation_list.append([case_id, citation['cite'], citation['type']])

    return citation_list

def get_court(case_name):
    '''
    Get court from a case (JSON) to insert into postgresql
    '''
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    # First get the case id
    case_id = case['id']

    # Then get multiple citations
    court_dict = case['court']

    # Convert a list of dicts into a list of list
    court_list = [
        case_id,
        court_dict['id'],
        court_dict['jurisdiction_url'],
        court_dict['name'],
        court_dict['name_abbreviation'],
        court_dict['slug']
    ]

    return court_list

def get_jurisdiction(case_name):
    '''
    Get jurisdiction from a case (JSON) to insert into postgresql
    '''
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    # First get the case id
    case_id = case['id']

    # Then get multiple citations
    jurisdiction_dict = case['jurisdiction']

    # Convert a list of dicts into a list of list
    jurisdiction_list = [
        case_id,
        jurisdiction_dict['id'],
        jurisdiction_dict['name'],
        jurisdiction_dict['name_long'],
        jurisdiction_dict['slug'],
        jurisdiction_dict['whitelisted']
    ]

    return jurisdiction_list

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

    # Get the case_id first
    case_id = case['id']

    # Create Element Tree
    root = ET.fromstring(casebody)

    ## O(N) METHOD: Traverse the xml tree
    court = citation = decisiondate = docketnumber = judges = parties = None
    headnotes = summaries = opinions = None
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
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}judges":
            judges = elem.text
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}parties":
            parties = elem.text
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}headnotes":
            """TODO: FIX THIS, MULTIPLE HEAD NOTES"""
            headnotes = elem.text
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}summaries":
            """TODO: FIX THIS, MULTIPLE HEAD NOTES"""
            summaries = elem.text
        elif elem.tag == "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}opinions":
            opinions  = elem.text

    casebody_list = [
        case_id,
        court,
        citation,
        decisiondate,
        docketnumber,
        judges,
        parties,
        headnotes,
        summaries,
        opinions
    ]

    return casebody_list

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
