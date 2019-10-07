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
    print(root.tag)
    print(root.attrib)
    print([elem.tag for elem in root.iter()])

    # Print Pretty the XML File
    #print(etree.tostring(root, pretty_print=True).decode())

    #for child in root:
    #    print(child.tag, child.attrib)

    #party = root.findall('casebody/parties')
    #print(party)


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
