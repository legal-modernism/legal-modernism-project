#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15 Sep

@author: Jay Zern Ng

Utility functions to get or print JSON and XML files
"""

import os
import lzma
import json

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def get_all_entities(case_name):
    """Implements all functions below"""
    filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')

    with lzma.open(filepath) as in_file:
        for line in in_file:
            data = json.loads(str(line, 'utf8'))

    # Get cases
    case = [
        data['id'],
        data['name'],
        data['name_abbreviation'],
        data['decision_date'],
        data['docket_number'],
        data['first_page'],
        data['last_page'],
        data['frontend_url'],
        data['volume']['volume_number'],
        data['reporter']['full_name']
    ]

    # Get citations (there may be multiple)
    citations = []
    for citation in data['citations']:
        citations.append([data['id'], citation['cite'], citation['type']])

    # Get jurisdictions
    jurisdiction = [
        data['id'],
        data['jurisdiction']['id'],
        data['jurisdiction']['name'],
        data['jurisdiction']['name_long'],
        data['jurisdiction']['slug'],
        data['jurisdiction']['whitelisted']
    ]

    # Get courts
    court = [
        data['id'],
        data['court']['id'],
        data['court']['jurisdiction_url'],
        data['court']['name'],
        data['court']['name_abbreviation'],
        data['court']['slug']
    ]

    # Handle XML files, Create element tree, Traverse the xml tree
    casebody = data['casebody']['data']
    root = ET.fromstring(casebody)
    parties = []
    judges = []
    headnotes = []
    summary = []
    opinion = []
    attorneys = []

    """TODO: Fix this:
    5. for cases, need to get call casebody attributes and store it in cases
    """

    tag_prefix = "{http://nrs.harvard.edu/urn-3:HLS.Libr.US_Case_Law.Schema.Case_Body:v1}"
    for elem in root.iter():
        if elem.tag == tag_prefix + "judges":
            case_id = data['id']
            judges_id = elem.attrib['id']
            judges_text = ET.tostring(elem, method='text').decode()
            judges.append([case_id, judges_id, judges_text])
        elif elem.tag == tag_prefix + "parties":
            case_id = data['id']
            parties_id = elem.attrib['id']
            parties_text = ET.tostring(elem, method='text').decode()
            parties.append([case_id, parties_id, parties_text])
        elif elem.tag == tag_prefix + "headnotes":
            case_id = data['id']
            headnotes_id = elem.attrib['id']
            headnotes_text = ET.tostring(elem, method='text').decode()
            headnotes.append([case_id, headnotes_id, headnotes_text])
        elif elem.tag == tag_prefix + "summary":
            case_id = data['id']
            summary_id = elem.attrib['id']
            summary_text = ET.tostring(elem, method='text').decode()
            summary.append([case_id, summary_id, summary_text])
        elif elem.tag == tag_prefix + "opinion":
            case_id = data['id']
            opinion_type = elem.attrib['type']
            for child in elem:
                if child.tag == tag_prefix + "p":
                    text_type = "paragraph"
                    text_id = child.attrib['id']
                    text = ET.tostring(child, method='text').decode()
                    opinion.append(
                        [case_id, opinion_type, text_type, text_id, text])
                if child.tag == tag_prefix + "author":
                    text_type = "author"
                    text_id = child.attrib['id']
                    text = ET.tostring(child, method='text').decode()
                    opinion.append(
                        [case_id, opinion_type, text_type, text_id, text])
                if child.tag == tag_prefix + "judges":
                    text_type = "judges"
                    text_id = child.attrib['id']
                    text = ET.tostring(child, method='text').decode()
                    opinion.append(
                        [case_id, opinion_type, text_type, text_id, text])
                if child.tag == tag_prefix + "footnote":
                    for grandchild in child:
                        text_type = "footnote"
                        text_id = grandchild.attrib['id']
                        text = ET.tostring(grandchild, method='text').decode()
                        opinion.append(
                            [case_id, opinion_type, text_type, text_id, text])
        elif elem.tag == tag_prefix + "attorneys":
            case_id = data['id']
            attorneys_id = elem.attrib['id']
            attorneys_text = ET.tostring(elem, method='text').decode()
            attorneys.append([case_id, attorneys_id, attorneys_text])
        else:
            # Else do something here
            pass

    return case, citations, jurisdiction, court, parties, judges, \
        attorneys, headnotes, summary, opinion


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
