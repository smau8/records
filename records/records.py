#!/usr/bin/env python

"""
A function for gathering data from GBIF via REST API based on 
user's search criteria ()
"""

import pandas as pd
import requests
import json

class Records:
    def __init__(self, genus=None, year=None):
        
        # store input params
        self.genus = genus
        self.year = year
        
        # will be used to store output results
        self.df = pd.DataFrame()
        self.json = {}
    
    # add function to differentiate between genus or genusKey as input
    def get_genus(self):
        if type(self.genus) == int:
            self.genusKey = self.genus
        else:
            result = requests.get(
            url="https://api.gbif.org/v1/species/match/",
            params={"genus": self.genus},
            )
            self.genusKey = result.json()["genusKey"]
        return self.genusKey

    def get_single_batch(self, offset=0, limit=20):
        "returns JSON result for a small batch query"
        result = requests.get(
        url="https://api.gbif.org/v1/occurrence/search/",
        params={
            "genusKey": self.genusKey,
            "year": self.year,
            "offset": offset,
            "limit": limit,
        }
        )
        result_dict = result.json()
        return result_dict
        
    def get_all_records(self):
        """
        Iterate requests over incremental offset positions until
        all records have been fetched. When the last record has
        been fetched the key 'endOfRecords' will be 'true'. Takes
        the API params as a dictionary. Returns result as a list
        of dictionaries.
        """
        # for storing results
        alldata = []
    
        # continue until we call 'break'
        offset = 0
        while 1:
        
            # get JSON data for a batch 
            jdata = self.get_single_batch(offset, 300)
        
            # increment counter by 300 (the max limit)
            offset += 300
        
            # add this batch of data to the growing list
            alldata.extend(jdata["results"])
        
            # stop when end of record is reached
            if jdata["endOfRecords"]:
                print(f'Done. Found {len(alldata)} records')
                break
            
            # print a dot on each rep to show progress
            print('.', end='')
            
        self.json = json.dumps(alldata)
        self.df = pd.json_normalize(alldata)

       

# demo for testing
    #rec = Records(genusKey=1340278, year="1980,1985")
    #rec.get_genus()
    #rec.get_single_batch(offset=0, limit=10)
    #rec.get_all_records()
    #rec.df.shape
    #rec.json[:500]
