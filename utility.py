#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Sep 2019

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


def get_all_cap_entities(case_name):
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


def get_legal_treatises_metadata(book_name):
    return


def get_book_metadata(book_name):
    filepath_meta = os.path.join('./example_moml/', '20001735402_DocMetadata.xml')
    root = ET.parse(filepath_meta)

    # Get PSMID
    for elem in root.iter('bookInfo'):
        PSMID = elem.find('PSMID').text

    # Get contentType, ID, FAID and COLID
    for elem in root.iter('book'):
        contentType = elem.attrib['contentType']
        ID = elem.attrib['ID']
        FAID = elem.attrib['FAID']
        COLID = elem.attrib['COLID']

    # Get bookInfo
    for elem in root.iter('bookInfo'):
        bookInfo = {
            "PSMID": PSMID,
            "contentType": contentType,
            "ID": ID,
            "FAID": FAID,
            "COLID": COLID,
            "ocr": elem.find('ocr').text,
            "assetID": elem.find('assetID').text,
            "assetIDeTOC": elem.find('assetIDeTOC').text,
            "dviCollectionID": elem.find('dviCollectionID').text,
            "bibliographicID": elem.find('bibliographicID').text,
            "bibliographicID_type": elem.find('bibliographicID').attrib['type'],
            "unit": elem.find('unit').text,
            "ficheRange": elem.find('unit').text,
            "mcode": elem.find('mcode').text,
            "pubDate_year": elem.find('pubDate').find('year').text,
            "pubDate_composed": elem.find('pubDate').find('composed').text,
            "pubDate_pubDateStart": elem.find('pubDate').find('pubDateStart').text,
            "releaseDate": elem.find('releaseDate').text,
            "sourceLibrary_libraryName": elem.find('sourceLibrary').find('libraryName').text,
            "sourceLibrary_libraryLocation": elem.find('sourceLibrary').find('libraryLocation').text,
            "language": elem.find('language').text,
            "language_ocr": elem.find('language').attrib['ocr'],
            "language_primary": elem.find('language').attrib['primary'],
            "documentType": elem.find('documentType').text,
            "notes": elem.find('notes').text,
            "categoryCode": elem.find('categoryCode').text,
            "categoryCode_source": elem.find('categoryCode').attrib['source'],
            "ProductLink": elem.find('ProductLink').text,
        }
        # print(bookInfo)

    # Get citation
    for elem in root.iter('citation'):
        citation = {
            "PSMID": PSMID,
            "author_role": elem.find('authorGroup').attrib['role'],
            "author_composed": elem.find('authorGroup').find('author').find('composed').text,
            "author_first": elem.find('authorGroup').find('author').find('first').text,
            "author_middle": elem.find('authorGroup').find('author').find('middle').text,
            "author_last": elem.find('authorGroup').find('author').find('last').text,
            "author_birthDate": elem.find('authorGroup').find('author').find('birthDate').text,
            "author_deathDate": elem.find('authorGroup').find('author').find('deathDate').text,
            "fullTitle": elem.find('titleGroup').find('fullTitle').text,
            "displayTitle": elem.find('titleGroup').find('displayTitle').text,
            "variantTitle": elem.find('titleGroup').find('variantTitle').text,
            "edition": elem.find('edition').text,
            "editionStatement": elem.find('editionStatement').text,
            "currentVolume": elem.find('volumeGroup').find('currentVolume').text,
            "volume": elem.find('volumeGroup').find('Volume').text,
            "totalVolumes": elem.find('volumeGroup').find('totalVolumes').text,
            "imprintFull": elem.find('imprint').find('imprintFull').text,
            "imprintPublisher": elem.find('imprint').find('imprintPublisher').text,
            "collation": elem.find('collation').text,
            "publicationPlaceCity": elem.find('publicationPlace').find('publicationPlaceCity').text,
            "publicationPlaceComposed": elem.find('publicationPlace').find('publicationPlaceComposed').text,
            "totalPages": elem.find('totalPages').text
        }
        # print(citation)

    # Get Book_Subject
    subject_list = []
    for elem in root.iter('subject'):
        subject = {
            "PSMID": PSMID,
            "subject": elem.text,
            "source": elem.attrib['source']
        }
        subject_list.append(subject)

    # Get Book_volumeSet
    volumeSet_list = []
    for elem in root.iter('filmedVolume'):
        volumeSet = {
            "PSMID": PSMID,
            "volumeID": elem.attrib['volumeID'],
            "assetID": elem.attrib['assetID'],
            "filmedVolume": elem.text
        }
        volumeSet_list.append(volumeSet)

    # Get Book_locSubjectHead
    locSubjectHead_list = []
    for elem in root.iter('locSubjectHead'):
        for locSubject in elem.iter('locSubject'):
            locSubjectHead = {
                "PSMID": PSMID,
                "type": elem.attrib['type'],
                "subField": locSubject.attrib['subField'],
                "locSubject": locSubject.text
            }
            locSubjectHead_list.append(locSubjectHead)

    # Get Page and Page Content
    page_list = []
    pageContent_list = []
    for elem in root.iter('page'):
        # check if sourcePage exists
        sourcePage = elem.find('pageInfo').find('sourcePage')
        if sourcePage is not None:
            # Get corresponding text
            sourcePage = sourcePage.text

        page = {
            "pageID": elem.find('pageInfo').find('pageID').text,
            "PSMID": PSMID,
            "type": elem.attrib['type'],
            "firstPage": elem.attrib['firstPage'],
            "assetID": elem.find('pageInfo').find('assetID').text,
            "ocrLanguage": elem.find('pageInfo').find('ocrLanguage').text,
            "sourcePage": sourcePage,
            "ocr": elem.find('pageInfo').find('ocr').text,
            "imageLink_pageIndicator": elem.find('pageInfo').find('imageLink').attrib['pageIndicator'],
            "imageLink_width": elem.find('pageInfo').find('imageLink').attrib['width'],
            "imageLink_height": elem.find('pageInfo').find('imageLink').attrib['height'],
            "imageLink_type": elem.find('pageInfo').find('imageLink').attrib['type'],
            "imageLink_colorimage": elem.find('pageInfo').find('imageLink').attrib['colorimage'],
            "imageLink": elem.find('pageInfo').find('imageLink').text
        }
        page_list.append(page)

        # Check if pageContent exists first
        if elem.find('pageContent').find('sectionHeader') is not None:
            # Loop through all section Headers
            # There may be multiple sectionHeaders
            for sectionHeaders in elem.iter('sectionHeader'):
                pageContent = {
                    "pageID": elem.find('pageInfo').find('pageID').text,
                    "PSMID": PSMID,
                    "sectionHeader_type": sectionHeaders.attrib['type'],
                    "sectionHeader": sectionHeaders.text
                }
                pageContent_list.append(pageContent)

    # Get Page OCR Text
    filepath_ocr = os.path.join('./example_moml/', '20001735402_PageText.xml')
    root_ocr = ET.parse(filepath_ocr)

    ocrText_list = []
    for elem in root_ocr.iter('page'):
        ocrText = {
            "pageID": elem.attrib['id'],
            "PSMID": PSMID,
            "ocrText": elem.find('ocrText').text,
        }
        ocrText_list.append(ocrText)

    return


