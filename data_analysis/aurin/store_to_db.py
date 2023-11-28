"""
Author: Wei Ge - 1074198
        Han Wang - 1041260 
        YanBei Jiang - 1087029
        Yiwen Zhang - 1002781
        Zening Zhang - 1078374
"""
# import sys
# import sys
# sys.path.append("../crawler")
import db_load_data
import json 

def aurin_main():
    doc_education_level = open("aurin/education_level.json",'r')
    doc_housing_price = open("aurin/housing_price.json",'r')
    doc_education_metadata = open("aurin/education_metadata.json",'r')
    doc_education_origin_data = open("aurin/education_origin_data.json",'r')
    doc_house_origin_data = open("aurin/house_origin_data.json",'r')
    doc_house_price_metadata = open("aurin/house_price_metadata.json",'r')

    initialize_couchdb()
    store_to_aurin_cache_db(json.load(doc_education_level))
    store_to_aurin_cache_db(json.load(doc_housing_price))
    store_to_aurin_cache_db(json.load(doc_education_metadata))
    store_to_aurin_cache_db(json.load(doc_education_origin_data))
    store_to_aurin_cache_db(json.load(doc_house_origin_data))
    store_to_aurin_cache_db(json.load(doc_house_price_metadata))
    

    
    
    
    
    

