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

from zipfile import ZipFile
from environs import Env

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def get_all_entities(case_name):
    """Implements all functions below"""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    # Get cases
    case_list = [
        case['id'],
        case['name'],
        case['name_abbreviation'],
        case['decision_date'],
        case['docket_number'],
        case['first_page'],
        case['last_page'],
        case['frontend_url'],
        case['volume']['volume_number'],
        case['reporter']['full_name']
    ]

    # Get citations (there may be multiple)
    citation_list = []
    for citation in case['citations']:
        citation_list.append([case['id'], citation['cite'], citation['type']])

    # Get jurisdictions
    jurisdiction_list = [
        case['id'],
        case['jurisdiction']['id'],
        case['jurisdiction']['name'],
        case['jurisdiction']['name_long'],
        case['jurisdiction']['slug'],
        case['jurisdiction']['whitelisted']
    ]

    # Get courts
    court_list = [
        case['id'],
        case['court']['id'],
        case['court']['jurisdiction_url'],
        case['court']['name'],
        case['court']['name_abbreviation'],
        case['court']['slug']
    ]

    # Handle XML files, Create element tree, Traverse the xml tree
    casebody = case['casebody']['data']
    root = ET.fromstring(casebody)
    court = citation = decisiondate = docketnumber = judges = parties = None
    headnotes = []; summaries = []; opinions = []; attorneys = []

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
        if elem.tag == tag_prefix + "court":
            court = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix + "citation":
            citation = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix + "decisiondate":
            decisiondate = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix + "docketnumber":
            docketnumber = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix + "judges":
            judges = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix + "parties":
            parties = ET.tostring(elem, method='text')
        elif elem.tag == tag_prefix + "headnotes":
            headnotes.append([case['id'], ET.tostring(elem, method='text')])
        elif elem.tag == tag_prefix + "summaries":
            summaries.append([case['id'], ET.tostring(elem, method='text')])
        elif elem.tag == tag_prefix + "opinions":
            opinions.append([case['id'], ET.tostring(elem, method='text')])
        elif elem.tag == tag_prefix + "attorneys":
            attorneys.append([case['id'], ET.tostring(elem, method='text')])

    # Get parties
    #parties_list = [
    #    case_id,
    #    parties
    #]

    # Get judges
    #judges_list = [
    #    case_id,
    #    judges
    #]

    # DEBUG:
    #for pair in attorneys:
    #    print(pair)


def get_case(case_name):
    """Get a case (JSON) to insert into postgresql"""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))
    case_list = [
        case['id'],
        case['name'],
        case['name_abbreviation'],
        case['decision_date'],
        case['docket_number'],
        case['first_page'],
        case['last_page'],
        case['frontend_url'],
        case['volume']['volume_number'],
        case['reporter']['full_name']
    ]
    return case_list


def get_citations(case_name):
    """ Get citations from a case (JSON) to insert into postgresql"""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))
    citation_list = []
    for citation in case['citations']:
        citation_list.append([case['id'], citation['cite'], citation['type']])
    return citation_list


def get_court(case_name):
    """Get court from a case (JSON) to insert into postgresql"""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))
    court_list = [
        case['id'],
        case['court']['id'],
        case['court']['jurisdiction_url'],
        case['court']['name'],
        case['court']['name_abbreviation'],
        case['court']['slug']
    ]
    return court_list


def get_jurisdiction(case_name):
    """Get jurisdiction from a case (JSON) to insert into postgresql"""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))
    jurisdiction_list = [
        case['id'],
        case['jurisdiction']['id'],
        case['jurisdiction']['name'],
        case['jurisdiction']['name_long'],
        case['jurisdiction']['slug'],
        case['jurisdiction']['whitelisted']
    ]
    return jurisdiction_list


def pretty_print_case(case_name):
    """Helper function to pretty print a case"""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    print(json.dumps(case, indent=4, sort_keys=True))
    print('\n')

    casebody = case["casebody"]["data"]
    casebody = casebody[:-1]
    root = etree.fromstring(casebody)
    print(etree.tostring(root, pretty_print=True).decode())
    print('\n')
