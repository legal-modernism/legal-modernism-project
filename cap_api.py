#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15 Sep

@author: Jay Zern Ng

# Case Law Access Project
Source: https://case.law
Learn how to access bulk data here: https://case.law/bulk/
"""

import numpy as np
import pandas as pd
import requests
import os

import lzma
import json
import lxml.etree as etree

from zipfile import ZipFile
from environs import Env

def download_cap_data():
    """
    Requests data from caselaw and stores it in ../data/
    """
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

        # check if file exists
        file_exists = os.path.exists('../data/'+download_filename)

        if file_exists:
            print(download_filename+' already exists.')
        else:
            # Request the file
            download_request = requests.get(
                download_url,
                headers={'Authorization': 'Token e3db7dd707ff11888ac0da88153ab3a4470944bd'}
            )

            # Download the file
            # save file in ../data/*
            file_dir = os.path.join('../data/', download_filename)

            with open(file_dir, 'wb') as f:
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
    """
    Utility function to pretty print a case.
    """

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
