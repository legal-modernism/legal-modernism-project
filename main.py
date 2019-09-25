#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15 Sep

@author: Jay Zern Ng

# Case Law Access Project
### Source: https://case.law
### Learn how to access bulk data here: https://case.law/bulk/
"""
import numpy as np
import pandas as pd
import requests
import zipfile, io
import urllib.request
import urllib
import os

import lzma
import json
import lxml.etree as etree
import xml.etree.ElementTree as ET
import xml.dom.minidom

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from os import listdir
from os.path import isfile, join
from environs import Env

def download_cap_data():
    # Read environment variables from .env file
    env = Env()
    env.read_env()

    # WARNING:
    # 1. Do not share API_KEY with others!
    # 2. Make sure .env is in .gitignore
    API_KEY = env("API_KEY");

    # Note: set body_format to xml
    # Important: Set token for API authorization, do not share this!
    response = requests.get(
        "https://api.case.law/v1/bulk/?body_format=xml&filter_type=jurisdiction",
        headers={'Authorization': 'Token '+API_KEY}
    )

    if response.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(response.status_code))
    else:
        print(response.status_code)

    # Print pretty the GET request
    print(json.dumps(response.json(), indent=4, sort_keys=True))

    # Cycle through each document and download it
    print("Downloading...")
    for result in response.json()["results"]:

        # Get the url
        download_url = result['download_url']

        # Get the filename
        download_filename = result['file_name']

        # Check
        print('{} {}'.format(download_filename, download_url))

        # TODO: Check if the file has been downloaded already

        # Request the file
        download_request = requests.get(
            download_url,
            headers={'Authorization': 'Token e3db7dd707ff11888ac0da88153ab3a4470944bd'}
        )

        # save file in ../data/*
        with open('../data/'+download_filename, 'wb') as f:
            f.write(download_request.content)

        # Unzip the file
        with ZipFile('../data/'+download_filename, 'r') as zip:
            # printing all the contents of the zip file
            zip.printdir()

            # extracting all the files
            print('Extracting all the files now...')
            zip.extractall(path='../data/')
            print('Done!')

def print_case(case_name):

    filepath = '../data/'

    filepath = case_name

    filepath += '/data/data.jsonl.xz'

    with lzma.open(filepath) as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))

    # Print pretty the JSON file
    print(json.dumps(case, indent=4, sort_keys=True))

    # Access the casebody string
    casebody = case["casebody"]["data"]

    # Remove the last characters \n
    casebody = casebody[:-1]

    # Create lxml root
    root = etree.fromstring(casebody)

    # Print Pretty the XML File
    print(etree.tostring(root, pretty_print=True).decode())

if __name__ == "__main__":

    # Fetch data
    #download_cap_data()

    # Print subfolers
    subfolders = [f.path for f in os.scandir('../data/') if f.is_dir() ]
    print(subfolders)

    # Example public data
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

    # Print a case to see
    #print_case(case_name)
