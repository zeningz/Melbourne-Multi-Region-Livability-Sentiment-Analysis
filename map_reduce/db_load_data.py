"""
Author: Wei Ge - 1074198
        Han Wang - 1041260 
        YanBei Jiang - 1087029
        Yiwen Zhang - 1002781
        Zening Zhang - 1078374
"""
import configparser
from glob import glob
from multiprocessing.spawn import old_main_modules
import os
import couchdb
import json

# global variables
db_info_ini_file = "db_config.ini"

username = ""
password = ""
host = ""
port = ""
old_db_name = ""
new_db_name = ""
pro_db_name = ""
cache_tweets_db_name = ""
cache_aurin_db_name = ""
couch = ""


def connect_couchdb(username, password, host, port):
    '''
    Connect to couchdb
    '''
    couch = couchdb.Server('http://' + username + ':' + password + '@' + host + ':' + port)
    return couch


def get_spec_db(db_name):
    '''
    Get the specific database
    '''
    global couch
    # get existed db
    try:
        return couch[db_name]
    # otherwise, create the db
    except:
        return couch.create(db_name)


def get_db_into():
    '''
    Get the database configuration
    @return the dictionary with user and db's information
    '''
    global db_info_ini_file
    # read the configuration file
    curpath = os.path.dirname(os.path.realpath(__file__))
    cfgpath = os.path.join(curpath, db_info_ini_file)
    conf = configparser.ConfigParser()
    conf.read(cfgpath, encoding="utf-8")

    # get the items
    db_user_info = conf.items('user_info')
    db_info = conf.items('db_info')

    # convert tuples to dict
    dict = {}
    for curr_tuple in db_user_info:
        dict[curr_tuple[0]] = curr_tuple[1]
    for curr_tuple in db_info:
        dict[curr_tuple[0]] = curr_tuple[1]
    
    return dict


def initialize_couchdb():
    '''
    Initialize the couchdb
    '''
    print("Initialize the database")
    global username
    global password
    global host
    global port
    global old_db_name
    global new_db_name
    global pro_db_name
    global cache_tweets_db_name
    global cache_aurin_db_name
    global couch
    
    # set up info
    db_info = get_db_into()
    username = db_info['username']
    password = db_info['password']
    host = db_info['host']
    port = db_info['port']
    old_db_name = db_info['old_db_name']
    new_db_name = db_info['new_db_name']
    pro_db_name = db_info['pro_db_name']
    cache_tweets_db_name = db_info['cache_tweets_db_name']
    cache_aurin_db_name = db_info['cache_aurin_db_name']

    # connect the database
    couch = connect_couchdb(username, password, host, port)
    # generate the two database
    get_spec_db(old_db_name)
    get_spec_db(new_db_name)
    get_spec_db(pro_db_name)
    get_spec_db(cache_tweets_db_name)
    get_spec_db(cache_aurin_db_name)
    print("Initialize the database Successfully.\n")


def store_to_old_data_backup_db(data):
    '''
    Accept data and store into backup database which stored old data
    @param data be stored
    '''
    global old_db_name
    global couch

    get_spec_db(old_db_name).save(data)


def store_to_new_data_backup_db(data):
    '''
    Accept data and store into backup database which stored new data
    @param data be stored
    '''
    global new_db_name
    global couch

    # duplication check
    duplicateId = get_spec_db(old_db_name).find({"selector" : {"id" : data["id"]}})
    if (len(list(duplicateId)) == 0):
        get_spec_db(new_db_name).save(data)

def store_to_aurin_cache_db(data):
    '''
    Accept data and store into backup database which stored new data
    @param data be stored
    '''
    global cache_aurin_db_name
    global couch

    get_spec_db(cache_aurin_db_name).save(data)

def store_to_processed_db(data):
    '''
    Accept data and store into processed databse
    @param data be stored
    '''
    global pro_db_name
    global couch

    # duplication check
    duplicateId = get_spec_db(pro_db_name).find({"selector" : {"id": data["id"]}})
    if (len(list(duplicateId)) == 0):
        get_spec_db(pro_db_name).save(data)
    
def store_to_cache_db(data):
    '''
    Accept data and store into processed databse
    @param data be stored
    '''
    global cache_tweets_db_name
    global couch
    
    get_spec_db(cache_tweets_db_name).save(data)

def get_data_from_db(db_name):
    '''
    Get data from couchdb
    @param db_name
    '''
    # get all rows from 
    for id in db_name:
        print(db_name[id])


def empty_spec_db(db_name):
    '''
    Delete all data in the specific database
    @param db: the couchdb
    @param db_name: the specific database be deleted
    '''
    global couch
    couch.delete(db_name)