def get_page_text(book_name):
    return

# def get_case(case_name):
#     """Get a case (JSON) to insert into postgresql"""
#     filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
#     with lzma.open(filepath) as in_file:
#         for line in in_file:
#             case = json.loads(str(line, 'utf8'))
#     case_list = [
#         case['id'],
#         case['name'],
#         case['name_abbreviation'],
#         case['decision_date'],
#         case['docket_number'],
#         case['first_page'],
#         case['last_page'],
#         case['frontend_url'],
#         case['volume']['volume_number'],
#         case['reporter']['full_name']
#     ]
#     return case_list


# def get_citations(case_name):
#     """ Get citations from a case (JSON) to insert into postgresql"""
#     filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
#     with lzma.open(filepath) as in_file:
#         for line in in_file:
#             case = json.loads(str(line, 'utf8'))
#     citation_list = []
#     for citation in case['citations']:
#         citation_list.append([case['id'], citation['cite'], citation['type']])
#     return citation_list


# def get_court(case_name):
#     """Get court from a case (JSON) to insert into postgresql"""
#     filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
#     with lzma.open(filepath) as in_file:
#         for line in in_file:
#             case = json.loads(str(line, 'utf8'))
#     court_list = [
#         case['id'],
#         case['court']['id'],
#         case['court']['jurisdiction_url'],
#         case['court']['name'],
#         case['court']['name_abbreviation'],
#         case['court']['slug']
#     ]
#     return court_list


# def get_jurisdiction(case_name):
#     """Get jurisdiction from a case (JSON) to insert into postgresql"""
#     filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
#     with lzma.open(filepath) as in_file:
#         for line in in_file:
#             case = json.loads(str(line, 'utf8'))
#     jurisdiction_list = [
#         case['id'],
#         case['jurisdiction']['id'],
#         case['jurisdiction']['name'],
#         case['jurisdiction']['name_long'],
#         case['jurisdiction']['slug'],
#         case['jurisdiction']['whitelisted']
#     ]
#     return jurisdiction_list


# def pretty_print_case(case_name):
#     """Helper function to pretty print a case"""
#     filepath = os.path.join('../data/', case_name, 'data', 'data.jsonl.xz')
#     with lzma.open(filepath) as in_file:
#         for line in in_file:
#             case = json.loads(str(line, 'utf8'))
#
#     print(json.dumps(case, indent=4, sort_keys=True))
#     print('\n')
#
#     casebody = case["casebody"]["data"]
#     casebody = casebody[:-1]
#     root = etree.fromstring(casebody)
#     print(etree.tostring(root, pretty_print=True).decode())
#     print('\n')
